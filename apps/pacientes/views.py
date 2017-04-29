from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.pacientes.forms import PacienteForm
from apps.pacientes.models import Paciente

from django.contrib import  messages

# Create your views here.

def index(request):
    #return HttpResponse("Llego al index")
    return render(request, 'pacientes/index_paciente.html')

#vistas basada en funciones
def paciente_crear(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():#consulta si el formulario es valido
            print('oguahe koape')
            form.save()
            messages.success(request,'Datos Básicos grabados correctamente.!!')
            return redirect ('paciente:index')
    else:
        form = PacienteForm()
    return  render (request, 'pacientes/paciente_form.html',{'form':form})


#vista basada en clase Paciente
class PacienteCreate(CreateView):
    '''crear un nuevo paciente con sus datos básicos'''
    model = Paciente  # indico el modelo

    #indico el formulario a utilizar
    form_class = PacienteForm
    #luego indico el template
    template_name = 'pacientes/paciente_form.html'
    #redirijimos
    success_url = reverse_lazy('paciente:index')



class PacienteUpdate(UpdateView):
    '''actualizacion del paciente'''
    model = Paciente
    form_class = PacienteForm

    template_name = 'pacientes/paciente_form.html'

    success_url = reverse_lazy('paciente:index')

class PacienteDelete(DeleteView):
    '''clase de eliminacion de paciente'''
    model = Paciente
    print("llego hasta aca")
    template_name = 'pacientes/paciente_delete.html'
    success_url = reverse_lazy('paciente:index')
