from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
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


#vista basada en clase
class PacienteCreate(CreateView):
    model = Paciente  # indico el modelo

    #indico el formulario a utilizar
    form_class = PacienteForm
    #luego indico el template
    template_name = 'pacientes/paciente_form.html'
    #redirijimos
    success_url = reverse_lazy('pacientes:index')

