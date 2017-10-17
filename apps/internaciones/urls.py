from django.conf.urls import url

from apps.internaciones.views import *

urlpatterns = [
    url(r'^tipo_medicamento/$', TipoMedicamentoListView.as_view(), name='tipo_medicamento'),
    url(r'^tipo_medicamento/crear/$', TipoMedicamentoCreateView.as_view(), name='tipo_medicamento_crear'),
    url(r'^tipo_medicamento/(?P<tipo_id>\d+)/editar$',
        TipoMedicamentoUpdateView.as_view(), name='tipo_medicamento_editar'),
    url(r'^tipo_medicamento/(?P<tipo_id>\d+)/eliminar$',
        TipoMedicamentoDelete.as_view(), name='tipo_medicamento_eliminar'),

    url(r'^medicamentos/$', MedicamentoListView.as_view(), name='medicamentos'),
    url(r'^medicamento/crear/$', MedicamentoCreateView.as_view(), name='medicamento_crear'),
    url(r'^medicamento/(?P<medicamento_id>\d+)/editar$', MedicamentoUpdateView.as_view(), name='medicamento_editar'),
    url(r'^medicamento/(?P<medicamento_id>\d+)/eliminar$',
        MedicamentoDeleteView.as_view(), name='medicamento_eliminar'),
]