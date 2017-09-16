from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, View
from django.views.generic.list import ListView
from apps.pacientes.forms import *
from apps.pacientes.models import *
from apps.principal.common_functions import filtros_establecidos
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.edit import FormView
from django.db import connection
from django.contrib import messages
import json


def paciente_delete(request, id_paciente):
    paciente = Paciente.objects.get(id=id_paciente)
    paciente_direccion = None
    if paciente_direccion:
        if request.method == 'POST':
            paciente_direccion.delete()
            paciente.delete()
    else:
        paciente.delete()
        return redirect('pacientes:index')
    return render(request, 'pacientes/paciente_delete.html', {'paciente': paciente})


class PacienteOtrosDatosView(ListView):
    model = SeguroMedico
    template_name = "pacientes/paciente_seguro_medico.html"
    context_object_name = "seguro"

    def get_success_url(self):
        return reverse('pacientes:paciente_direccion', kwargs=self.kwargs)

    def get_datos_laborales(self):
        return PacienteOcupacion.objects.filter(paciente=self.kwargs['paciente_id'])

    def get_nivel_educativo(self):
        return PacienteNivelEducativo.objects.filter(paciente=self.kwargs['paciente_id'])

    def get_paciente(self):
        return Paciente.objects.get(pk=self.kwargs['paciente_id'])

    def get_context_data(self, **kwargs):
        context = super(PacienteOtrosDatosView, self).get_context_data(**kwargs)
        context.update({'ocupaciones': self.get_datos_laborales(),
                        'nivel_educativo': self.get_nivel_educativo(),
                        'paciente': self.get_paciente(),
                        'id_paciente': self.kwargs['paciente_id']
        })
        return context


class PacienteDelete(DeleteView):
    model = Paciente

    template_name = 'pacientes/paciente_delete.html'

    success_url = reverse_lazy('pacientes:index')


class PacienteDireccionView(FormView):
    model = Direccion
    template_name = "pacientes/paciente_direccion.html"
    pk_url_kwarg = "paciente_id"
    form_class = DireccionForm

    def get_success_url(self):
        return reverse('pacientes:paciente_direccion', kwargs=self.kwargs)

    def get_form_kwargs(self):
        kwargs = super(PacienteDireccionView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PacienteDireccionView, self).get_context_data(**kwargs)
        direcciones = Direccion.objects.filter(paciente=self.kwargs['paciente_id'])
        paciente = Paciente.objects.get(pk=self.kwargs['paciente_id'])
        context.update({
            'direcciones': direcciones,
            'id_paciente': self.kwargs['paciente_id'],
            'paciente': paciente
        })
        return context

    def post(self, request, *args, **kwargs):
        direccion = request.POST['direccion_id']
        direction = Direccion.objects.get(pk=direccion)
        direction.delete()
        return redirect(self.get_success_url())


def paciente_direccion(request, paciente_id):
    """permite guardar los datos de direccion de un paciente.
       paciente_id = codigo del paciente
    """
    if request.method == 'GET':
        direccion = Direccion.objects.filter(paciente=paciente_id)
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
        direccion = Direccion.objects.filter(paciente=paciente_id)
        contexto = {
            'direcciones': direccion,
            'id_paciente': paciente_id
        }
    return render(request, 'pacientes/paciente_direccion.html', contexto)


def crear_direccion(request, paciente_id):
    """
    metodo para crear una nueva direccion
    :param request:
    :param paciente_id: codigo de pacientes
    :return:
    """
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


def paciente_seguro_medico(request, paciente_id):
    """
    metodo que permite obtener el seguro medico del paciente.
    :param request
    :param paciente_id: codigo de paciente
    :return:
    """
    if request.method == 'GET':
        seguro = PacienteSeguroMedico.objects.filter(paciente=paciente_id)
        contexto = {
            'seguros': seguro,
            'id_paciente': paciente_id
        }
    return render(request, 'pacientes/paciente_seguro_medico.html', contexto)


def paciente_seguro_medico_crear(request, paciente_id):
    """
    metodo para cargar el formulario de seguro medico del paciente
    :param request:
    :param paciente_id:
    :return:
    """
    if request.method == 'GET':
        seguro = SeguroMedicoForm()
        contexto = {
            'form': seguro,
            'id_paciente': paciente_id
        }
    else:
        form = SeguroMedicoForm(request.POST, paciente_id)
        data = request.POST
        otro_seguro = data['nombre_seguro']
        if form.is_valid():
            seguro_paciente = form.save(commit=False)
            seguro_paciente.paciente_id = paciente_id
            seguro_paciente.detalle = otro_seguro
            seguro_paciente.save()
            return redirect('pacientes:paciente_seguro_medico', paciente_id)
    return render(request, 'pacientes/paciente_seguro_medico_crear.html', contexto)


def paciente_situacion_laboral(request, paciente_id):
    """
    permite obtener la sit
    :param request:
    :param paciente_id:
    :return:
    """
    if request.method == 'POST':
        form = PacienteOcupacionForm(request.POST, paciente_id)
        if form.is_valid():
            paciente_ocupacion = form.save(commit=False)
            paciente_ocupacion.ocupacion_id = request.POST['ocupacion']
            paciente_ocupacion.profesion_id = request.POST['profesion']
            paciente_ocupacion.paciente_id = paciente_id
            paciente_ocupacion.save()
            messages.success(request, "Situación Laboral guardado correctamente!!")
            return redirect('pacientes:padre_crear', paciente_id)

    else:
        paciente_ocupacion = PacienteOcupacion.objects.filter(paciente=paciente_id)
        if paciente_ocupacion.count() > 0:
            context = {
                'form': paciente_ocupacion,
                'id_paciente': paciente_id
            }
            return render(request, 'pacientes/paciente_situacion_laboral_listar.html', context)
        else:
            form = PacienteOcupacionForm()
    contexto = {
        'form': form,
        'id_paciente': paciente_id
    }
    return render(request, 'pacientes/paciente_situacion_laboral_crear.html', contexto)


def paciente_padre_crear(request, paciente_id):
    """
    permite insertar los datos del padre/madre del paciente
    :param request:
    :param paciente_id:
    :return:
    """

    if request.method == 'POST':
        form = PacientePadreForm(request.POST, paciente_id)
        if form.is_valid():
            padre_paciente = form.save(commit=False)
            padre_paciente.save()
            new_paciente = Paciente.objects.get(id=paciente_id)
            padre_paciente.paciente.add(new_paciente)
            messages.success(request, "Datos del Padre guardado correctamente!!")
            return redirect('pacientes:nuevo_paciente')
    else:
        paciente_padre = PacientePadre.objects.filter(paciente=paciente_id).filter(padre='on')
        if paciente_padre.exists():
            context = {
                'form': paciente_padre,
                'id_paciente': paciente_id
            }
            return render(request, 'pacientes/paciente_padre_list.html', context)
        else:
            form = PacientePadreForm()

    contexto = {
        'form': form,
        'id_paciente': paciente_id
    }
    return render(request, 'pacientes/paciente_padre_crear.html', contexto)


def paciente_madre_crear(request, paciente_id):
    """
    permite insertar los datos de la madre del paciente
    :param request:
    :param paciente_id:
    :return:
    """
    if request.method == 'POST':
        form = PacientePadreForm(request.POST, paciente_id)
        if form.is_valid():
            padre_paciente = form.save(commit=False)
            padre_paciente.padre = False
            padre_paciente.save()
            new_paciente = Paciente.objects.get(id=paciente_id)
            padre_paciente.paciente.add(new_paciente)
            messages.success(request, "Datos de la Madre guardado correctamente!!")
            return redirect('pacientes:nuevo_paciente')
    else:
        paciente_padre = PacientePadre.objects.filter(paciente=paciente_id).filter(padre=False)
        if paciente_padre.exists():
            context = {
                'form': paciente_padre,
                'id_paciente': paciente_id
            }
            return render(request, 'pacientes/paciente_padre_list.html', context)
        else:
            form = PacientePadreForm()

    contexto = {
        'form': form,
        'id_paciente': paciente_id
    }
    return render(request, 'pacientes/paciente_padre_crear.html', contexto)


def paciente_nivel_educativo(request, paciente_id):
    if request.method == 'POST':
        form = PacienteNivelEducativoForm(request.POST, paciente_id)
        if form.is_valid():
            nivel_educativo = form.save(commit=False)
            culmino = request.POST['completo']
            if culmino == "False":
                nivel_educativo.anho_cursado = request.POST['anho_cursado']

            nivel_educativo.paciente_id = paciente_id
            nivel_educativo.save()
            return redirect('pacientes:nuevo_paciente')
    else:
        paciente = PacienteNivelEducativo.objects.filter(paciente=paciente_id)
        if paciente.exists():
            contexto = {
                'form': paciente,
                'id_paciente': paciente_id
            }
            return render(request, 'pacientes/paciente_nivel_educativo_listar.html', contexto)
        else:
            form = PacienteNivelEducativoForm()
        context = {
            'form': form,
            'id_paciente': paciente_id
        }
        return render(request, 'pacientes/paciente_nivel_educativo.html', context)


class PacientePadreCreateView(FormView):
    model = PacientePadre
    form_class = PacientePadreForm
    template_name = "pacientes/paciente_padre_crear.html"

    def get_success_url(self):
        return reverse('nuevo_paciente')

    def get_context_data(self, **kwargs):
        context = super(PacientePadreCreateView, self).get_context_data(**kwargs)
        context['cliente'] = Paciente.objects.get(pk=self.kwargs['paciente_id'])
        context['id_paciente'] = self.kwargs['paciente_id']
        return context

    def get_form_kwargs(self):
        kwargs = super(PacientePadreCreateView, self).get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        paciente = Paciente.objects.get(pk=self.kwargs['paciente_id'])

        padre_paciente = form.save(commit=False)
        padre_paciente.paciente_id = paciente.id
        padre_paciente.save()


class PacienteIndex(TemplateView):

    template_name = 'pacientes/index.html'
    #success_url = reverse_lazy('paciente:buscar')


class PacienteBuscar(TemplateView):

    template_name = 'pacientes/busqueda.html'

    def post(self, request, *args,**kwargs):

        query = request.GET['cedula', '']

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


class PacienteView(TemplateView):
    template_name = 'pacientes/index.html'
    model = Paciente

    def get_context_data(self, **kwargs):
        context = super(PacienteView, self).get_context_data(**kwargs)
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
                        vendedor['id'] = r[0]
                        vendedor['label'] = r[3]+"-"+r[1]+" "+r[2]
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

    return render(request, 'pacientes/index.html',{'pacientes': pacientes })


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
        pk_paciente = self.kwargs.get('pk', 0)
        query = (
            '''
            SELECT MAX(id)
            FROM pacientes_telefono
            WHERE paciente_id =''' + pk_paciente + '''
                                            '''
        )
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
        paciente = self.second_model.objects.get(id=telefono.paciente_id)
        form = self.form_class(request.POST, instance=telefono)
        form2 = self.second_form_class(request.POST, instance=paciente)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
        return HttpResponseRedirect(self.get_success_url())


class PacienteDireccionDeleteView(View):
    """
    permite eliminar los datos de la direccion del paciente
    """
    login_url = '/'
    local_id = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        direccion = get_object_or_404(Direccion, pk=kwargs.get('direccion_id'))
        direccion.delete()
        return JsonResponse({'success': True})
