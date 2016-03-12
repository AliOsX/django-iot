from django.contrib import admin
from django_iot.apps.observations.models import Attribute, PowerStatus, Color


admin.site.register(Attribute)
admin.site.register(PowerStatus)
admin.site.register(Color)
