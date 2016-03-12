from django.conf.urls import url
from django_iot.apps.interactions import views


urlpatterns = [
    url(r'^interactions/pull_status[/]', views.PullStatus.as_view(), name='pull-status'),
    url(r'^interactions/set_status[/]', views.SetStatus.as_view(), name='set-status'),
    url(r'^interactions/pull_data[/]', views.PullData.as_view(), name='pull-data'),
    url(r'^interactions/set_attributes[/]', views.SetAttributes.as_view(), name='set-attributes'),
]
