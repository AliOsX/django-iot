from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from rest_framework.views import APIView
from rest_framework import serializers
from django_iot.apps.interactions import tasks
from django_iot.apps.devices.models import Device
from django_iot.apps.observations.models import Attribute, PowerStatus


# serializers

class DevicePkSerializer(serializers.Serializer):
    # device pk
    device_id = serializers.IntegerField()

    def validate_device_id(self, value):
        if not Device.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No device available with id %d' % value)
        return value


class DeviceStatusSerializer(DevicePkSerializer):
    # desired status
    is_on = serializers.BooleanField()


class DeviceAttributeSerializer(DevicePkSerializer):
    # desired color
    color = serializers.CharField(required=False)

    # desired brightness
    brightness = serializers.FloatField(required=False)


# views


class BaseInteractionView(APIView):
    def get_task_function(self):
        # necessary to avoid
        #    TypeError: ... got multiple values for keyword argument '...'
        return getattr(tasks, self.task_name)

    def post(self, request, format=None):
        # validate using serializer
        ser = self.serializer_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            # run task
            task = self.get_task_function()
            pks = task(**ser.validated_data)

            # redirect to results
            if len(pks) == 1:
                # redirect to detail
                obj = self.output_model.objects.get(pk=pks[0])
                return redirect(obj)

            else:
                # redirect to filtered list
                url = reverse(self.redirect_list_url) + '?device=%d' % ser.data['device_id']
                return redirect(url)


class PullStatus(BaseInteractionView):
    serializer_class = DevicePkSerializer
    output_model = PowerStatus
    task_name = 'pull_status'
    redirect_list_url = 'powerstatus-list'


class PullData(BaseInteractionView):
    serializer_class = DevicePkSerializer
    output_model = Attribute
    task_name = 'pull_data'
    redirect_list_url = 'attribute-list'


class SetStatus(BaseInteractionView):
    serializer_class = DeviceStatusSerializer
    output_model = PowerStatus
    task_name = 'set_status'
    redirect_list_url = 'powerstatus-list'


class SetAttributes(BaseInteractionView):
    serializer_class = DeviceAttributeSerializer
    output_model = Attribute
    task_name = 'set_attributes'
    redirect_list_url = 'attribute-list'
