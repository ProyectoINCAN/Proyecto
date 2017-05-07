from django.conf.urls import url

from apps.agendamientos.views import index, agenda_nuevo, agenda_edit, agenda_delete, AgendaDetalleList, \
    AgendaDetalleCreate, AgendaList, AgendaDetalleUpdate, AgendaDetalleDelete, AgendaAgendaDetalleList, \
    agendaDetalleDelete, agendaDetalleCrear

urlpatterns = [
    url(r'^index$', index, name='index'),
    url(r'^nuevo$', agenda_nuevo, name='nuevo'),
    url(r'^listar', AgendaList.as_view(), name='agenda_listar'),
    url(r'^editar/(?P<id_agenda>\d+)/$', agenda_edit, name='agenda_editar'),
    url(r'^eliminar/(?P<id_agenda>\d+)/$', agenda_delete, name='agenda_eliminar'),
    #agenda_detalle
    url(r'^agendaDetalle/listar$', AgendaDetalleList.as_view(), name='agenda_detalle_listar'),
    #url(r'^agendaDetalle/nuevo$', AgendaDetalleCreate.as_view(), name='agenda_detalle_crear'),

    url(r'^agendaDetalle/nuevo$', agendaDetalleCrear, name='agenda_detalle_crear'),
    url(r'^agendaDetalle/editar/(?P<pk>\d+)/$', AgendaDetalleUpdate.as_view(), name='agenda_detalle_editar'),
    url(r'^agendaDetalle/eliminar/(?P<agenda_detalle_id>\d+)/$', agendaDetalleDelete, name='agenda_detalle_eliminar'),
    #prueba
    url(r'^agendaDetalle/([\w-]+)/$', AgendaAgendaDetalleList.as_view(), name='agenda_detalle'),
]