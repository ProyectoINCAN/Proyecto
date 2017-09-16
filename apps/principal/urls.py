from django.conf.urls import url

from apps.principal import views

urlpatterns = [
    url(r'^principal/distrito/(?P<pk>[0-9]+)$', views.distrito, name='distrito'),
]