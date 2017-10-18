from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.consultorios import views
from apps.consultorios.views import MedicoList, EvolucionPacienteList, EvolucionPacienteUpdate, \
    EvolucionPacienteCreate, HorarioMedicoList, HorarioMedicoCreate, HorarioMedicoUpdate, medico_update, \
    medico_create, cambio_password, EnfermeroList, enfermero_create, enfermero_update, AdministrativoList, \
    administrativo_create, administrativo_update, consulta_paciente_list

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

    url(r'^evolucion_paciente/$', login_required(EvolucionPacienteList.as_view()), name='evolucion_paciente_listar'),  #TODO | agregar id del paciente en URL
    url(r'^evolucion_paciente/nuevo$', login_required(EvolucionPacienteCreate.as_view()),
        name='evolucion_paciente_nuevo'),
    url(r'^evolucion_paciente/(?P<pk>[0-9]+)/editar$', login_required(EvolucionPacienteUpdate.as_view()),              #TODO | cuando se termine agendamiento
        name='evolucion_paciente_editar'),
    url(r'^medico_especialidad/(?P<id_medico>\d+)$', views.medico_especialidad, name='medico_especialidad'),
    url(r'^medico_turno/(?P<id_medico>\d+)$', views.medico_turno, name='medico_turno'),
    url(r'^horario_medico/(?P<id_medico>\d+)/(?P<codigo_turno>[\w\-]+)/$', views.horario_medico, name='horario_medico'),
    url(r'^consulta/(?P<consulta_id>\d+)$', login_required(consulta_paciente_list), name='consulta_detalle'),

]
