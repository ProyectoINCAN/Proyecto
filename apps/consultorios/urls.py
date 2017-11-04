from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.consultorios import views
from apps.consultorios.views import MedicoList, EvolucionPacienteList, EvolucionPacienteUpdate, \
    EvolucionPacienteCreate, HorarioMedicoList, HorarioMedicoCreate, HorarioMedicoUpdate, medico_update, \
    medico_create, cambio_password, EnfermeroList, enfermero_create, enfermero_update, AdministrativoList, \
    administrativo_create, administrativo_update, consulta_paciente_list, ConsultaCreate, \
    ConsultaDetalleContinuar, PacienteDiagnosticoCreate

urlpatterns = [
    url(r'^medico/$', login_required(MedicoList.as_view()), name='medico_listar'),
    url(r'^medico/nuevo$', login_required(medico_create), name='medico_nuevo'),
    url(r'^medico/(?P<pk>[0-9]+)/editar$', login_required(medico_update), name='medico_editar'),
    url(r'^usuario/cambio_password$', login_required(cambio_password), name='cambio_password'),

    url(r'^enfermero/$', login_required(EnfermeroList.as_view()), name='enfermero_listar'),
    url(r'^enfermero/nuevo$', login_required(enfermero_create), name='enfermero_nuevo'),
    url(r'^enfermero/(?P<pk>[0-9]+)/editar$', login_required(enfermero_update), name='enfermero_editar'),

    url(r'^administrativo/$', login_required(AdministrativoList.as_view()), name='administrativo_listar'),
    url(r'^administrativo/nuevo$', login_required(administrativo_create), name='administrativo_nuevo'),
    url(r'^administrativo/(?P<pk>[0-9]+)/editar$', login_required(administrativo_update), name='administrativo_editar'),

    url(r'^horario_medico/$', login_required(HorarioMedicoList.as_view()), name='horario_medico_listar'),
    url(r'^horario_medico/nuevo$', login_required(HorarioMedicoCreate.as_view()), name='horario_medico_nuevo'),
    url(r'^horario_medico/(?P<pk>[0-9]+)/editar$', login_required(HorarioMedicoUpdate.as_view()),
        name='horario_medico_editar'),

    url(r'^consulta/evolucion_paciente/$', login_required(EvolucionPacienteList.as_view()), name='evolucion_paciente_listar'),  #TODO | agregar id del paciente en URL
    url(r'^evolucion_paciente/nuevo$', login_required(EvolucionPacienteCreate.as_view()),
        name='evolucion_paciente_nuevo'),
    url(r'^evolucion_paciente/(?P<pk>[0-9]+)/editar$', login_required(EvolucionPacienteUpdate.as_view()),              #TODO | cuando se termine agendamiento
        name='evolucion_paciente_editar'),
    url(r'^medico_especialidad/(?P<id_medico>\d+)$', views.medico_especialidad, name='medico_especialidad'),
    url(r'^medico_turno/(?P<id_medico>\d+)$', views.medico_turno, name='medico_turno'),
    url(r'^horario_medico/(?P<id_medico>\d+)/(?P<codigo_turno>[\w\-]+)/$', views.horario_medico, name='horario_medico'),
    url(r'^consulta/(?P<consulta_id>\d+)$', login_required(consulta_paciente_list), name='consulta_detalle'),
    url(r'^consulta/create/(?P<agenda_id>\d+)$', ConsultaCreate.as_view(), name='consulta'),

    url(r'^ordenes_estudio/$', views.OrdenEstudioListGlobal.as_view(), name='ordenes_estudio'),
    url(r'^ordenes_estudio/crear/$', views.OrdenEstudioCreateGlobal.as_view(), name='orden_estudio_crear'),
    url(r'^ordenes_estudio/(?P<orden_id>\d+)/eliminar/$', views.OrdenEstudioDeleteGlobal.as_view(),
        name='orden_estudio_eliminar'),
    url(r'^ordenes_estudio/(?P<orden_id>\d+)/editar/$', views.OrdenEstudioUpdateGlobal.as_view(),
        name='orden_estudio_editar'),
    url(r'^ordenes_estudio/(?P<orden_id>\d+)/detalle/listar/$', views.OrdenEstudioDetalleListGlobal.as_view(),
        name='orden_estudio_detalle_list'),
    url(r'^ordenes_estudio/(?P<orden_id>\d+)/detalle/crear/$', views.OrdenEstudioDetalleCreate.as_view(),
        name='orden_estudio_detalle_crear'),
    url(r'^ordenes_estudio/detalle/(?P<detalle_id>\d+)/eliminar$', views.OrdenEstudioDetalleDeleteGlobal.as_view(),
        name='orden_estudio_detalle_eliminar'),
    url(r'^ordenes_estudio/detalle/(?P<detalle_id>\d+)/editar$', views.OrdenEstudioDetalleUpdateGlobal.as_view(),
        name='orden_estudio_detalle_editar'),


    url(r'^consultas_dia/$', views.ConsultasDia.as_view(), name='consultas_dia'),
    url(r'^consulta/(?P<consulta_id>\d+)/detalles/$', views.ConsultaDetalleDia.as_view(), name='consulta_detalle_dia'),
    url(r'^consulta/(?P<consulta_id>\d+)/detalle/iniciar/$',
        views.ConsultaDetalleIniciar.as_view(), name='consulta_detalle_iniciar'),

    # url(r'^consulta/detalle/(?P<detalle_id>\d+)/diagnostico/list/$', views.ConsultaDetalleDiagnosticoList.as_view(),
    #     name='consulta_diagnostico_crear'),
    url(r'^consulta/detalle/(?P<detalle_id>\d+)/diagnostico/crear/$', views.PacienteDiagnosticoCreate.as_view(),
        name='consulta_diagnostico_crear'),
    url(r'^consulta/detalle/diagnostico/(?P<diagnostico_id>\d+)/$', views.PacienteDiagnosticoEditar.as_view(),
        name='consulta_diagnostico_editar'),
    url(r'^consulta/detalle/diagnostico/(?P<diagnostico_id>\d+)/eliminar$', views.PacienteDiagnosticoEliminar.as_view(),
        name='consulta_diagnostico_eliminar'),
    url(r'^consulta/detalle/(?P<detalle_id>\d+)/$',
        views.ConsultaDetalleContinuar.as_view(), name='consulta_detalle_continuar'),
    url(r'^consulta/detalle/(?P<detalle_id>\d+)/orden_estudio/crear/$', views.PacienteOrdenEstudioCreate.as_view(),
        name='consulta_orden_estudio_crear'),
    url(r'^consulta/detalle/orden_estudio/(?P<orden_id>\d+)/editar/$', views.PacienteOrdenEstudioUpdate.as_view(),
        name='consulta_orden_estudio_editar'),
    url(r'^consulta/detalle/orden_estudio/(?P<orden_id>\d+)/eliminar$', views.PacienteOrdenEstudioDelete.as_view(),
        name='consulta_orden_estudio_eliminar'),
    url(r'^consulta/detalle/(?P<detalle_id>\d+)/prescripcion/crear/$', views.PacientePrescripcionCreate.as_view(),
        name='consulta_prescripcion_crear'),
    url(r'^consulta/detalle/prescripcion/(?P<prescripcion_id>\d+)/editar/$', views.PacientePrescripcionUpdate.as_view(),
        name='consulta_prescripcion_editar'),
    url(r'^consulta/detalle/prescripcion/(?P<prescripcion_id>\d+)/eliminar$', views.PacientePrescripcionDelete.as_view(),
        name='consulta_prescripcion_eliminar'),

]
