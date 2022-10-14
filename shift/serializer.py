
from rest_framework import serializers
from .models import Availability, Shift


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = "__all__"


class AVSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = Availability
        fields = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'carer', 'count')

    def get_count(self, obj):
        print(type(obj), "object")


