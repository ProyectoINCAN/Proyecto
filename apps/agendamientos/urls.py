from django.conf.urls import url

from apps.agendamientos.views import agenda_view

urlpatterns = [
    url(r'^nuevo$', agenda_view, name='crear_agenda'),
]