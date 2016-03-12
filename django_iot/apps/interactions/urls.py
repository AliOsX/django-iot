from django.conf.urls import url
from django_iot.apps.interactions import views


urlpatterns = [
    url(r'^set_status[/]', views.SetStatus.as_view(), name='set-status'),
    url(r'^refresh[/]', views.Refresh.as_view(), name='refresh'),
    url(r'^set_color[/]', views.SetColor.as_view(), name='set-color'),
]
