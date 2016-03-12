from rest_framework import serializers
from django_iot.apps.observations.models import Attribute, PowerStatus


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute


class PowerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerStatus
