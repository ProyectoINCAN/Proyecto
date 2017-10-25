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
from django.db.models.deletion import ProtectedError
from django.views.generic.edit import FormView
from django.db import connection
from django.contrib import messages
import json
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import calendar
from apps.agendamientos.models import Agenda

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
    """
    permite ver seguro médico, situación laboral y nivel educactivo del
    paciente seleccionado.
    """
    model = PacienteSeguroMedico
    template_name = "pacientes/seguro_medico/paciente_seguro_medico.html"
    context_object_name = "seguros"

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
        seguro = PacienteSeguroMedicoForm()
        context.update({'ocupaciones': self.get_datos_laborales(),
                        'nivel_educativo': self.get_nivel_educativo(),
                        'paciente': self.get_paciente(),
                        'id_paciente': self.kwargs['paciente_id'],
                        'form': seguro
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
        # print('direccion', direccion.)
        direction = Direccion.objects.get(pk=direccion)
        print('direccion', direction)
        direction.delete()
        return redirect(self.get_success_url())


def paciente_direccion(request, paciente_id):
    """permite guardar los datos de direccion de un paciente.
       paciente_id = codigo del paciente
    """
    if request.method == 'GET':
        direcciones = Direccion.objects.filter(paciente=paciente_id)
        direccion = DireccionForm()
        contexto = {
            'direcciones': direcciones,
            'id_paciente': paciente_id,
            'form': direccion
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

        print('prueba', form.is_valid())
        # direccion = form.save(commit=False)
        # print('prueba', direccion)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.paciente_id = paciente_id
            print('direccion', direccion)
            direccion.save()
            return redirect('pacientes:paciente_direccion', paciente_id)
    return render(request, 'pacientes/direccion.html', contexto)


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
            paciente = Paciente.objects.filter(nro_doc__icontains=query)
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

    dic = {'pacientes': pacientes}
    paginator = Paginator(pacientes, 5)

    page =request.GET.get('page', '1')
    print(page)
    try:
        pacientes = paginator.page(page)
    except PageNotAnInteger:
        pacientes = paginator.page(1)
    except EmptyPage:
        pacientes = paginator.page(paginator.num_pages)

    return render(request, 'pacientes/index.html', {'pacientes': pacientes })


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


class PacienteCreateByAgenda(LoginRequiredMixin, CreateView):
    """
    permite crear un nuevo paciente desde ventanilla de confirmacion para la agenda
    """
    model = Telefono
    template_name = 'pacientes/paciente_crear_by_agendamiento.html'
    form_class = TelefonoForm
    second_form_class = PacienteForm

    def get_success_url(self):
        return reverse('agendamientos:agenda_detalle_paciente_list', kwargs={'agenda_id': self.kwargs['agenda_id']})


    # agregamos los form al contexto
    def get_context_data(self, **kwargs):
        context = super(PacienteCreateByAgenda, self).get_context_data(**kwargs)
        context['agenda']=Agenda.objects.get(pk=self.kwargs['agenda_id'])
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


def distrito(request):
    if request.method == 'GET':
        departamento = request.GET.get('departamento', None)
        print('entro en distrito')
        data = {
            'distrito': Distrito.objects.filter(departamento=departamento)
        }
        return JsonResponse(data)


class PacienteOtrosDatosView(ListView):
    """
    permite ver seguro médico, situación laboral y nivel educactivo del
    paciente seleccionado.
    """
    model = PacienteSeguroMedico
    template_name = "pacientes/seguro_medico/paciente_seguro_medico.html"
    context_object_name = "seguros"

    def get_queryset(self):
        return PacienteSeguroMedico.objects.filter(paciente=self.kwargs['paciente_id'])

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
        seguro = PacienteSeguroMedicoForm()
        context.update({'ocupaciones': self.get_datos_laborales(),
                        'nivel_educativo': self.get_nivel_educativo(),
                        'paciente': self.get_paciente(),
                        'id_paciente': self.kwargs['paciente_id'],
                        'form': seguro
        })
        return context


class PacienteSeguroMedicoCreate(LoginRequiredMixin, CreateView):
    template_name = 'pacientes/seguro_medico/paciente_seguro_medico_crear.html'
    model = PacienteSeguroMedico
    form_class = PacienteSeguroMedicoForm

    def get_success_url(self):
        return reverse('pacientes:paciente_seguro_medico', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(PacienteSeguroMedicoCreate, self).get_context_data(**kwargs)
        paciente = Paciente.objects.get(pk=self.kwargs['paciente_id'])
        context.update({
            'paciente': paciente
        })
        return context

    def form_valid(self, form):
        detalle = form.data['detalle']
        seguro_medico = form.save(commit=False)
        seguro_medico.paciente_id = self.kwargs['paciente_id']
        seguro_medico.detalle = detalle
        seguro_medico.save()
        return JsonResponse({'success': True})


class PacienteSeguroMedicoDelete(LoginRequiredMixin, DeleteView):
    """
    permite eliminar los registros del seguro médico del paciente
    """
    model = PacienteSeguroMedico
    template_name = "pacientes/seguro_medico/paciente_seguro_medico_eliminar.html"
    pk_url_kwarg = 'seguro_id'
    context_object_name = 'seguro'

    def post(self, request, *args, **kwargs):
        paciente = Paciente.objects.get(pacienteseguromedico=kwargs['seguro_id'])

        paciente_seguro = PacienteSeguroMedico.objects.get(pk=kwargs['seguro_id'])
        paciente_seguro.delete()

        return HttpResponseRedirect(reverse('pacientes:paciente_seguro_medico',
                                            kwargs={'paciente_id': paciente.id}))


class PacienteSeguroMedicoUpdate(LoginRequiredMixin, UpdateView):
    model = PacienteSeguroMedico
    form_class = PacienteSeguroMedicoForm
    template_name = 'pacientes/seguro_medico/paciente_seguro_medico_edit.html'
    pk_url_kwarg = 'seguro_id'

    def form_valid(self, form):
        form.save()

        return JsonResponse({'success': True})


class PacienteSituacionLaboralCreate(LoginRequiredMixin, CreateView):
    template_name = 'pacientes/situacion_laboral/paciente_situacion_laboral.html'
    model = PacienteOcupacion
    form_class = PacienteOcupacionForm

    def get_success_url(self):
        return reverse('pacientes:paciente_seguro_medico', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(PacienteSituacionLaboralCreate, self).get_context_data(**kwargs)
        paciente = Paciente.objects.get(pk=self.kwargs['paciente_id'])
        context.update({
            'paciente': paciente
        })
        return context

    def form_valid(self, form):
        ocupacion = form.save(commit=False)
        ocupacion.paciente_id = self.kwargs['paciente_id']
        ocupacion.save()
        return JsonResponse({'success': True})


class PacienteSituacionLaboralDelete(LoginRequiredMixin, DeleteView):
    """
    permite eliminar los registros de las ocupaciones del paciente
    """
    model = PacienteOcupacion
    template_name = "pacientes/situacion_laboral/paciente_situacion_laboral_eliminar.html"
    pk_url_kwarg = 'ocupacion_id'
    context_object_name = 'ocupacion'

    def post(self, request, *args, **kwargs):
        """
        primero obtenemos el paciente de dicha ocupacion a eliminar y luego eliminamos el registro
        de la ocupacion seleccionada del paciente a eliminar
        :param request:
        :param args:
        :param kwargs: codigo de ocupacion
        :return:
        """
        paciente = Paciente.objects.get(pacienteocupacion=kwargs['ocupacion_id'])
        paciente_ocupacion = PacienteOcupacion.objects.get(pk=kwargs['ocupacion_id'])
        paciente_ocupacion.delete()

        return HttpResponseRedirect(reverse('pacientes:paciente_seguro_medico',
                                            kwargs={'paciente_id': paciente.id}))


class PacienteSituacionLaboralUpdate(LoginRequiredMixin, UpdateView):
    model = PacienteOcupacion
    form_class = PacienteOcupacionForm
    template_name = 'pacientes/situacion_laboral/paciente_situacion_laboral_editar.html'
    pk_url_kwarg = 'ocupacion_id'

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True})


class PacienteNivelEducativoCreate(LoginRequiredMixin, CreateView):
    template_name = 'pacientes/nivel_educativo/paciente_nivel_educativo.html'
    model = PacienteNivelEducativo
    form_class = PacienteNivelEducativoForm

    def get_success_url(self):
        return reverse('pacientes:paciente_seguro_medico', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(PacienteNivelEducativoCreate, self).get_context_data(**kwargs)
        paciente = Paciente.objects.get(pk=self.kwargs['paciente_id'])
        context.update({
            'paciente': paciente
        })
        return context

    def form_valid(self, form):
        educacion = form.save(commit=False)
        educacion.paciente_id = self.kwargs['paciente_id']
        educacion.save()
        return JsonResponse({'success': True})


class PacienteNivelEducativoDelete(LoginRequiredMixin, DeleteView):
    """
    permite eliminar los registros de los registros del nivel educativo seleccionado
    del paciente
    """
    model = PacienteNivelEducativo
    template_name = "pacientes/nivel_educativo/paciente_nivel_educativo_eliminar.html"
    pk_url_kwarg = 'educacion_id'
    context_object_name = 'educacion'

    def post(self, request, *args, **kwargs):
        paciente = Paciente.objects.get(pacienteniveleducativo=kwargs['educacion_id'])
        paciente_educacion = PacienteNivelEducativo.objects.get(pk=kwargs['educacion_id'])
        paciente_educacion.delete()

        return HttpResponseRedirect(reverse('pacientes:paciente_seguro_medico',
                                            kwargs={'paciente_id': paciente.id}))


class PacienteNivelEducativoUpdate(LoginRequiredMixin, UpdateView):
    model = PacienteNivelEducativo
    form_class = PacienteNivelEducativoForm
    template_name = 'pacientes/nivel_educativo/paciente_nivel_educativo_editar.html'
    pk_url_kwarg = 'educacion_id'

    def form_valid(self, form):
        if form.data['completo'] == 'True':
            educacion = PacienteNivelEducativo.objects.get(pk=self.kwargs['educacion_id'])
            educacion.nivel_educativo_id = form.data['nivel_educativo']
            educacion.completo = form.data['completo']
            educacion.anho_cursado = 0
            educacion.save()
        else:
            form.save()
        return JsonResponse({'success': True})


class DashboardAdministrativoView(LoginRequiredMixin, TemplateView):
    template_name = 'pacientes/index.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardAdministrativoView, self).dispatch(request, *args, *kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        pacientes = Paciente.objects.all()

        now = datetime.datetime.now()
        _, num_days = calendar.monthrange(now.year, now.month)
        first_day = datetime.date(now.year, now.month, 1)
        last_day = datetime.date(now.year, now.month, num_days)

        #pacientes registrados en el mes
        listado_mensual = Paciente.objects.filter(fecha_registrado__gte=first_day, fecha_registrado__lte=last_day)

        #pacientes registrado en el dia
        listado_diario = Paciente.objects.filter(fecha_registrado=now)
        context.update({
            'pacientes': pacientes,
            'total_pacientes': pacientes.count(),
            'mensual': listado_mensual.count(),
            'hoy': listado_diario.count()
        })
        return super(TemplateView, self).render_to_response(context)

