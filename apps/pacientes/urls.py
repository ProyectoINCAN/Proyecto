from django.conf.urls import url

from apps.pacientes.views import index

urlpatterns = [
    url(r'^hola$', index, name='index'),
]