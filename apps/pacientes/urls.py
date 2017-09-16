from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.consultorios.views import MedicoUpdate
from apps.pacientes.views import PacienteCreate, PacienteUpdate, PacienteCreate


from apps.pacientes import views as pacienteViews

urlpatterns = [

    url(r'^index/$', pacienteViews.consulta, name='index'),

    url(r'^nuevo_paciente$', login_required(PacienteCreate.as_view()), name='nuevo_paciente'),
    url(r'^paciente/(?P<pk>[0-9]+)/editar$', login_required(PacienteUpdate.as_view()), name='paciente_editar'),


    #dos url para eliminar, estamos usando el de la funcion y no el de la clase
    url(r'^pacientedelete/(?P<pk>\d+)$', login_required(pacienteViews.PacienteDelete.as_view()), name='paciente_delete2'),
    url(r'^paciente_delete/(?P<id_paciente>\d+)$',
        login_required(pacienteViews.paciente_delete), name='paciente_delete'),

    #abre la vista de direcciones del paciente
    url(r'^paciente/(?P<paciente_id>\d+)/direcciones/$',
        login_required(pacienteViews.PacienteDireccionView.as_view()), name='paciente_direccion'),
    url(r'^paciente/direccion/(?P<direccion_id>\d+)/eliminar$',
        login_required(pacienteViews.PacienteDireccionDeleteView.as_view()), name='paciente_direccion_eliminar'),
    #abre la url para agregar una nueva direccion
    url(r'^direccion/nuevo/(?P<paciente_id>\d+)$', login_required(pacienteViews.crear_direccion), name='crear_direccion'),
    url(r'^paciente/(?P<paciente_id>\d+)/paciente_nivel_educativo$',
      login_required(pacienteViews.paciente_nivel_educativo), name='paciente_nivel_educatvo'),

    #seguro medico del paciente
    url(r'^paciente/seguro_medico/crear/(?P<paciente_id>\d+)$',
        pacienteViews.PacienteOtrosDatosView.as_view(), name='paciente_seguro_medico'),
    url(r'^paciente/(?P<paciente_id>\d+)/seguro_medico/nuevo$',
        pacienteViews.paciente_seguro_medico_crear, name='paciente_seguro_medico_crear'),

    #situacion laboral del paciente
    url(r'^paciente/(?P<paciente_id>\d+)/situacion_laboral/crear$', pacienteViews.paciente_situacion_laboral, name='paciente_situacion_laboral'),


    url(r'^buscar/$', login_required(pacienteViews.PacienteBuscar.as_view()), name='buscar'),
    url(r'^autocomplete_nombres/$', login_required(pacienteViews.autocomplete_nombres), name='autocomplete_nombres'),

    url(r'^paciente/(?P<paciente_id>\d+)/padre/crear$', pacienteViews.paciente_padre_crear,
        name='padre_crear'),
    url(r'^paciente/(?P<paciente_id>\d+)/madre/crear$', pacienteViews.paciente_madre_crear,
        name='madre_crear'),


]