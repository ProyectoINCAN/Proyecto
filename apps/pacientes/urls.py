from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.consultorios.views import MedicoUpdate
from apps.pacientes.views import PacienteCreate, PacienteUpdate, PacienteCreate


from apps.pacientes import views as pacienteViews, views

urlpatterns = [

    #url(r'^index/$', pacienteViews.consulta, name='index'),
    url(r'^index/$', pacienteViews.DashboardAdministrativoView.as_view(), name='index'),

    url(r'^paciente/nuevo/$', login_required(PacienteCreate.as_view()), name='nuevo_paciente'),
    # url(r'^paciente/(?P<pk>\d+)/editar$', login_required(PacienteUpdate.as_view()), name='paciente_editar'),
    url(r'^paciente/(?P<pk>\d+)/editar/$', PacienteUpdate.as_view(), name='paciente_editar'),


    #dos url para eliminar, estamos usando el de la funcion y no el de la clase
    url(r'^pacientedelete/(?P<pk>\d+)$', login_required(pacienteViews.PacienteDelete.as_view()), name='paciente_delete2'),
    url(r'^paciente_delete/(?P<id_paciente>\d+)$',
        login_required(pacienteViews.paciente_delete), name='paciente_delete'),

    #abre la vista de direcciones del paciente
    url(r'^paciente/(?P<paciente_id>\d+)/direcciones/$',
        login_required(pacienteViews.PacienteDireccionView.as_view()), name='paciente_direccion'),
    url(r'^paciente/direccion/(?P<direccion_id>\d+)/eliminar$',
        login_required(pacienteViews.PacienteDireccionDelete.as_view()), name='paciente_direccion_eliminar'),
    #abre la url para agregar una nueva direccion
    url(r'^direccion/nuevo/(?P<paciente_id>\d+)$', login_required(pacienteViews.crear_direccion), name='crear_direccion'),
    url(r'^paciente/direccion/(?P<direccion_id>\d+)/editar/$',
        pacienteViews.PacienteDireccionUpdate.as_view(), name='paciente_direccion_editar'),


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

    url(r'^paciente/(?P<paciente_id>\d+)/correo_electronico/nuevo$',
        pacienteViews.PacienteCorreoElectronicoCreate.as_view(), name='paciente_correo_electronico_crear'),
    url(r'^paciente/correo_electronico/(?P<correo_id>\d+)/editar/$',
        pacienteViews.PacienteCorreoElectronicoUpdate.as_view(), name='paciente_correo_electronico_editar'),
    url(r'^paciente/correo_electronico/(?P<correo_id>\d+)/eliminar/$',
        pacienteViews.PacienteCorreoElectronicoDelete.as_view(), name='paciente_correo_electronico_eliminar'),



    url(r'^paciente/(?P<paciente_id>\d+)/padre/crear$', pacienteViews.paciente_padre_crear,
        name='padre_crear'),
    url(r'^paciente/(?P<paciente_id>\d+)/madre/crear$', pacienteViews.paciente_madre_crear,
        name='madre_crear'),
    url(r'^paciente/padre/(?P<pk>[0-9]+)/editar/$',
        pacienteViews.PacientePadreUpdate.as_view(), name='paciente_padre_editar'),

    url(r'^paciente/madre/(?P<pk>[0-9]+)/editar/$',
        pacienteViews.PacienteMadreUpdate.as_view(), name='paciente_madre_editar'),

    url(r'^paciente/(?P<id_paciente>\d+)/padre/list$',
        pacienteViews.PacientePadreList.as_view(), name='paciente_padre_listar'),

    url(r'^paciente/padre/(?P<padre_id>\d+)/eliminar$', views.PacientePadreDelete.as_view(),
        name='paciente_padre_eliminar'),

    url(r'^paciente/(?P<id_paciente>\d+)/madre/list$',
        pacienteViews.PacienteMadreList.as_view(), name='paciente_madre_listar'),
    url(r'^paciente/madre/(?P<madre_id>\d+)/eliminar$', views.PacienteMadreDelete.as_view(),
        name='paciente_madre_eliminar'),

    url(r'^distrito/(?P<paciente_id>\d+)$', pacienteViews.distrito, name='distrito'),

    url(r'^agenda/(?P<agenda_id>\d+)/(?P<origen>\d+)/paciente/nuevo/$',
        pacienteViews.PacienteCreateByAgenda.as_view(), name='agenda_paciente_crear'),

    # # vivienda del paciente
    url(r'^paciente/(?P<paciente_id>\d+)/antedecentes_socio_economicos/$',
        pacienteViews.PacienteAntecedentesView.as_view(), name='paciente_antedecentes_socio_economicos'),

    url(r'^paciente/(?P<paciente_id>\d+)/vivienda/nuevo$',
        pacienteViews.PacienteViviendaCreate.as_view(), name='paciente_vivienda_crear'),

    url(r'^paciente/vivienda/(?P<vivienda_id>\d+)/editar/$',
        pacienteViews.PacienteViviendaUpdate.as_view(), name='paciente_vivienda_editar'),
    url(r'^paciente/vivienda/(?P<vivienda_id>\d+)/eliminar/$',
        pacienteViews.PacienteViviendaDelete.as_view(), name='paciente_vivienda_eliminar'),

    url(r'^paciente/(?P<paciente_id>\d+)/servicio_sanitario/nuevo$',
        pacienteViews.PacienteServiciosSanitariosCreate.as_view(), name='paciente_servicio_sanitario_crear'),
    url(r'^paciente/servicio_sanitario/(?P<servicio_id>\d+)/editar/$',
        pacienteViews.PacienteServiciosSanitariosUpdate.as_view(), name='paciente_servicio_sanitario_editar'),
    url(r'^paciente/servicio_sanitario/(?P<servicio_id>\d+)/eliminar/$',
        pacienteViews.PacienteServiciosSanitarioDelete.as_view(), name='paciente_servicio_sanitario_eliminar'),

    url(r'^paciente/(?P<paciente_id>\d+)/servicios_basicos/nuevo$',
        pacienteViews.PacienteServiciosBasicosCreate.as_view(), name='paciente_servicios_basicos_crear'),
    url(r'^paciente/servicios_basicos/(?P<servicio_id>\d+)/editar/$',
        pacienteViews.PacienteServiciosBasicosUpdate.as_view(), name='paciente_servicios_basicos_editar'),
    url(r'^paciente/servicios_basicos/(?P<servicio_id>\d+)/eliminar/$',
        pacienteViews.PacienteServiciosBasicosDelete.as_view(), name='paciente_servicios_basicos_eliminar'),

    url(r'^paciente/(?P<paciente_id>\d+)/acompanhante/$',
        pacienteViews.PacienteAcompanhanteView.as_view(), name='paciente_acompanhante'),
    url(r'^paciente/(?P<paciente_id>\d+)/acompanhante/nuevo$',
        pacienteViews.PacienteAcompañanteCreate.as_view(), name='paciente_acompanhante_crear'),
    url(r'^paciente/acompanhante/(?P<acompanhante_id>\d+)/editar/$',
        pacienteViews.PacienteAcompanhanteUpdate.as_view(), name='paciente_acompanhante_editar'),
    url(r'^paciente/acompanhante/(?P<acompanhante_id>\d+)/eliminar/$',
        pacienteViews.PacienteAcompañanteDelete.as_view(), name='paciente_acompanhante_eliminar'),



]