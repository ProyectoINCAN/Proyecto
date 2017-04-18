from django.conf.urls import url

from apps.pacientes.views import index,PacienteCreate, paciente_crear

urlpatterns = [
    url(r'^hola$', index, name='index'),
    #url(r'^nueva_persona$', PacienteCreate.as_view(),name='nueva_persona'),
    url(r'^nuevo_paciente$', paciente_crear ,name='nuevo_paciente'),

]