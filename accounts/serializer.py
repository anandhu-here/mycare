
from rest_framework import serializers
from .models import User, HomeProfile
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
  profile = serializers.SerializerMethodField(read_only = True)
  type = serializers.SerializerMethodField()
  class Meta:
    model = User
    fields = ('id', 'email', 'last_login', "first_login", "staff", "admin", "home", "carer", "profile", "type", "push_token")
  def get_type(self, obj):
    if obj.home:
      return "HOME"
    else:
      return "CARER"
  def get_profile(self, obj):
    # if(obj.home):
    #   profile = HomeProfile.objects.get(home = obj)
    #   return HomeProfileSerializer(profile).data
    # else:
    #   user = Profile.objects.get(user = obj)
    #   return ProfileSerializer(user, context={"shift_id":False}).data
    pass 
# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
  type = serializers.SerializerMethodField()
  class Meta:
    model = User
    fields = ('id', 'email', 'password', 'type', 'push_token')
    extra_kwargs = {'password': {'write_only': True}}
  def create(self, validated_data):
    user_type = self.context['type']
    if(user_type=='CARER'):
      user = User.objects.create_carer_user(**validated_data)
      return user
    elif(user_type=='HOME'):
      user = User.objects.create_home_user(**validated_data)
      return user
    return
# Login Serializer
class LoginSerializer(serializers.Serializer):
  email = serializers.CharField()
  password = serializers.CharField()
  def validate(self, data):
    try:
      user = User.objects.get(email=data['email'])
    except User.DoesNotExist:
      raise serializers.ValidationError("Incorrect Credentials")
    user = authenticate(email=user.email, password=data['password'])
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Incorrect Credentials")
