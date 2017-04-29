from django.conf.urls import url

from apps.pacientes.views import index,PacienteCreate, paciente_crear, PacienteUpdate

from apps.pacientes import views as pacienteViews

urlpatterns = [
    url(r'^hola$', index, name='index'),
    url(r'^nueva_persona$', pacienteViews.PacienteCreate.as_view(),name='nueva_persona'),
    #url(r'^nuevo_paciente$', paciente_crear ,name='nuevo_paciente'),
    url(r'^pacientedit/(?P<pk>\d+)$', pacienteViews.PacienteUpdate.as_view(),name='paciente_edit'),
    url(r'^pacientedelete/(?P<pk>\d+)$', pacienteViews.PacienteDelete.as_view(),name='paciente_delete'),



]