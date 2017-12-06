from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.agendamientos.views import agenda_nuevo, agenda_especialidad, agenda_detalle_list, agenda_cancelar, \
    agenda_detalle_crear2, agenda_detalle_edit, AgendaByFechaList, PacienteByAgenda, \
    agenda_detalle_confirmar, AgendaDetalleListPDF, AgendaNuevaCreateView

urlpatterns = [
    url(r'^agenda_fecha/$', AgendaByFechaList.as_view(), name='agenda_fecha_listar'),
    url(r'^agenda/(?P<origen>\d+)/nuevo$', AgendaNuevaCreateView.as_view(), name='agenda_nuevo'),
    url(r'^agenda/(?P<agenda_id>\d+)/(?P<origen>\d+)/$', login_required(agenda_detalle_list), name='agenda_detalle'),
    url(r'^agenda/(?P<agenda_id>\d+)/(?P<agenda_detalle_id>\d+)/editar$', login_required(agenda_detalle_edit),
        name='agenda_editar'),
    url(r'^agenda/(?P<agenda_id>\d+)/(?P<origen>\d+)/cancelar$', login_required(agenda_cancelar),
        name='agenda_cancelar'),
    url(r'^agendas/$', login_required(agenda_especialidad), name='agenda_especialidad_medico'),

    url(r'^agenda/(?P<agenda_id>\d+)/paciente/listar/(?P<origen>\d+)/$', PacienteByAgenda.as_view(),
        name='agenda_detalle_paciente_list'),
    url(r'^agenda/(?P<agenda_id>\d+)/paciente/(?P<paciente_id>\d+)/(?P<origen>\d+)/nuevo$',
        login_required(agenda_detalle_crear2), name='agenda_detalle_crear'),

    url(r'^agenda/(?P<agenda_id>\d+)/paciente/(?P<paciente_id>\d+)/(?P<origen>\d+)/confirmar$',
        login_required(agenda_detalle_confirmar), name='agenda_detalle_confirmar'),

    url(r'^agenda/(?P<agenda_id>\d+)/pdf', login_required(AgendaDetalleListPDF.as_view()), name='agenda_detalle_pdf'),
]
