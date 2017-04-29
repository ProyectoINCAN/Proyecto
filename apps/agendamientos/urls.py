from django.conf.urls import url

from apps.agendamientos.views import index, agenda_nuevo

urlpatterns = [
    url(r'^index$', index, name='index'),
    url(r'^nuevo', agenda_nuevo, name='nuevo'),
]