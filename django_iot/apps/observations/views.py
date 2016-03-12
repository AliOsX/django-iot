from rest_framework import viewsets
from rest_framework import filters
from django_iot.apps.observations.models import Attribute, PowerStatus
from django_iot.apps.observations.serializers import AttributeSerializer, PowerStatusSerializer


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('device', 'units')
    ordering_fields = ('valid_at',)
    ordering = ('valid_at',)


class PowerStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PowerStatus.objects.all()
    serializer_class = PowerStatusSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('device',)
    ordering_fields = ('valid_at',)
    ordering = ('-valid_at',)
