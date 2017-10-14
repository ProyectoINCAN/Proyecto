from django.conf.urls import url

from apps.internaciones.views import *

urlpatterns = [
    url(r'^tipo_medicamento/$', TipoMedicamentoListView.as_view(), name='tipo_medicamento'),
    url(r'^tipo_medicamento/crear/$', TipoMedicamentoCreateView.as_view(), name='tipo_medicamento_crear'),
    url(r'^tipo_medicamento/(?P<tipo_id>\d+)/editar$',
        TipoMedicamentoUpdateView.as_view(), name='tipo_medicamento_editar'),
    url(r'^tipo_medicamento/(?P<tipo_id>\d+)/eliminar$',
        TipoMedicamentoDelete.as_view(), name='tipo_medicamento_eliminar'),
]