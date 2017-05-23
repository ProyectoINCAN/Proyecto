from django.conf.urls import url

from apps.consultorios.views import MedicoCreate, UserCreate, prueba, \
    MedicoList, Medico2Create

urlpatterns = [
    # url(r'^evolucion_paciente_list$', EvolucionPacienteList.as_view(), name='evolucion_paciente_list'),
    # url(r'^evolucion_paciente$', EvolucionPacienteCreate.as_view(), name='evolucion_paciente'),
    url(r'^medico/$', MedicoList.as_view(), name='medico_listar'),
    url(r'^medico/nuevo$', MedicoCreate.as_view(), name='medico_nuevo'),
    # url(r'^usuario/nuevo$', UserCreate.as_view(), name='usuario_nuevo'),

    url(r'^prueba', Medico2Create.as_view(), name='prueba'),
]
