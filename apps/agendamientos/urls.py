from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.agendamientos.views import index, agenda_nuevo, agenda_delete, AgendaDetalleList, \
     AgendaList, AgendaDetalleUpdate, AgendaDetalleDelete, \
    agendaDetalleDelete, AgendaUpdate, AgendaDetalleCreate, agenda_especialidad, agenda_detalle_list, agenda_cancelar, \
    agenda_detalle_crear, agenda_detalle_edit

urlpatterns = [
    url(r'^index$', index, name='index'),
    url(r'^agenda/nuevo$', login_required(agenda_nuevo), name='agenda_nuevo'),
    # url(r'^agendas', AgendaList.as_view(), name='agenda_listar'),
    # url(r'^agenda/(?P<pk>[0-9]+)/editar$', AgendaUpdate.as_view(), name='agenda_editar'),
    #agenda_detalle
    # url(r'^agendaDetalle/listar$', AgendaDetalleList.as_view(), name='agenda_detalle_listar'),
    url(r'^agendaDetalle/$', AgendaDetalleList.as_view(), name='agenda_detalle_listar'),
    # url(r'^agendaDetalle/nuevo$', AgendaDetalleCreate.as_view(), name='agenda_detalle_crear'),
    # url(r'^agendaDetalle/nuevo$', AgendaDetalleCreate.as_view(), name='agenda_detalle_crear'),
    # url(r'^agendaDetalle/(?P<pk>\d+)/prueba/$', DetallesAgendas.as_view(), name='agenda_detalle'),

    # url(r'^agendaDetalle/nuevo$', agendaDetalleCreate.a, name='agenda_detalle_crear'),

    url(r'^agendaDetalle/eliminar/(?P<agenda_detalle_id>\d+)/$', agendaDetalleDelete, name='agenda_detalle_eliminar'),
    #prueba

    # url(r'^agenda/([\w-]+)$', AgendaAgendaDetalleList.as_view(), name='agenda_detalle'),
    # url(r'^agenda/(?P<agenda_id>\d+)/nuevo$', AgendaDetalleCreate.as_view(), name='agenda_detalle_crear'),
    url(r'^agenda/(?P<agenda_id>\d+)$', login_required(agenda_detalle_list), name='agenda_detalle'),
    url(r'^agenda/(?P<agenda_id>\d+)/nuevo$', login_required(agenda_detalle_crear), name='agenda_detalle_crear'),
    url(r'^agenda/(?P<agenda_id>\d+)/(?P<agenda_detalle_id>\d+)/editar$', login_required(agenda_detalle_edit), name='agenda_editar'),
    # url(r'^agenda/(?P<agenda_id>\d+)/nuevo$', agenda_detalle_crear, name='agenda_detalle_crear'),
    url(r'^agenda/(?P<agenda_id>\d+)/cancelar$', login_required(agenda_cancelar), name='agenda_cancelar'),
    # url(r'^agenda/([\w-]+)/(?P<pk>\d+)/$', AgendaDetalleUpdate.as_view(), name='agenda_detalle_editar'),
    #agenda especialidad
    # url(r'^agendaEspecialidad/([\w-]+)/$', agenda_especialidad, name='agenda_especialidad'),
    url(r'^agendas/$', login_required(agenda_especialidad), name='agenda_especialidad_medico'),


]