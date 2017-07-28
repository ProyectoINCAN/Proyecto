from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.consultorios.views import MedicoCreate, prueba, MedicoList, MedicoUpdate,\
    EvolucionPacienteList, EvolucionPacienteUpdate, EvolucionPacienteCreate, HorarioMedicoList, HorarioMedicoCreate, \
    HorarioMedicoUpdate

urlpatterns = [
    url(r'^medico/$', login_required(MedicoList.as_view()), name='medico_listar'),
    url(r'^medico/nuevo$', login_required(MedicoCreate.as_view()), name='medico_nuevo'),
    url(r'^medico/(?P<pk>[0-9]+)/editar$', login_required(MedicoUpdate.as_view()), name='medico_editar'),

    url(r'^horario_medico/$', login_required(HorarioMedicoList.as_view()), name='horario_medico_listar'),
    url(r'^horario_medico/nuevo$', login_required(HorarioMedicoCreate.as_view()), name='horario_medico_nuevo'),
    url(r'^horario_medico/(?P<pk>[0-9]+)/editar$', login_required(HorarioMedicoUpdate.as_view()),
        name='horario_medico_editar'),

    url(r'^evolucion_paciente/$', login_required(EvolucionPacienteList.as_view()), name='evolucion_paciente_listar'),  #TODO | agregar id del paciente en URL
    url(r'^evolucion_paciente/nuevo$', login_required(EvolucionPacienteCreate.as_view()),
        name='evolucion_paciente_nuevo'),
    url(r'^evolucion_paciente/(?P<pk>[0-9]+)/editar$', login_required(EvolucionPacienteUpdate.as_view()),              #TODO | cuando se termine agendamiento
        name='evolucion_paciente_editar'),

]
