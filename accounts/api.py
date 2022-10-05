from backend.shift.models import ShiftName
from rest_framework import generics, permissions, views, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.parsers import MultiPartParser, FormParser
from .serializer import HomeProfileSerializer, ProfileSerializer, UserSerializer, RegisterSerializer, LoginSerializer, DocsSerializer, TimesheetSerializer
import random
from rest_framework import parsers
from  rest_framework.permissions import IsAuthenticated
from .models import AgentProfile, HomeProfile, Profile, User, Docs, Timesheets
from rest_framework.decorators import api_view, permission_classes

class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer
  def post(self, request, *args, **kwargs):
    data = request.data
    email = data['email']
    password = data['password']
    push_token = data['push_token']
    type = data['type']
    serializer = self.get_serializer(data={
      "email":email,
      "password":password,
      "push_token":push_token
    }, context={'type':data['type']})
    if serializer.is_valid(raise_exception=True):

      if type == "HOME":
        user = serializer.save()
        profile = HomeProfile.objects.get(home=user)
        profile.name = data['home_name']
        profile.save()
          
          
    
      
      if type == 'CARER':
        carer = Profile.objects.get(user = user)
        carer.first_name = data['first_name']
        carer.last_name = data['last_name']
        carer.save()
      return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1],
        "message":"authorized"
      })

# Login API
class LoginAPI(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    _, token = AuthToken.objects.create(user)
    
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": token,
      "message":"authorized"
    })

# Get User API
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def UserAPI(request, *args, **kwargs):
  user = request.user
  serializer = UserSerializer(user)
  _, token = AuthToken.objects.create(user)
  home_img_url = 'http://localhost:8000/media/care.jpg'
  return Response({
    "user":serializer.data,
    "token":token,
    "message":"authorized",
    home_img_url:home_img_url
  })