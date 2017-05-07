from django.conf.urls import url

from apps.pacientes.views import index,PacienteCreate, paciente_crear, PacienteUpdate, PacienteCallCenterCreate

from apps.pacientes import views as pacienteViews

urlpatterns = [
    url(r'^hola$', index, name='hola'),

    #usar la vista basada en funcion paciente_crear
    # url(r'^nueva_persona$', pacienteViews.PacienteCreate.as_view(),name='nueva_persona'),
    # url(r'^nuevo_paciente$', paciente_crear ,name='nuevo_paciente'),
    url(r'^nuevo_paciente$', PacienteCallCenterCreate.as_view(),name='nuevo_paciente'),
    url(r'^pacientedit/(?P<pk>\d+)$', pacienteViews.PacienteUpdate.as_view(),name='paciente_edit'),


    #dos url para eliminar, estamos usando el de la funcion y no el de la clase
    url(r'^pacientedelete/(?P<pk>\d+)$', pacienteViews.PacienteDelete.as_view(),name='paciente_delete2'),
    url(r'^paciente_delete/(?P<id_paciente>\d+)$', pacienteViews.paciente_delete,name='paciente_delete'),

    url(r'^paciente_direccion/(?P<paciente_id>\d+)$', pacienteViews.paciente_direccion, name='paciente_direccion'),
    url(r'^paciente_nivel_educativo/(?P<paciente_id>\d+)$', pacienteViews.paciente_nivel_educativo, name='paciente_nivel_educatvo'),

    url(r'^index/$', pacienteViews.consulta, name='index'),
    url(r'^buscar/$', pacienteViews.PacienteBuscar.as_view(), name='buscar'),




]