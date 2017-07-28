from django.conf.urls import url

from apps.agendamientos.views import index, agenda_nuevo, agenda_delete, AgendaDetalleList, \
    AgendaDetalleCreate, AgendaList, AgendaDetalleUpdate, AgendaDetalleDelete, AgendaAgendaDetalleList, \
    agendaDetalleDelete, agendaDetalleCreate, AgendaUpdate

urlpatterns = [
    url(r'^index$', index, name='index'),
    url(r'^agenda/nuevo$', agenda_nuevo, name='nuevo'),
    url(r'^agendas', AgendaList.as_view(), name='agenda_listar'),
    url(r'^agenda/(?P<pk>[0-9]+)/editar$', AgendaUpdate.as_view(), name='agenda_editar'),
    url(r'^agenda/(?P<pk>[0-9]+)/eliminar$', agenda_delete, name='agenda_eliminar'),
    #agenda_detalle
    # url(r'^agendaDetalle/listar$', AgendaDetalleList.as_view(), name='agenda_detalle_listar'),
    url(r'^agendaDetalle/$', AgendaDetalleList.as_view(), name='agenda_detalle_listar'),
    #url(r'^agendaDetalle/nuevo$', AgendaDetalleCreate.as_view(), name='agenda_detalle_crear'),

    url(r'^agendaDetalle/nuevo$', agendaDetalleCreate, name='agenda_detalle_crear'),
    url(r'^agendaDetalle/editar/(?P<pk>\d+)/$', AgendaDetalleUpdate.as_view(), name='agenda_detalle_editar'),
    url(r'^agendaDetalle/eliminar/(?P<agenda_detalle_id>\d+)/$', agendaDetalleDelete, name='agenda_detalle_eliminar'),
    #prueba
    url(r'^agendaDetalle/([\w-]+)/$', AgendaAgendaDetalleList.as_view(), name='agenda_detalle'),
]