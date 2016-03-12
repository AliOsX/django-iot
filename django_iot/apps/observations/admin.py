from django.contrib import admin
from django_iot.apps.observations.models import Attribute, PowerStatus


admin.site.register(Attribute)
admin.site.register(PowerStatus)
