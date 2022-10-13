
from rest_framework import serializers
from .models import Availability, Shift


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = "__all__"


class AVSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = "__all__"



