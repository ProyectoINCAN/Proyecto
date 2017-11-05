from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core import serializers
from django.http.response import JsonResponse
from django.db import connection
import json
from django.core import serializers
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render
from django.db.models.deletion import ProtectedError

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, View

from datetime import date

from apps.agendamientos.models import Agenda, AgendaDetalle, EstadoAgenda
from apps.consultorios.forms import MedicoForm, UserForm, EvolucionPacienteModelForm, HorarioMedicoModelForm, \
    EnfermeroForm, AdministrativoForm, OrdenEstudioForm, OrdenEstudioDetalleForm, DiagnosticoPacienteForm, \
    OrdenEstudioPacienteForm, PrescripcionPacienteForm
from apps.consultorios.models import *
from apps.pacientes.models import Paciente
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.internaciones.models import Diagnostico


class MedicoList(ListView):
    print("llegamos al list de medico")
    model = Medico
    template_name = 'consultorios/medico_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super(MedicoList, self).get_context_data(**kwargs)
    #     pk = self.kwargs.get('pk', 3)
    #     print("pk medico "+str(pk))
    #     medico = self.model.objects.get(id=pk)
    #     context['especialidad'] = Especialidad.objects.raw("""
    #                                 select string_agg(e.nombre, ', ') as especialidades
    #                                 from consultorios_medico m
    #                                 join consultorios_medico_especialidad me on m.id = me.medico_id
    #                                 join consultorios_especialidad e on me.especialidad_id = e.id
    #                                 where m.id = %d
    #                             """, medico.id)


@transaction.atomic
def medico_create(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos guardados correctamente.")
            return redirect('consultorios:medico_listar')
        else:
            messages.error(request, "Ha ocurrido un error. Datos no guardados.")
            return redirect('consultorios:medico_listar')
    else:
        form = MedicoForm()
    contexto = {'form': form}
    return render(request, 'consultorios/medico_form.html', contexto)


@transaction.atomic
def medico_update(request, pk):
    objeto = Medico.objects.get(id=pk)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=objeto)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente.")
            return redirect("consultorios:medico_listar")
    else:
        form = MedicoForm(instance=objeto)
    contexto = {'form': form}
    return render(request, 'consultorios/medico_form.html', contexto)


class EnfermeroList(ListView):
    model = Enfermero
    template_name = 'consultorios/enfermero_list.html'


@transaction.atomic
def enfermero_create(request):
    if request.method == 'POST':
        form = EnfermeroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos guardados correctamente.")
            return redirect('consultorios:enfermero_listar')
        else:
            messages.error(request, "Ha ocurrido un error. Datos no guardados.")
            return redirect('consultorios:enfermero_listar')
    else:
        form = EnfermeroForm()
    contexto = {'form': form}
    return render(request, 'consultorios/enfermero_form.html', contexto)


@transaction.atomic
def enfermero_update(request, pk):
    objeto = Enfermero.objects.get(id=pk)
    if request.method == 'POST':
        form = EnfermeroForm(request.POST, instance=objeto)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente.")
            return redirect("consultorios:enfermero_listar")
    else:
        form = EnfermeroForm(instance=objeto)
    contexto = {'form': form}
    return render(request, 'consultorios/enfermero_form.html', contexto)


class AdministrativoList(ListView):
    model = Administrativo
    template_name = 'consultorios/administrativo_list.html'


@transaction.atomic
def administrativo_create(request):
    if request.method == 'POST':
        form = AdministrativoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos guardados correctamente.")
            return redirect('consultorios:administrativo_listar')
        else:
            messages.error(request, "Ha ocurrido un error. Datos no guardados.")
            return redirect('consultorios:administrativo_listar')
    else:
        form = AdministrativoForm()
    contexto = {'form': form}
    return render(request, 'consultorios/administrativo_form.html', contexto)


@transaction.atomic
def administrativo_update(request, pk):
    objeto = Administrativo.objects.get(id=pk)
    if request.method == 'POST':
        form = AdministrativoForm(request.POST, instance=objeto)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente.")
            return redirect("consultorios:administrativo_listar")
    else:
        form = AdministrativoForm(instance=objeto)
    contexto = {'form': form}
    return render(request, 'consultorios/administrativo_form.html', contexto)


def cambio_password(request):
    pass


class MedicoCreate(CreateView):
    model = Medico
    template_name = 'consultorios/medico_form.html'
    form_class = MedicoForm
    second_form_class = UserForm
    success_url = reverse_lazy('consultorios:medico_listar')

    def get_context_data(self, **kwargs):
        context = super(MedicoCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            medico = form.save(commit=False)
            user = form2.save(commit=True)
            medico.usuario = user
            medico.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))


class UserCreate(CreateView):
    model = User
    form_class = UserForm
    template_name = 'consultorios/medico_form.html'  # temporalmente para probar
    success_url = reverse_lazy('consultorios:evolucion_paciente_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


def prueba(request):
    # return render(request, 'base/base.html')
    return render(request, 'consultorios/prueba.html')


class MedicoUpdate(UpdateView):
    model = Medico
    second_model = User
    template_name = 'consultorios/medico_form.html'
    form_class = MedicoForm
    second_form_class = UserForm
    success_url = reverse_lazy('consultorios:medico_listar')

    def get_context_data(self, **kwargs):
        context = super(MedicoUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        medico = self.model.objects.get(id=pk)
        user = self.second_model.objects.get(id=medico.usuario_id)

        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=user)
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        print("request", self.request)
        print("args", self.args)
        print("kwargs", self.kwargs)
        print("POST", self.request.POST)
        self.object = self.get_object
        id_medico = kwargs['pk']
        medico = self.model.objects.get(id=id_medico)
        user = self.second_model.objects.get(id=medico.usuario.id)
        form = self.form_class(request.POST, instance=medico)
        form2 = self.second_form_class(request.POST, instance=user)
        print(form.is_valid())
        print(form2.is_valid())
        if form.is_valid() and form2.is_valid():
            print("son válidos")
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            print("NO son válidos")
            return HttpResponseRedirect(self.get_success_url())


class HorarioMedicoList(ListView):
    model = HorarioMedico
    template_name = 'consultorios/horario_medico_list.html'


class HorarioMedicoCreate(CreateView):
    model = HorarioMedico
    template_name = 'consultorios/horario_medico_form.html'
    form_class = HorarioMedicoModelForm
    success_url = reverse_lazy('consultorios:horario_medico_listar')

    def get_context_data(self, **kwargs):
        context = super(HorarioMedicoCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class HorarioMedicoUpdate(UpdateView):
    model = HorarioMedico
    template_name = 'consultorios/horario_medico_form.html'
    form_class = HorarioMedicoModelForm
    success_url = reverse_lazy('consultorios:horario_medico_listar')


class EvolucionPacienteList(ListView):
    model = EvolucionPaciente
    template_name = 'consultorios/evolucion_paciente_list.html'


class EvolucionPacienteCreate(CreateView):
    model = EvolucionPaciente
    template_name = 'consultorios/evolucion_paciente_form.html'
    form_class = EvolucionPacienteModelForm
    success_url = reverse_lazy('consultorios:evolucion_paciente_listar')

    def get_context_data(self, **kwargs):
        context = super(EvolucionPacienteCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        paciente = Paciente.objects.get(pk=1)
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            form.paciente = paciente
            evolucion = form.save(commit=False)
            evolucion.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EvolucionPacienteUpdate(UpdateView):
    model = EvolucionPaciente
    template_name = 'consultorios/evolucion_paciente_form.html'
    form_class = EvolucionPacienteModelForm
    success_url = reverse_lazy('consultorios:evolucion_paciente_listar')


def medico_especialidad(request, id_medico):
    especialidad = Especialidad.objects.filter(medico=id_medico).order_by('id')
    # print('especialidad', especialidad)
    data = serializers.serialize('json', especialidad)
    return JsonResponse(data, safe=False)


def medico_turno(request, id_medico):
    query = """select turno.*, horario.cantidad from consultorios_horariomedico horario
               join consultorios_turno turno on horario.turno_id = turno.codigo
               where horario.medico_id = %s """
    cursor = connection.cursor()
    cursor.execute(query, [id_medico])
    turnos = cursor.fetchall()
    data = turnos
    if not turnos:
        data = []
    return JsonResponse(json.dumps(data), safe=False)


def horario_medico(request, id_medico, codigo_turno):
    print('id', id_medico)
    horario_medico = HorarioMedico.objects.filter(medico=id_medico, turno=codigo_turno)
    print('horario_medico', horario_medico)
    data = serializers.serialize('json', horario_medico)
    return JsonResponse(data, safe=False)

def consulta_paciente_list(request, consulta_id):
    print("llega a consulta paciente list. consulta_id: ", consulta_id, "request: ", request)
    consulta = Consulta.objects.get(pk=consulta_id)
    consulta_detalle = ConsultaDetalle.objects.filter(consulta=consulta_id)
    # if request.method == 'GET':
    #
    # else:
    #     # form = ConsultaForm(request.POST, instance=consulta)
    #     if form.is_valid():
    #         form.save()
    contexto = {'consulta': consulta, 'consulta_detalle': consulta_detalle}
    return render(request, 'consultorios/consulta_detalle_list.html', contexto)


class OrdenEstudioListGlobal(LoginRequiredMixin, ListView):
    model = OrdenEstudio
    context_object_name = 'ordenes'
    template_name = 'consultorios/orden_estudio/orden_estudio_list.html'


class OrdenEstudioCreateGlobal(LoginRequiredMixin, CreateView):
    model=OrdenEstudio
    form_class=OrdenEstudioForm
    template_name = 'consultorios/orden_estudio/orden_estudio_form.html'

    def get_success_url(self):
        return reverse('consultorios:ordenes_estudio')


class OrdenEstudioDeleteGlobal(LoginRequiredMixin, DeleteView):
    model = OrdenEstudio
    template_name = "consultorios/orden_estudio/orden_estudio_eliminar.html"
    pk_url_kwarg = 'orden_id'
    context_object_name = 'orden'

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            # render the template with your message in the context
            # or you can use the messages framework to send the message
            print('Estado: PROTEGIDO')
            messages.error(request, 'No se puede borrar ' + self.object.nombre)
            return HttpResponseRedirect(reverse('consultorios:ordenes_estudio'))

    def get_success_url(self):
        return reverse('consultorios:ordenes_estudio')


class OrdenEstudioUpdateGlobal(LoginRequiredMixin, UpdateView):
    model = OrdenEstudio
    form_class = OrdenEstudioForm
    template_name = 'consultorios/orden_estudio/orden_estudio_editar.html'
    pk_url_kwarg = 'orden_id'

    def get_success_url(self):
        return reverse('consultorios:ordenes_estudio')


class OrdenEstudioDetalleListGlobal(LoginRequiredMixin, ListView):
    model = OrdenEstudioDetalle
    context_object_name = 'orden_detalle'
    template_name = 'consultorios/orden_estudio_detalle/orden_estudio_detalle_list.html'

    def get_queryset(self):
        return OrdenEstudioDetalle.objects.filter(orden_estudio=OrdenEstudio.objects.get(pk=self.kwargs['orden_id']))

    def get_context_data(self, **kwargs):
        context = super(OrdenEstudioDetalleListGlobal, self).get_context_data(**kwargs)
        context.update({'orden': OrdenEstudio.objects.get(pk=self.kwargs['orden_id'])})
        return context


class OrdenEstudioDetalleUpdateGlobal(LoginRequiredMixin, UpdateView):
    model = OrdenEstudioDetalle
    form_class = OrdenEstudioDetalleForm
    template_name = 'consultorios/orden_estudio_detalle/orden_estudio_detalle_editar.html'
    pk_url_kwarg = 'detalle_id'

    def get_success_url(self):
        orden_detail = OrdenEstudioDetalle.objects.get(pk=self.kwargs['detalle_id'])
        orden=OrdenEstudio.objects.get(pk=orden_detail.orden_estudio.id)
        return reverse('consultorios:orden_estudio_detalle_list', kwargs={'orden_id': orden.id })


class OrdenEstudioDetalleCreate(LoginRequiredMixin, CreateView):
    model = OrdenEstudioDetalle
    form_class = OrdenEstudioDetalleForm
    template_name = 'consultorios/orden_estudio_detalle/orden_estudio_detalle_crear.html'

    def get_success_url(self):
        return reverse('consultorios:orden_estudio_detalle_list', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrdenEstudioDetalleCreate, self).get_context_data(**kwargs)
        context.update({'orden': OrdenEstudio.objects.get(pk=self.kwargs['orden_id'])})
        return context

    def form_valid(self, form):
        detalle = form.save(commit=False)
        orden=OrdenEstudio.objects.get(pk=self.kwargs['orden_id'])
        detalle.orden_estudio = orden
        detalle.save()
        return redirect(self.get_success_url())


class OrdenEstudioDetalleDeleteGlobal(LoginRequiredMixin, DeleteView):
    model = OrdenEstudio
    template_name = "consultorios/orden_estudio_detalle/orden_estudio_detalle_eliminar.html"
    pk_url_kwarg = 'detalle_id'
    context_object_name = 'detalle'

    def post(self, request, *args, **kwargs):
        orden_detail=OrdenEstudioDetalle.objects.get(pk=kwargs['detalle_id'])
        orden=OrdenEstudio.objects.get(pk=orden_detail.orden_estudio.id)
        orden_detail.delete()
        return HttpResponseRedirect(reverse('consultorios:orden_estudio_detalle_list', kwargs={'orden_id': orden.id}))


class ConsultasDia(LoginRequiredMixin, TemplateView):
    """
    permite obtener todas las consultas del dia
    """
    template_name = 'consultorios/consultas_dia.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        medico = Medico.objects.get(usuario=request.user)
        #obtenemos todas las consultas del dia de hoy del medico logueado
        consultas=Consulta.objects.filter(estado='P', medico=medico, fecha=date.today())
        context.update({'medico': medico,
                        'consultas': consultas,
                        })

        return super(TemplateView, self).render_to_response(context)


class ConsultaDetalleDia(LoginRequiredMixin, TemplateView):
    """
    obtenemos los detalles de la consulta seleccionada
    """
    template_name = 'consultorios/citas_dia.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        medico = Medico.objects.get(usuario=request.user)
        consulta=Consulta.objects.get(pk=self.kwargs['consulta_id'])

        detalle = ConsultaDetalle.objects.filter(consulta=consulta)

        context.update({
                        'consulta': consulta,
                        'detalles': detalle,
                        })

        return super(TemplateView, self).render_to_response(context)


class ConsultaCreate(LoginRequiredMixin, View):
    model = Consulta

    def post(self, request, *args, **kwargs):
        agenda = Agenda.objects.get(pk=kwargs.get('agenda_id'))

        agenda.estado=EstadoAgenda.objects.get(codigo='V')
        agenda.save()
        agenda_detalle = AgendaDetalle.objects.filter(agenda=agenda)
        #obtenemos el horario medico para asignar la hora de inicio
        # horario = HorarioMedico.objects.filter(medico=agenda.medico, turno=agenda.turno, especialidad=agenda.especialidad)
        consulta = Consulta.objects.create(fecha=agenda.fecha, estado=EstadoConsulta.objects.get(codigo='P'),
                                           medico=agenda.medico, turno=agenda.turno,
                                           especialidad=agenda.especialidad)
        for det in agenda_detalle:
            ConsultaDetalle.objects.create(orden=det.orden, confirmado=det.confirmado, consulta=consulta,
                                           paciente=det.paciente, estado=EstadoConsultaDetalle.objects.get(codigo='P'))
        return HttpResponseRedirect(reverse('agendamientos:agenda_especialidad_medico'))


class ConsultaDetalleIniciar(LoginRequiredMixin, TemplateView):
    """
    permite iniciar la consulta con el primer paciente que confirmo su llegada.
    """
    template_name = 'consultorios/consulta/consulta_iniciar.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        consulta = Consulta.objects.get(pk=self.kwargs['consulta_id'])
        #obtenemos el detalle de la consulta donde el estado sea pendiente
        detalle = ConsultaDetalle.objects.filter(consulta=consulta, estado='P').first()
        #actualizamos el estado de la detalle de la consulta a "en proceso"
        #detalle.estado = EstadoConsultaDetalle.objects.get(codigo='E')
        detalle.save()

        #diagnosticos del paciente.
        diagnosticos = Diagnostico.objects.filter(paciente=detalle.paciente)
        #ordenes de estudio del paciente
        ordenes = ConsultaOrdenEstudio.objects.filter(paciente=detalle.paciente)
        # prescripciones del paciente
        prescripciones = ConsultaPrescripcion.objects.filter(paciente=detalle.paciente)

        context.update({
            'consulta': consulta,
            'detalle': detalle,
            'diagnosticos': diagnosticos,
            'ordenes': ordenes,
            'prescripciones': prescripciones,
        })
        return super(TemplateView, self).render_to_response(context)


class ConsultaDetalleContinuar(LoginRequiredMixin, TemplateView):
    """
    permite registrar las siguientes acciones de la consulta del paciente.
    Muestra el detalle de la consulta actual
    """
    template_name = 'consultorios/consulta_iniciar.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #obtenemos el detalle actual
        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        consulta = Consulta.objects.get(pk=detalle.consulta.id)
        #obtenemos el detalle de la consulta donde el estado sea en proceso

        #consultamos si el paciente ya tiene un diagnostico en la consulta actual
        if Diagnostico.objects.filter(detalle=detalle).exists():
            diagnostico = Diagnostico.objects.get(detalle=detalle)
        else:
            diagnostico = None

        context.update({
            'consulta': consulta,
            'detalle': detalle,
            'diagnostico': diagnostico,
        })
        return super(TemplateView, self).render_to_response(context)


class ConsultaDetalleDiagnosticoList(LoginRequiredMixin, TemplateView):
    """permite obtener el listado de diagnostico del paciente. Obtiene la lista completa."""
    template_name = 'consultorios/consulta_iniciar.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #obtenemos el detalle actual
        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        consulta = Consulta.objects.get(pk=detalle.consulta.id)

        #consultamos si el paciente ya tiene un diagnostico en la consulta actual
        if Diagnostico.objects.filter(detalle=detalle).exists():
            diagnostico = Diagnostico.objects.get(detalle=detalle)
        else:
            diagnostico = None

        context.update({
            'consulta': consulta,
            'detalle': detalle,
            'diagnostico': diagnostico,
        })
        return super(TemplateView, self).render_to_response(context)


class PacienteDiagnosticoCreate(LoginRequiredMixin, FormView):
    """permite registrar el diagnostico al paciente"""
    model = Diagnostico
    template_name = 'consultorios/diagnostico_paciente.html'
    pk_url_kwarg = "detalle_id"
    form_class = DiagnosticoPacienteForm

    def get_context_data(self, **kwargs):
        context = super(PacienteDiagnosticoCreate, self).get_context_data(**kwargs)
        detalle=ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        context.update({'detalle': detalle})
        return context

    def form_valid(self, form):
        """guardamos el diagnostico de la consulta del paciente(consulta detalle)"""
        diagnostico = form.save(commit=False)
        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        consulta = Consulta.objects.get(pk=detalle.consulta.id)
        diagnostico.detalle = detalle
        diagnostico.paciente = detalle.paciente
        diagnostico.medico = consulta.medico
        diagnostico.save()

        return JsonResponse({'success': True})


class PacienteDiagnosticoEditar(LoginRequiredMixin, UpdateView):
    model = Diagnostico
    template_name = 'consultorios/consulta/diagnostico_paciente_editar.html'
    pk_url_kwarg = 'diagnostico_id'
    form_class = DiagnosticoPacienteForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True})


class PacienteDiagnosticoEliminar(LoginRequiredMixin, DeleteView):
    model = Diagnostico
    template_name = "consultorios/consulta/diagnostico_paciente_eliminar.html"
    pk_url_kwarg = 'diagnostico_id'
    context_object_name = 'diagnostico'

    def post(self, request, *args, **kwargs):
        diagnostico = Diagnostico.objects.get(pk=self.kwargs['diagnostico_id'])
        diagnostico.delete()
        return JsonResponse({'success': True})


class PacienteOrdenEstudioCreate(LoginRequiredMixin, FormView):
    """permite registrar el diagnostico al paciente"""
    model = ConsultaOrdenEstudio
    template_name = 'consultorios/consulta/orden_estudio_form.html'
    pk_url_kwarg = "detalle_id"
    form_class = OrdenEstudioPacienteForm

    def get_context_data(self, **kwargs):
        context = super(PacienteOrdenEstudioCreate, self).get_context_data(**kwargs)
        detalle=ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        context.update({'detalle': detalle})
        return context

    def form_valid(self, form):
        """guardamos el diagnostico de la consulta del paciente(consulta detalle)"""
        orden_estudio = form.save(commit=False)
        consulta_detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        orden_estudio.consulta_detalle = consulta_detalle
        orden_estudio.paciente = consulta_detalle.paciente
        orden_estudio.save()

        return JsonResponse({'success': True})


class PacienteOrdenEstudioUpdate(LoginRequiredMixin, UpdateView):
    model = ConsultaOrdenEstudio
    form_class = OrdenEstudioPacienteForm
    template_name = 'consultorios/consulta/orden_estudio_editar.html'
    pk_url_kwarg = 'orden_id'
    context_object_name = 'orden'

    def form_valid(self, form):
        print("entro")
        """guardamos el diagnostico de la consulta del paciente(consulta detalle)"""
        orden=form.save()
        consulta=orden.consulta_detalle.consulta
        form.save()
        return JsonResponse({'success': True})


class PacienteOrdenEstudioDelete(LoginRequiredMixin, DeleteView):
    model = ConsultaOrdenEstudio
    template_name = "consultorios/consulta/orden_estudio_eliminar.html"
    pk_url_kwarg = 'orden_id'
    context_object_name = 'orden'

    def post(self, request, *args, **kwargs):
        orden = ConsultaOrdenEstudio.objects.get(pk=self.kwargs['orden_id'])
        orden.delete()
        return JsonResponse({'success': True})


class PacientePrescripcionCreate(LoginRequiredMixin, FormView):
    """permite registrar el diagnostico al paciente"""
    model = ConsultaPrescripcion
    template_name = 'consultorios/consulta/prescripcion_form.html'
    pk_url_kwarg = "prescripcion_id"
    form_class = PrescripcionPacienteForm

    def get_context_data(self, **kwargs):
        context = super(PacientePrescripcionCreate, self).get_context_data(**kwargs)
        detalle=ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        context.update({'detalle': detalle})
        return context

    def form_valid(self, form):
        """guardamos el diagnostico de la consulta del paciente(consulta detalle)"""
        prescripcion = form.save(commit=False)
        consulta_detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        prescripcion.paciente = consulta_detalle.paciente
        prescripcion.consulta_detalle = consulta_detalle
        prescripcion.save()

        return JsonResponse({'success': True})


class PacientePrescripcionUpdate(LoginRequiredMixin, UpdateView):
    model = ConsultaPrescripcion
    form_class = PrescripcionPacienteForm
    template_name = 'consultorios/consulta/prescripcion_editar.html'
    pk_url_kwarg = 'prescripcion_id'
    context_object_name = 'prescripcion'

    def form_valid(self, form):
        """guardamos la prescripcion de la consulta del paciente(consulta detalle)"""
        form.save()
        return JsonResponse({'success': True})


class PacientePrescripcionDelete(LoginRequiredMixin, DeleteView):
    model = ConsultaPrescripcion
    template_name = "consultorios/consulta/prescripcion_eliminar.html"
    pk_url_kwarg = 'prescripcion_id'
    context_object_name = 'prescripcion'

    def post(self, request, *args, **kwargs):
        orden = ConsultaPrescripcion.objects.get(pk=self.kwargs['prescripcion_id'])
        orden.delete()
        return JsonResponse({'success': True})
