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


    #seguro medico del paciente
    url(r'^paciente/(?P<paciente_id>\d+)/seguro_medico/crear/$',
        pacienteViews.PacienteOtrosDatosView.as_view(), name='paciente_seguro_medico'),
    url(r'^paciente/(?P<paciente_id>\d+)/seguro_medico/nuevo$',
        pacienteViews.PacienteSeguroMedicoCreate.as_view(), name='paciente_seguro_medico_crear'),
    url(r'^paciente/seguro_medico/(?P<seguro_id>\d+)/editar/$',
        pacienteViews.PacienteSeguroMedicoUpdate.as_view(), name='paciente_seguro_medico_editar'),
    url(r'^paciente/seguro_medico/(?P<seguro_id>\d+)/eliminar/$',
        pacienteViews.PacienteSeguroMedicoDelete.as_view(), name='paciente_seguro_medico_eliminar'),


    url(r'^paciente/(?P<paciente_id>\d+)/situacion_laboral/crear$',
        pacienteViews.PacienteSituacionLaboralCreate.as_view(), name='paciente_situacion_laboral_crear'),
    url(r'^paciente/situacion_laboral/(?P<ocupacion_id>\d+)/editar$',
        pacienteViews.PacienteSituacionLaboralUpdate.as_view(), name='paciente_situacion_laboral_editar'),
    url(r'^paciente/situacion_laboral/(?P<ocupacion_id>\d+)/eliminar$',
        pacienteViews.PacienteSituacionLaboralDelete.as_view(), name='paciente_situacion_laboral_eliminar'),

    url(r'^paciente/(?P<paciente_id>\d+)/nivel_educativo/crear$',
        pacienteViews.PacienteNivelEducativoCreate.as_view(), name='paciente_nivel_educativo_crear'),
    url(r'^paciente/nivel_educativo/(?P<educacion_id>\d+)/editar$',
        pacienteViews.PacienteNivelEducativoUpdate.as_view(), name='paciente_nivel_educativo_editar'),
    url(r'^paciente/nivel_educativo/(?P<educacion_id>\d+)/eliminar/$',
        pacienteViews.PacienteNivelEducativoDelete.as_view(), name='paciente_nivel_educativo_eliminar'),


    url(r'^buscar/$', login_required(pacienteViews.PacienteBuscar.as_view()), name='buscar'),
    url(r'^autocomplete_nombres/$', login_required(pacienteViews.autocomplete_nombres), name='autocomplete_nombres'),



    url(r'^paciente/(?P<paciente_id>\d+)/padre/crear$', pacienteViews.paciente_padre_crear,
        name='padre_crear'),
    url(r'^paciente/(?P<paciente_id>\d+)/madre/crear$', pacienteViews.paciente_madre_crear,
        name='madre_crear'),

    url(r'^distrito/(?P<paciente_id>\d+)$', pacienteViews.distrito, name='distrito'),
]