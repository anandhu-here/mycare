
from rest_framework import serializers
from .models import AssignedCarer, Availability, Shift


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = "__all__"


class AVSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'carer', 'count')

    


class AssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedCarer
        fields = "__all__"