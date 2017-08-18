from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from apps.pacientes.forms import PacienteForm, DireccionForm, NivelEducativoForm, TelefonoForm
from apps.pacientes.models import Paciente, Direccion, Paciente, Telefono
from apps.principal.common_functions import filtros_establecidos
from django.contrib import  messages
from django.db import connection
import json

# Create your views here.





def paciente_delete(request, id_paciente):
    '''implementacion del metodo para eliminar el registro de un paciente
    Dado que ya se registro la direccion del paciente, se realiza un delete multiple
    id_paciente = codigo del paciente'''

    paciente = Paciente.objects.get(id=id_paciente)  #obtenemos el objeto del paciente que queremos eliminar
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
        direccion = Direccion.objects.all()
        contexto = {
            'direcciones': direccion,
            'id_paciente': paciente_id
        }

    else:
        form = DireccionForm(request.POST, paciente_id)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.paciente_id = paciente_id
            direccion.save()
        direccion = Direccion.objects.all()
        contexto = {
            'direcciones': direccion,
            'id_paciente': paciente_id
        }
    return render (request,'pacientes/paciente_direccion.html', contexto )

def crear_direccion(request, paciente_id):
    '''
    metodo para crear una nueva direccion
    :param request:
    :param paciente_id: codigo de pacientes
    :return:
    '''
    if request.method == 'GET':
        direccion = DireccionForm()
        contexto = {
            'form': direccion,
            'id_paciente': paciente_id
        }

    else:
        form = DireccionForm(request.POST, paciente_id)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.paciente_id = paciente_id
            direccion.save()
            return redirect('pacientes:paciente_direccion', paciente_id)


    return render(request, 'pacientes/direccion.html', contexto)


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
            return  redirect('paciente:nuevo_paciente')
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
	model = Paciente
	def get_context_data(self, **kwargs):
		context = super(PacienteView, self).get_context_data(**kwargs)
		context['pacientes'] = Paciente.objects.filter()
		return context

def autocomplete_nombres(request):
    if request.method == 'GET':
        if request.is_ajax():
            if request.is_ajax():
                try:
                    name_paciente = request.GET['term']
                    print("term ->" + name_paciente);

                    query = (
                        '''
                        SELECT *
                        FROM pacientes_paciente
                        WHERE CONCAT (UPPER(nombres), ' ', UPPER(apellidos),' ', UPPER(nro_doc)) like UPPER('%''' + name_paciente + '''%')
                                    '''
                    )

                    cursor = connection.cursor()
                    cursor.execute(query)
                    results = cursor.fetchall()
                    lista_pacientes = []
                    for r in results:
                        vendedor = {}
                        vendedor['id']= r[0]
                        vendedor['label']= r[3]+"-"+r[1]+" "+r[2]
                        vendedor['value'] = r[1]+" "+r[2]
                        lista_pacientes.append(vendedor)
                    data = json.dumps(lista_pacientes)
                except Exception:
                    print("error de consulta");
            else:
                data = 'fail'
            mimetype = 'application/json'
            return HttpResponse(data,mimetype)
        else:
            print("debo redirigir al login")




def consulta(request):
    filtros = filtros_establecidos(request,'index_paciente')

    #significa que se ingreso el nombre del paciente
    if filtros == 1 :
        pacientes = Paciente.objects.filter(id = request.GET.get('paciente'))
    else:
        pacientes = Paciente.objects.all()

    dic = {'pacientes': pacientes }
    paginator = Paginator(pacientes, 5 )

    page =request.GET.get('page','1')
    print(page)
    try:
        pacientes = paginator.page(page)
    except PageNotAnInteger:
        pacientes = paginator.page(1)
    except EmptyPage:
        pacientes = paginator.page(paginator.num_pages)

    return render(request,'pacientes/index.html',{'pacientes': pacientes })


class PacienteCreate(CreateView):
    model = Telefono
    template_name = 'pacientes/paciente_callCenter_form.html'
    form_class = TelefonoForm
    second_form_class = PacienteForm
    success_url = reverse_lazy('pacientes:index')

    # agregamos los form al contexto
    def get_context_data(self, **kwargs):
        context = super(PacienteCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)  # TelefonoForm
        form2 = self.second_form_class(request.POST)  # PersonaForm

        print(str(form.is_valid()) + " " + str(form2.is_valid()))
        if form.is_valid() and form2.is_valid():
            telefono = form.save(commit=False)
            telefono.paciente = form2.save()
            telefono.save()
            return HttpResponseRedirect(self.get_success_url())


        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))


class PacienteUpdate(UpdateView):
    second_model = Paciente
    model = Telefono
    template_name = 'pacientes/paciente_form.html'
    form_class = TelefonoForm
    second_form_class = PacienteForm
    success_url = reverse_lazy('pacientes:index')

    def get_context_data(self, **kwargs):
        context = super(PacienteUpdate, self).get_context_data(**kwargs)
        pk_paciente = self.kwargs.get('pk',0)
        print(pk_paciente)
        query = (
            '''
            SELECT MAX(id)
            FROM pacientes_telefono
            WHERE paciente_id =''' + pk_paciente + '''
                                            '''
        )
        print(query)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for r in results:
            codigo_telefono = r[0]
        print(codigo_telefono)
        telefono = self.model.objects.get(id=codigo_telefono)
        paciente = self.second_model.objects.get(id=telefono.paciente_id)
        if 'form' not in context:
            context['form'] = self.form_class(instance=telefono)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=paciente)
            context['form'] = self.form_class(instance=telefono)
        context['id'] = codigo_telefono
        context['id_paciente'] = pk_paciente
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_paciente = kwargs['pk']
        query = (
            '''
            SELECT MAX(id)
            FROM pacientes_telefono
            WHERE paciente_id =''' + id_paciente + '''
                                                    '''
        )
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for r in results:
            id_telefono = r[0]
        telefono = self.model.objects.get(id = id_telefono)
        paciente =  self.second_model.objects.get(id = telefono.paciente_id)
        form = self.form_class(request.POST, instance = telefono)
        form2 = self.second_form_class(request.POST, instance = paciente)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
        return HttpResponseRedirect(self.get_success_url())








