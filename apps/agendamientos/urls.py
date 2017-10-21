from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.agendamientos.views import agenda_nuevo, agenda_especialidad, agenda_detalle_list, agenda_cancelar, \
    agenda_detalle_crear2, agenda_detalle_edit, AgendaByFechaList, agenda_by_fecha_list, PacienteByAgenda, \
    agenda_detalle_confirmar

urlpatterns = [
    # url(r'^agenda_fecha/$', login_required(AgendaByFechaList.as_view()), name='agenda_fecha_listar'),
    url(r'^agenda_fecha/$', login_required(agenda_by_fecha_list), name='agenda_fecha_listar'),
    url(r'^agenda/nuevo$', login_required(agenda_nuevo), name='agenda_nuevo'),
    #agenda_detalle
    #url(r'^agenda/(?P<agenda_id>\d+)/nuevo$', login_required(agenda_detalle_crear), name='agenda_detalle_crear'),
    url(r'^agenda/(?P<agenda_id>\d+)$', login_required(agenda_detalle_list), name='agenda_detalle'),
    url(r'^agenda/(?P<agenda_id>\d+)/(?P<agenda_detalle_id>\d+)/editar$', login_required(agenda_detalle_edit), name='agenda_editar'),
    url(r'^agenda/(?P<agenda_id>\d+)/cancelar$', login_required(agenda_cancelar), name='agenda_cancelar'),
    url(r'^agendas/$', login_required(agenda_especialidad), name='agenda_especialidad_medico'),

    url(r'^agenda/(?P<agenda_id>\d+)/paciente/listar/$', PacienteByAgenda.as_view(), name='agenda_detalle_paciente_list'),
    url(r'^agenda/(?P<agenda_id>\d+)/paciente/(?P<paciente_id>\d+)/nuevo$', login_required(agenda_detalle_crear2),
        name='agenda_detalle_crear'),

    url(r'^agenda/(?P<agenda_id>\d+)/paciente/(?P<paciente_id>\d+)/confirmar$', login_required(agenda_detalle_confirmar),
        name='agenda_detalle_confirmar'),



]