from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from apps.pacientes.forms import PacienteForm, DireccionForm, NivelEducativoForm
from apps.pacientes.models import Paciente, Direccion, PacienteCallCenter

from django.contrib import  messages

# Create your views here.

def index(request):
    #return HttpResponse("Llego al index")
    return render(request, 'pacientes/index_paciente.html')

#vistas basada en funciones
def paciente_crear(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST) #llama a mi form de Paciente de Call Center
        print('oguahe koape1')
        if form.is_valid():#consulta si el formulario es valido
            print('oguahe koape')

            paciente = form.save()
            messages.success(request,'Datos Básicos grabados correctamente.!!')
            return redirect ('pacientes:paciente_direccion', paciente.id)
    else:
        form = PacienteForm()
    return  render (request, 'pacientes/paciente_form.html',{'form':form})




#vista basada en clase Paciente
class PacienteCreate(CreateView):
    '''crear un nuevo paciente con sus datos básicos'''
    model = Paciente  # indico el modelo

    #indico el formulario a utilizar
    form_class = PacienteForm

    print("llego hasta creacion de paciente")
    #luego indico el template
    template_name = 'pacientes/paciente_form.html'
    #redirijimos
    success_url = reverse_lazy('pacientes:paciente_direccion','3' )



class PacienteUpdate(UpdateView):
    '''actualizacion de los primeros datos de paciente en call center'''
    model = PacienteCallCenter
    form_class = PacienteForm

    template_name = 'pacientes/paciente_form.html'
    print("llego hasta update de paciente")
    success_url = reverse_lazy('pacientes:index')


def paciente_delete(request, id_paciente):
    '''implementacion del metodo para eliminar el registro de un paciente
    Dado que ya se registro la direccion del paciente, se realiza un delete multiple
    id_paciente = codigo del paciente'''

    paciente = PacienteCallCenter.objects.get(id=id_paciente)  #obtenemos el objeto del paciente que queremos eliminar
    #pacienteDireccion = Direccion.objects.get(paciente_id = id_paciente)
    pacienteDireccion = None
    print("paciente delete")
    if pacienteDireccion :
        if request.method == 'POST':
            pacienteDireccion.delete()
            paciente.delete()
            return redirect('pacientes:index')   #vuelve a la lista de pacientes
    else:
        paciente.delete()
        return redirect('pacientes:index')  # vuelve a la lista de pacientes
    return render(request,'pacientes/paciente_delete.html',{'paciente':paciente})
    #se redirecciona a la vista de confirmación de eliminación del paciente y se envia el contexto de dicho paciente.


class PacienteDelete(DeleteView):
    '''clase de eliminacion de paciente'''
    model = Paciente
    print("llego hasta aca")
    template_name = 'pacientes/paciente_delete.html'
    print("llego hasta eliminacion de paciente")
    success_url = reverse_lazy('pacientes:index')



def paciente_direccion(request, paciente_id):
    '''permite guardar los datos de direccion de un paciente.
       paciente_id = codigo del paciente
    '''
    if request.method == 'GET':
        form = DireccionForm()
    else:
        form = DireccionForm(request.POST, paciente_id)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.paciente_id = paciente_id
            direccion.save()
            messages.success(request, 'Direcciones del Paciente grabados correctamente.!!')
            return  redirect('pacientes:paciente_nivel_educativo', paciente_id)
    return render (request,'pacientes/paciente_direccion.html', {'form': form})

def paciente_nivel_educativo(request, paciente_id):
    '''permite guardar el registro de nivel educativo del paciente
       recibe como parametro
       paciente_id: codigo del paciente'''
    if request.method == 'GET':
        form = NivelEducativoForm()
    else:
        form = NivelEducativoForm(request.POST, paciente_id)
        if form.is_valid():
            nivelEducativo = form.save(commit=False)
            nivelEducativo.paciente_id = paciente_id
            nivelEducativo.save()
            messages.success(request, 'Nivel Educativo grabado correctamente.!!')
            return  redirect('pacientes:nuevo_paciente')
    return render (request,'pacientes/paciente_nivelEducativo.html', {'form': form})



class PacienteIndex(TemplateView):

    template_name = 'pacientes/index.html'
    #success_url = reverse_lazy('paciente:buscar')


class PacienteBuscar(TemplateView):

    template_name = 'pacientes/busqueda.html'


    def post(self,request, *args,**kwargs):

        query = request.GET['cedula','']

        if query:
            paciente = Paciente.objects.filter(nro_doc__icontains = query)
            print(paciente)
        else:
            result = []
        return render_to_response("pacientes/index.html", {"result":result, "query":query})





         #   buscar = request.POST['cedula']
        #print(buscar)
        #paciente = Paciente.objects.filter(nro_doc__icontains = request.POST['cedula'])
        #print (paciente)
        '''metodo post a la hora de realizar la busqueda'''
        #return render(request,'pacientes/busqueda.html')


def search(request):
    query = request.GET.get('cedula', '')

    if query:
        paciente = Paciente.objects.filter(nro_doc__icontains=query)
        print(paciente)
    else:
        paciente = []
    return render_to_response("pacientes/index.html", {"result": paciente, "query": query})


class PacienteView(TemplateView):
	template_name = 'pacientes/index.html'
	model = PacienteCallCenter
	def get_context_data(self, **kwargs):
		context = super(PacienteView, self).get_context_data(**kwargs)
		context['pacientes'] = PacienteCallCenter.objects.filter()
		return context




def consulta(request):
    query = request.GET.get('cedula','')
    pacientes = PacienteCallCenter.objects.filter(nro_doc__icontains = query)
    dic = {'pacientes': pacientes }
    paginator = Paginator(pacientes, 5 )

    page =request.GET.get('page')
    print(page)
    try:
        pacientes = paginator.page(page)
    except PageNotAnInteger:
        pacientes = paginator.page(1)
    except EmptyPage:
        pacientes = paginator.page(paginator.num_pages)

    return render(request,'pacientes/index.html',{'pacientes': pacientes })



