import calendar

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.db.models.aggregates import Max
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.http.response import JsonResponse
from django.db import connection
import json
from django.core import serializers
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models.deletion import ProtectedError

# Create your views here.
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, View

import datetime

from Proyecto import settings
from apps import pacientes
from apps.agendamientos.functions import get_origen_url_agendamiento
from apps.agendamientos.models import Agenda, AgendaDetalle, EstadoAgenda
from apps.consultorios.forms import *
from apps.consultorios.functions import verificar_estado_consulta
from apps.consultorios.models import *
from apps.pacientes.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.internaciones.models import Diagnostico
from django.utils.safestring import mark_safe
from apps.consultorios.helpers import calculate_age
from utils.generate_pdf import render_to_pdf


class MedicoList(ListView):
    model = Medico
    template_name = 'consultorios/medico_list.html'


@transaction.atomic
def medico_create(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            data = form.save()
            print("data.id", data.id, data.pk)  # borrar
            messages.success(request, "Se ha creado el médico.")
            return redirect('consultorios:medico_editar', data.id)
        else:
            messages.error(request, "Ha ocurrido un error. Datos no guardados.")
            return redirect('consultorios:medico_listar')
    else:
        form = MedicoForm()
    contexto = {'form': form}
    return render(request, 'consultorios/medico_form.html', contexto)


@transaction.atomic
def medico_update(request, pk):
    print("llega al update")  # borrar
    objeto = Medico.objects.get(id=pk)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=objeto)
        print("form.is_valid()", form.is_valid(), form.errors)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Se han actualizado los datos del médico.")
            return redirect("consultorios:medico_listar")
        else:
            messages.error(request, "Ha ocurrido un error. Datos no guardados.")
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
            messages.success(request, "Se ha creado el enfermero.")
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
            messages.success(request, "Se han actualizado los datos del enfermero.")
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
            messages.success(request, "Se ha creado el administrativo.")
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
            messages.success(request, "Se han actualizado los datos del administrativo.")
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
            messages.success(self.request, "Se ha creado el médico.")
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
            messages.success(self.request, "Se ha creado el horario médico.")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class HorarioMedicoUpdate(UpdateView):
    model = HorarioMedico
    template_name = 'consultorios/horario_medico_form.html'
    form_class = HorarioMedicoModelForm
    success_url = reverse_lazy('consultorios:horario_medico_listar')


def medico_especialidad(request, id_medico):
    especialidad = Especialidad.objects.filter(medico=id_medico).order_by('id')
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

    def form_valid(self, form):
        orden = form.save(commit=False)
        obs = orden.observacion
        if obs:
            obs = obs.replace(' src="', ' class="img-responsive" src="')
        orden.observacion = obs
        orden.save()
        messages.success(self.request, "Se ha creado la orden de estudio.")
        return JsonResponse({'success': True})


class OrdenEstudioDeleteGlobal(LoginRequiredMixin, DeleteView):
    model = OrdenEstudio
    template_name = "consultorios/orden_estudio/orden_estudio_eliminar.html"
    pk_url_kwarg = 'orden_id'
    context_object_name = 'orden'

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            print('Estado: PROTEGIDO')
            messages.error(request, 'No se puede borrar ' + self.object.nombre)
            return HttpResponseRedirect(reverse('consultorios:ordenes_estudio'))

    def get_success_url(self):
        messages.success(self.request, "Se ha eliminado la orden de estudio.")
        return reverse('consultorios:ordenes_estudio')


class OrdenEstudioUpdateGlobal(LoginRequiredMixin, UpdateView):
    model = OrdenEstudio
    form_class = OrdenEstudioForm
    template_name = 'consultorios/orden_estudio/orden_estudio_editar.html'
    pk_url_kwarg = 'orden_id'

    def form_valid(self, form):
        orden = form.save(commit=False)
        obs = orden.descripcion
        if obs:
            obs = obs.replace(' src="', ' class="img-responsive" src="')
        orden.descripcion = obs
        orden.save()
        messages.success(self.request, "Se han actualizado los datos de orden de estudio.")
        return JsonResponse({'success': True})

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
        messages.success(self.request, "Se han actualizado los datos de orden de estudio.")
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
        messages.success(self.request, "Se ha creado la orden de estudio.")
        return redirect(self.get_success_url())


class OrdenEstudioDetalleDeleteGlobal(LoginRequiredMixin, DeleteView):
    model = OrdenEstudioDetalle
    template_name = "consultorios/orden_estudio_detalle/orden_estudio_detalle_eliminar.html"
    pk_url_kwarg = 'detalle_id'
    context_object_name = 'detalle'

    def post(self, request, *args, **kwargs):
        orden_detail=OrdenEstudioDetalle.objects.get(pk=kwargs['detalle_id'])
        orden=OrdenEstudio.objects.get(pk=orden_detail.orden_estudio.id)
        print("orden", orden.pk)
        print("orden", orden_detail.pk)
        orden_detail.delete()
        messages.success(self.request, "Se ha eliminado la orden de estudio.")
        return HttpResponseRedirect(reverse('consultorios:orden_estudio_detalle_list', kwargs={'orden_id': orden.id}))


class ConsultorioPacienteList(LoginRequiredMixin, ListView):
    model = Paciente
    context_object_name = 'pacientes'
    template_name = 'consultorios/consultorio_paciente_list.html'

    def get_queryset(self):
        return Paciente.objects.exclude(consultadetalle__consulta=self.kwargs['consulta_id'])

    def get_context_data(self, **kwargs):
        context = super(ConsultorioPacienteList, self).get_context_data(**kwargs)
        context.update({'consulta': Consulta.objects.get(pk=self.kwargs['consulta_id'])})
        return context


class ConsultorioPacienteAgregar(LoginRequiredMixin, View):
    model = ConsultaDetalle

    def post(self, request, *args, **kwargs):
        consulta = Consulta.objects.get(pk=request.POST.get('consulta_id'))
        detalles = ConsultaDetalle.objects.filter(consulta=consulta)
        max_orden = detalles.aggregate(Max('orden'))
        paciente = Paciente.objects.get(pk=request.POST.get('paciente_id'))

        nuevo_detalle = ConsultaDetalle(orden=max_orden['orden__max']+1, paciente=paciente, consulta=consulta,
                                        estado=EstadoConsultaDetalle.objects.get(codigo='P'), confirmado=True)
        nuevo_detalle.save()

        verificar_estado_consulta(consulta)
        messages.success(self.request, "Se ha agregado el paciente.")
        return JsonResponse({'success': True})


class ConsultasDia(LoginRequiredMixin, TemplateView):
    """
    permite obtener todas las consultas del dia
    """
    template_name = 'consultorios/consultas_dia.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        medico = Medico.objects.get(usuario=request.user)
        # obtenemos todas las consultas del dia de hoy del medico logueado
        consultas = Consulta.objects.filter(estado='P', medico=medico, fecha=datetime.date.today())
        context.update({'medico': medico,
                        'consultas': consultas,
                        'fecha': datetime.date.today()
                        })

        return super(TemplateView, self).render_to_response(context)


class ConsultaDetalleDia(LoginRequiredMixin, TemplateView):
    """
    obtenemos los detalles de la consulta seleccionada
    """
    template_name = 'consultorios/citas_dia.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        consulta = Consulta.objects.get(pk=self.kwargs['consulta_id'])

        detalle = ConsultaDetalle.objects.filter(consulta=consulta)
        existe_en_proceso = detalle.filter(estado=EstadoConsultaDetalle.objects.get(codigo='E')).exists()

        context.update({'consulta': consulta,
                        'detalles': detalle,
                        'existe_en_proceso': existe_en_proceso,
                        })

        return super(TemplateView, self).render_to_response(context)


class ConsultaCreate(LoginRequiredMixin, View):
    model = Consulta

    def post(self, request, *args, **kwargs):
        agenda = Agenda.objects.get(pk=kwargs.get('agenda_id'))
        origen = request.POST["origen"]

        agenda.estado=EstadoAgenda.objects.get(codigo='V')
        agenda.save()
        agenda_detalle = AgendaDetalle.objects.filter(agenda=agenda)

        consulta = Consulta.objects.create(fecha=agenda.fecha, estado=EstadoConsulta.objects.get(codigo='P'),
                                           medico=agenda.medico, turno=agenda.turno,
                                           especialidad=agenda.especialidad)
        for det in agenda_detalle:
            ConsultaDetalle.objects.create(orden=det.orden, confirmado=det.confirmado, consulta=consulta,
                                           paciente=det.paciente, estado=EstadoConsultaDetalle.objects.get(codigo='P'))

        origen_url = get_origen_url_agendamiento(origen)

        return JsonResponse(origen_url, safe=False)


class ConsultaDetalleIniciar(LoginRequiredMixin, TemplateView):
    """
    permite iniciar la consulta del paciente.
    """
    template_name = 'consultorios/consulta/consulta_iniciar.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # obtenemos la consuta detalle
        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])

        # actualizamos el estado del detalle de la consulta a "en proceso"
        if detalle.estado.codigo == "P":
            detalle.estado = EstadoConsultaDetalle.objects.get(codigo='E')

        if not detalle.hora_inicio:
            detalle.hora_inicio = datetime.datetime.now()

        detalle.save()

        verificar_estado_consulta(detalle.consulta)

        #anamnesis del paciente
        anamnesis = Anamnesis.objects.filter(paciente=detalle.paciente, consulta_detalle=detalle).order_by('-pk')

        #diagnosticos del paciente.
        diagnosticos = Diagnostico.objects.filter(paciente=detalle.paciente, consulta_detalle=detalle).order_by('-pk')

        #evoluciones del paciente
        evoluciones = EvolucionPaciente.objects.filter(paciente=detalle.paciente,
                                                       consulta_detalle=detalle).order_by('-pk')

        #ordenes de estudio del paciente
        ordenes = ConsultaOrdenEstudio.objects.filter(paciente=detalle.paciente,
                                                      consulta_detalle=detalle).order_by('-pk')

        # prescripciones del paciente
        prescripciones = ConsultaPrescripcion.objects.filter(paciente=detalle.paciente,
                                                             consulta_detalle=detalle).order_by('-pk')

        # tratamientos del paciente
        tratamientos = Tratamiento.objects.filter(paciente=detalle.paciente, consulta_detalle=detalle)

        ir_a_tab = request.GET.get('ir_a_tab', None)
        print("ir_a_tab:", ir_a_tab)

        if not ir_a_tab:
            ir_a_tab = "a_anam"  # por default va al tab de anamnesis

        ir_a_tab = "#"+ir_a_tab

        print("va a tab:", ir_a_tab)

        context.update({
            'consulta': detalle.consulta,
            'detalle': detalle,
            'diagnosticos': diagnosticos,
            'evoluciones': evoluciones,
            'ordenes': ordenes,
            'prescripciones': prescripciones,
            'tratamientos': tratamientos,
            'anamnesis': anamnesis,
            'ir_a_tab': ir_a_tab
        })
        # return super(TemplateView, self).render_to_response(context)
        return render(request=request, template_name=self.template_name, context=context)


# class ConsultaDetalleContinuar(LoginRequiredMixin, TemplateView):
#     """
#     permite registrar las siguientes acciones de la consulta del paciente.
#     Muestra el detalle de la consulta actual
#     """
#     template_name = 'consultorios/consulta/consulta_iniciar.html'
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         #obtenemos el detalle actual
#         detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
#         consulta = Consulta.objects.get(pk=detalle.consulta.id)
#         #obtenemos el detalle de la consulta donde el estado sea en proceso
#
#         #consultamos si el paciente ya tiene un diagnostico en la consulta actual
#         if Diagnostico.objects.filter(consulta_detalle=detalle).exists():
#             diagnostico = Diagnostico.objects.get(consulta_detalle=detalle)
#         else:
#             diagnostico = None
#
#         context.update({
#             'consulta': consulta,
#             'detalle': detalle,
#             'diagnostico': diagnostico,
#         })
#         return super(TemplateView, self).render_to_response(context)


class ConsultaDetalleVolver(LoginRequiredMixin, View):
    """
    Devuelve la consulta detalle entre el listado de pacientes no atendidos
    """
    model = ConsultaDetalle

    def post(self, request, *args, **kwargs):
        consulta_det_id = request.POST.get('consulta_det_id')
        print("consulta det id", consulta_det_id)
        consulta_det = ConsultaDetalle.objects.get(pk=consulta_det_id)

        consulta_det.estado = EstadoConsultaDetalle.objects.get(codigo="P")  # cambio de estado a PENDIENTE
        consulta_det.hora_inicio = None
        consulta_det.save()

        verificar_estado_consulta(consulta_det.consulta)

        return JsonResponse({'success': True})


class ConsultaDetalleCancelar(LoginRequiredMixin, View):
    model = ConsultaDetalle

    def post(self, request, *args, **kwargs):
        consulta_det_id = request.POST.get('consulta_det_id')
        print("consulta det id", consulta_det_id)
        consulta_det = ConsultaDetalle.objects.get(pk=consulta_det_id)

        consulta_det.estado = EstadoConsultaDetalle.objects.get(codigo="C")  # cambio de estado a CANCELADO
        consulta_det.hora_fin = datetime.datetime.now()
        consulta_det.save()

        verificar_estado_consulta(consulta_det.consulta)

        return JsonResponse({'success': True})


class ConsultaDetalleFinalizar(LoginRequiredMixin, View):
    model = ConsultaDetalle

    def post(self, request, *args, **kwargs):
        consulta_det_id = request.POST.get('consulta_det_id')
        print("consulta det id", consulta_det_id)
        consulta_det = ConsultaDetalle.objects.get(pk=consulta_det_id)

        consulta_det.estado = EstadoConsultaDetalle.objects.get(codigo="F")  # cambio de estado a FINALIZADO
        consulta_det.hora_fin = datetime.datetime.now()
        consulta_det.save()

        verificar_estado_consulta(consulta_det.consulta)

        return JsonResponse({'success': True})


class ConsultaDetalleResumen(LoginRequiredMixin, TemplateView):
    """
    Resumen que se muestra al finalizar la consulta de un paciente
    """
    template_name = 'consultorios/consulta/consulta_resumen.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # detalle_id = request.GET.get('consulta_det_id')
        # consulta = Consulta.objects.get(pk=self.kwargs['consulta_id'])
        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        print("detalle id = ", detalle.pk)

        # anamnesis del paciente
        anamnesis = Anamnesis.objects.filter(paciente=detalle.paciente, consulta_detalle=detalle.id).order_by('-pk')

        # diagnosticos del paciente.  # TODO: ver si no se cambió a módulo de Consultorios. Agregar el Foreign key de consulta detalle
        diagnosticos = Diagnostico.objects.filter(paciente=detalle.paciente,
                                                  consulta_detalle=detalle.id).order_by('-pk')
        # evoluciones del paciente
        evoluciones = EvolucionPaciente.objects.filter(paciente=detalle.paciente,
                                                       consulta_detalle=detalle.id).order_by('-pk')
        # ordenes de estudio del paciente
        ordenes = ConsultaOrdenEstudio.objects.filter(paciente=detalle.paciente,
                                                      consulta_detalle=detalle.id).order_by('-pk')
        # prescripciones del paciente
        prescripciones = ConsultaPrescripcion.objects.filter(paciente=detalle.paciente,
                                                             consulta_detalle=detalle.id).order_by('-pk')
        # tratamientos del paciente
        tratamientos = Tratamiento.objects.filter(paciente=detalle.paciente,
                                                  consulta_detalle=detalle.id).order_by('-pk')

        context.update({
            'consulta': detalle.consulta,
            'detalle': detalle,
            'diagnosticos': diagnosticos,
            'evoluciones': evoluciones,
            'ordenes': ordenes,
            'prescripciones': prescripciones,
            'tratamientos': tratamientos,
            'anamnesis': anamnesis
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
        if Diagnostico.objects.filter(consulta_detalle=detalle).exists():
            diagnostico = Diagnostico.objects.get(consulta_detalle=detalle)
        else:
            diagnostico = None

        context.update({
            'consulta': consulta,
            'detalle': detalle,
            'diagnostico': diagnostico,
        })
        return super(TemplateView, self).render_to_response(context)


class EvolucionPacienteCreate(LoginRequiredMixin, FormView):
    """permite registrar la evolución del paciente en una consulta"""
    model = EvolucionPaciente
    template_name = 'consultorios/consulta/evolucion_paciente_form.html'
    pk_url_kwarg = "detalle_id"
    form_class = EvolucionPacienteForm

    def get_context_data(self, **kwargs):
        context = super(EvolucionPacienteCreate, self).get_context_data(**kwargs)
        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        context.update({'detalle': detalle})
        return context

    def form_valid(self, form):
        evolucion = form.save(commit=False)
        obs = evolucion.observaciones
        if obs:
            obs = obs.replace(' src="', ' class="img-responsive" src="')
        evolucion.observaciones = obs
        consulta_detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        consulta = Consulta.objects.get(pk=consulta_detalle.consulta.id)
        evolucion.consulta_detalle = consulta_detalle
        evolucion.paciente = consulta_detalle.paciente
        evolucion.medico = consulta.medico
        evolucion.save()
        messages.success(self.request, "Se ha creado la evolución.")
        return JsonResponse({'success': True})


class EvolucionPacienteUpdate(LoginRequiredMixin, UpdateView):
    model = EvolucionPaciente
    template_name = 'consultorios/consulta/evolucion_paciente_form.html'
    pk_url_kwarg = 'evolucion_id'
    form_class = EvolucionPacienteForm

    def get_context_data(self, **kwargs):
        context = super(EvolucionPacienteUpdate, self).get_context_data(**kwargs)
        context.update({'detalle': self.object.consulta_detalle})
        return context

    def form_valid(self, form):
        evolucion = form.save(commit=False)
        obs = evolucion.observaciones
        if obs:
            obs = obs.replace(' src="', ' class="img-responsive" src="')
        evolucion.observaciones = obs
        evolucion.save()
        messages.success(self.request, "Se han actualizado los datos de la evolución.")
        return JsonResponse({'success': True})


class EvolucionPacienteDetele(LoginRequiredMixin, DeleteView):
    model = EvolucionPaciente
    template_name = "consultorios/consulta/evolucion_paciente_eliminar.html"
    pk_url_kwarg = 'evolucion_id'
    context_object_name = 'evolucion'

    def post(self, request, *args, **kwargs):
        evolucion = EvolucionPaciente.objects.get(pk=self.kwargs['evolucion_id'])
        evolucion.delete()
        return JsonResponse({'success': True})


class EvolucionPacienteList(LoginRequiredMixin, ListView):
    """Obtiene el listado de registros de evolución del paciente"""
    model = EvolucionPaciente
    context_object_name = 'evoluciones'
    template_name = 'consultorios/consulta_iniciar.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # obtenemos el detalle actual
        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        consulta = Consulta.objects.get(pk=detalle.consulta.id)

        evoluciones = EvolucionPaciente.objects.filter(paciente=detalle.paciente).order_by('-consulta_detalle')

        context.update({
            'consulta': consulta,
            'detalle': detalle,
            'evoluciones': evoluciones,
        })
        messages.success(self.request, "Se ha eliminado la evolución.")
        return super(TemplateView, self).render_to_response(context)


class PacienteDiagnosticoCreate(LoginRequiredMixin, FormView):
    """permite registrar el diagnostico al paciente"""
    model = Diagnostico
    template_name = 'consultorios/consulta/diagnostico_paciente.html'
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
        diagnostico.consulta_detalle = detalle
        diagnostico.paciente = detalle.paciente
        diagnostico.medico = consulta.medico
        diagnostico.save()
        messages.success(self.request, "Se ha creado el diagnóstico.")
        return JsonResponse({'success': True})


class PacienteDiagnosticoEditar(LoginRequiredMixin, UpdateView):
    model = Diagnostico
    template_name = 'consultorios/consulta/diagnostico_paciente.html'
    pk_url_kwarg = 'diagnostico_id'
    form_class = DiagnosticoPacienteForm

    def get_context_data(self, **kwargs):
        context = super(PacienteDiagnosticoEditar, self).get_context_data(**kwargs)
        context.update({'detalle': self.object.consulta_detalle})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Se han actualizado los datos del diagnóstico.")
        return JsonResponse({'success': True})


class PacienteDiagnosticoEliminar(LoginRequiredMixin, DeleteView):
    model = Diagnostico
    template_name = "consultorios/consulta/diagnostico_paciente_eliminar.html"
    pk_url_kwarg = 'diagnostico_id'
    context_object_name = 'diagnostico'

    def post(self, request, *args, **kwargs):
        diagnostico = Diagnostico.objects.get(pk=self.kwargs['diagnostico_id'])
        diagnostico.delete()
        messages.success(self.request, "Se ha eliminado el diagnóstico")
        return JsonResponse({'success': True})


class PacienteOrdenEstudioCreate(LoginRequiredMixin, FormView):
    """Permite registrar la orden de estudio del paciente en la consulta"""
    model = ConsultaOrdenEstudio
    template_name = 'consultorios/consulta/orden_estudio_form.html'
    pk_url_kwarg = "detalle_id"
    form_class = OrdenEstudioPacienteForm

    def get_context_data(self, **kwargs):
        context = super(PacienteOrdenEstudioCreate, self).get_context_data(**kwargs)
        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        context.update({'detalle': detalle})
        return context

    def form_valid(self, form):
        """guardamos la orden de estudio de la consulta del paciente(consulta detalle)"""
        orden_estudio = form.save(commit=False)
        consulta_detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        orden_estudio.consulta_detalle = consulta_detalle
        orden_estudio.paciente = consulta_detalle.paciente
        orden_estudio.save()
        messages.success(self.request, "Se ha creado la orden de estudio.")
        return JsonResponse({'success': True})


class PacienteOrdenEstudioUpdate(LoginRequiredMixin, UpdateView):
    model = ConsultaOrdenEstudio
    form_class = OrdenEstudioPacienteForm
    template_name = 'consultorios/consulta/orden_estudio_form.html'
    pk_url_kwarg = 'orden_id'
    # context_object_name = 'orden'

    def get_context_data(self, **kwargs):
        context = super(PacienteOrdenEstudioUpdate, self).get_context_data(**kwargs)
        context.update({'detalle': self.object.consulta_detalle})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Se han actualizado los datos de la orden de estudio.")
        return JsonResponse({'success': True})


class PacienteOrdenEstudioDelete(LoginRequiredMixin, DeleteView):
    model = ConsultaOrdenEstudio
    template_name = "consultorios/consulta/orden_estudio_eliminar.html"
    pk_url_kwarg = 'orden_id'
    context_object_name = 'orden'

    def post(self, request, *args, **kwargs):
        orden = ConsultaOrdenEstudio.objects.get(pk=self.kwargs['orden_id'])
        orden.delete()
        messages.success(self.request, "Se ha eliminado la orden de estudio.")
        return JsonResponse({'success': True})


class PacientePrescripcionCreate(LoginRequiredMixin, FormView):
    """permite registrar el diagnostico al paciente"""
    model = ConsultaPrescripcion
    second_model = Medicamento
    template_name = 'consultorios/consulta/prescripcion_form.html'
    pk_url_kwarg = "prescripcion_id"
    form_class = PrescripcionPacienteForm
    second_form_class = MedicamentoForm

    def get_context_data(self, **kwargs):
        context = super(PacientePrescripcionCreate, self).get_context_data(**kwargs)
        detalle=ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        context.update({'detalle': detalle,
                        'form2': self.second_form_class(self.request.GET)})
        return context

    def form_valid(self, form):
        """guardamos la prescripción del paciente (consulta detalle)"""
        prescripcion = form.save(commit=False)
        consulta_detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        prescripcion.paciente = consulta_detalle.paciente
        prescripcion.consulta_detalle = consulta_detalle
        prescripcion.save()
        messages.success(self.request, "Se ha creado la prescripción médica.")
        return JsonResponse({'success': True})


class PacientePrescripcionUpdate(LoginRequiredMixin, UpdateView):
    model = ConsultaPrescripcion
    form_class = PrescripcionPacienteForm
    template_name = 'consultorios/consulta/prescripcion_form.html'
    pk_url_kwarg = 'prescripcion_id'
    context_object_name = 'prescripcion'
    second_form_class = MedicamentoForm

    def get_context_data(self, **kwargs):
        context = super(PacientePrescripcionUpdate, self).get_context_data(**kwargs)
        context.update({'detalle': self.object.consulta_detalle,
                        'form2': self.second_form_class(self.request.GET)})
        return context

    def form_valid(self, form):
        """guardamos la prescripcion de la consulta del paciente(consulta detalle)"""
        form.save()
        messages.success(self.request, "Se han actualizado los datos de prescripción médica.")
        return JsonResponse({'success': True})


class PacientePrescripcionDelete(LoginRequiredMixin, DeleteView):
    model = ConsultaPrescripcion
    template_name = "consultorios/consulta/prescripcion_eliminar.html"
    pk_url_kwarg = 'prescripcion_id'
    context_object_name = 'prescripcion'

    def post(self, request, *args, **kwargs):
        orden = ConsultaPrescripcion.objects.get(pk=self.kwargs['prescripcion_id'])
        orden.delete()
        messages.success(self.request, "Se ha eliminado la prescripción médica.")
        return JsonResponse({'success': True})


class PacienteTratamientoCreate(LoginRequiredMixin, FormView):
    """permite registrar el tratamiento al paciente"""
    model = Tratamiento
    template_name = 'consultorios/consulta/tratamiento/tratamiento_paciente_form.html'
    pk_url_kwarg = "detalle_id"
    form_class = TratamientoPacienteForm

    def get_context_data(self, **kwargs):
        context = super(PacienteTratamientoCreate, self).get_context_data(**kwargs)
        detalle=ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        context.update({'detalle': detalle})
        return context

    def form_valid(self, form):
        """guardamos el tratamiento de la consulta del paciente(consulta detalle)"""
        tratamiento = form.save(commit=False)
        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        tratamiento.consulta_detalle = detalle
        tratamiento.paciente = detalle.paciente
        tratamiento.save()
        messages.success(self.request, "Se ha creado el tratamiento.")
        return JsonResponse({'success': True})


class PacienteTratamientoDelete(LoginRequiredMixin, DeleteView):
    model = Tratamiento
    template_name = "consultorios/consulta/tratamiento/tratamiento_paciente_eliminar.html"
    pk_url_kwarg = 'tratamiento_id'
    context_object_name = 'tratamiento'

    def post(self, request, *args, **kwargs):
        diagnostico = Tratamiento.objects.get(pk=self.kwargs['tratamiento_id'])
        diagnostico.delete()
        messages.success(self.request, "Se ha eliminado el tratamiento.")
        return JsonResponse({'success': True})


class PacienteTratamientoUpdate(LoginRequiredMixin, UpdateView):
    model = Tratamiento
    template_name = 'consultorios/consulta/tratamiento/tratamiento_paciente_form.html'
    pk_url_kwarg = 'tratamiento_id'
    form_class = TratamientoPacienteForm

    def get_context_data(self, **kwargs):
        context = super(PacienteTratamientoUpdate, self).get_context_data(**kwargs)
        context.update({'detalle': self.object.consulta_detalle})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Se han actualizado los datos de tratamiento.")
        return JsonResponse({'success': True})


class DashboardMedico(LoginRequiredMixin, TemplateView):
    template_name = 'consultorios/dashboard_medico.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            if Medico.objects.filter(usuario=user).exists():
                return super(DashboardMedico, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('logout'))
        return super(DashboardMedico, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        medico = Medico.objects.get(usuario=request.user)
        # Obtenemos las especialidades del médico
        especialidades = medico.especialidad.all()

        # Obtenemos las consultas relacionadas al médico
        # Consultas = Consulta.objects.filter(medico=medico)
        detalles = ConsultaDetalle.objects.filter(consulta__medico=medico)

        consultas_realizadas = ConsultaDetalle.objects.filter(consulta__medico=medico,
                                                              estado=EstadoConsultaDetalle.objects.get(codigo='F')).\
            count()

        consultas_canceladas = ConsultaDetalle.objects.filter(consulta__medico=medico,
                                                              estado=EstadoConsultaDetalle.objects.get(
                                                                  codigo='C')).count()

        now = datetime.datetime.now()
        _, num_days = calendar.monthrange(now.year, now.month)
        first_day = datetime.date(now.year, now.month, 1)
        last_day = datetime.date(now.year, now.month, num_days)

        consultas_mes = ConsultaDetalle.objects.filter(consulta__medico=medico,
                                                       estado=EstadoConsultaDetalle.objects.get(codigo='F'),
                                                       consulta__fecha__range=[first_day, last_day]).count()

        consultas_dia = ConsultaDetalle.objects.filter(consulta__medico=medico,
                                                       consulta__fecha=datetime.date.today()).count()

        genero_masculino = []
        genero_femenino = []
        lista_especialidades = []
        lista_pacientes_especialidad = []
        max_ninhez = 12
        max_adolescencia = 18
        max_juventud = 4
        max_adultez = 65

        cant_ninhez = 0
        cant_adolescencia = 0
        cant_juventud = 0
        cant_adultez = 0
        cant_vejez = 0

        consultas = ConsultaDetalle.objects.filter(consulta__medico=medico).values('paciente').distinct()

        for consulta in consultas:
            paciente = Paciente.objects.get(pk=consulta['paciente'])
            edad = calculate_age(paciente.fecha_nacimiento)
            if edad <= max_ninhez:
                cant_ninhez += 1
            elif edad <= max_adolescencia:
                cant_adolescencia += 1
            elif edad <= max_juventud:
                cant_juventud += 1
            elif edad <= max_adultez:
                cant_adultez += 1
            else:
                cant_vejez += 1

        lista_pacientes_by_edad = [cant_ninhez, cant_adolescencia, cant_juventud, cant_adultez, cant_vejez]

        for especialidad in especialidades:

            consulta_masculina =ConsultaDetalle.objects.filter(consulta__medico=medico,
                                                               consulta__especialidad=especialidad,
                                                               paciente__sexo__codigo='M')
            genero_masculino.append(consulta_masculina.count())

            consulta_femenina = ConsultaDetalle.objects.filter(consulta__medico=medico,
                                                               consulta__especialidad=especialidad,
                                                               paciente__sexo__codigo='F')

            genero_femenino.append(consulta_femenina.count())

            # obtenemos la cantidad de pacientes que se agendaron en una especialidad
            paciente_by_especialidad = ConsultaDetalle.objects.filter(consulta__especialidad=especialidad).\
                values('paciente').distinct().count()

            lista_pacientes_especialidad.append(paciente_by_especialidad)

            lista_especialidades.append(especialidad.nombre)

        context.update({
            'pacientes_by_especialidad': lista_pacientes_especialidad,
            'especialidades_nombre': mark_safe(lista_especialidades),
            'genero_masculino': genero_masculino,
            'genero_femenino': genero_femenino,
            'medico': medico,
            'consultas_realizadas': consultas_realizadas,
            'consultas_canceladas': consultas_canceladas,
            'consultas_mes': consultas_mes,
            'consultas_dia': consultas_dia,
            'grupo_edades': mark_safe(['Infancia', 'Adolescencia', 'Juventud', 'Adultez', 'Vejez']),
            'pacientes_by_edad': lista_pacientes_by_edad,
            'especialidades': especialidades
        })

        return super(TemplateView, self).render_to_response(context)


class TipoMedicamentoListView(LoginRequiredMixin, ListView):
    model = TipoMedicamento
    context_object_name = 'tipos'
    template_name = 'consultorios/tipo_medicamento/tipo_medicamento_list.html'

    def get_queryset(self):
        return TipoMedicamento.objects.filter(habilitado=True)


class TipoMedicamentoCreateView(LoginRequiredMixin, CreateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'consultorios/tipo_medicamento/tipo_medicamento_crear.html'

    def form_valid(self, form):
        tipo_medicamento = form.save(commit=False)
        descripcion = tipo_medicamento.descripcion
        if descripcion:
            descripcion = descripcion.replace(' src="', ' class="img-responsive" src="')
        tipo_medicamento.descripcion = descripcion
        tipo_medicamento.save()
        messages.success(self.request, "Se ha creado el tipo medicamento.")
        return JsonResponse({'success': True})


class TipoMedicamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'consultorios/tipo_medicamento/tipo_medicamento_editar.html'
    pk_url_kwarg = 'tipo_id'

    def form_valid(self, form):
        tipo_medicamento = form.save(commit=False)
        desc = tipo_medicamento.descripcion
        if desc:
            desc = desc.replace(' src="', ' class="img-responsive" src="')
        tipo_medicamento.descripcion = desc
        tipo_medicamento.save()
        messages.success(self.request, "Se han actualizado los datos de tipo medicamento.")
        return JsonResponse({'success': True})


class TipoMedicamentoDelete(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        tipo = TipoMedicamento.objects.get(pk=kwargs['tipo_id'])
        tipo.habilitado = False
        tipo.save()
        messages.success(self.request, "Se ha eliminado el tipo medicamento.")
        return JsonResponse({'success':True})


class MedicamentoListView(LoginRequiredMixin, ListView):
    model = Medicamento
    context_object_name = 'medicamentos'
    template_name = 'consultorios/medicamentos/medicamentos_list.html'

    def get_queryset(self):
        return Medicamento.objects.filter(habilitado=True)


class MedicamentoCreateView(LoginRequiredMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'consultorios/medicamentos/medicamentos_form.html'

    def get_success_url(self):
        messages.success(self.request, "Se ha creado el medicamento.")
        return reverse('consultorios:medicamentos')


class MedicamentoNuevoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        forma_farmaceutica = request.POST.get('forma_farmaceutica')
        _tipificacion = request.POST.get('tipificacion')
        tipificacion = TipoMedicamento.objects.get(pk=_tipificacion)
        print(nombre, forma_farmaceutica, tipificacion)

        medicamento = Medicamento(nombre=nombre, forma_farmaceutica=forma_farmaceutica, tipificacion=tipificacion,
                                  cantidad=1)
        medicamento.save()
        return JsonResponse({'medicamento_id': medicamento.id,
                             'medicamento_nombre': medicamento.nombre})


class MedicamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'consultorios/medicamentos/medicamentos_form.html'
    pk_url_kwarg = 'medicamento_id'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(MedicamentoUpdateView, self).get_form_kwargs()
        kwargs['tipo'] = Medicamento.objects.filter(pk=self.kwargs['medicamento_id']).values('tipificacion')
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Se han actualizado los datos de medicamento.")
        return reverse('consultorios:medicamentos')


class MedicamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Medicamento
    template_name = "consultorios/medicamentos/medicamentos_eliminar.html"
    pk_url_kwarg = 'medicamento_id'
    context_object_name = 'medicamento'

    def post(self, request, *args, **kwargs):
        medicamento = Medicamento.objects.get(pk=kwargs['medicamento_id'])
        medicamento.habilitado = False
        medicamento.save()
        messages.success(self.request, "Se ha eliminado el medicamento.")
        return HttpResponseRedirect(reverse('consultorios:medicamentos'))


class AnamnesisPacienteCreate(LoginRequiredMixin, FormView):
    """permite registrar anamnesis del paciente en una consulta"""
    model = Anamnesis
    template_name = 'consultorios/consulta/anamnesis/anamnesis_form.html'
    pk_url_kwarg = "detalle_id"
    form_class = AnamnesisPacienteForm

    def get_context_data(self, **kwargs):
        context = super(AnamnesisPacienteCreate, self).get_context_data(**kwargs)
        detalle=ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        context.update({'detalle': detalle})
        return context

    def form_valid(self, form):
        anamnesis = form.save(commit=False)
        consulta_detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])
        consulta = Consulta.objects.get(pk=consulta_detalle.consulta.id)
        anamnesis.consulta_detalle = consulta_detalle
        anamnesis.paciente = consulta_detalle.paciente
        anamnesis.save()
        messages.success(self.request, "Se ha creado la anamnesis.")
        return JsonResponse({'success': True})


class AnamnesisPacienteDetele(LoginRequiredMixin, DeleteView):
    model = Anamnesis
    template_name = "consultorios/consulta/anamnesis/anamnesis_paciente_eliminar.html"
    pk_url_kwarg = 'anamnesis_id'
    context_object_name = 'anamnesis'

    def post(self, request, *args, **kwargs):
        anamnesis = Anamnesis.objects.get(pk=self.kwargs['anamnesis_id'])
        anamnesis.delete()
        messages.success(self.request, "Se ha eliminado los datos de anamnesis.")
        return JsonResponse({'success': True})


class AnamnesisPacienteUpdate(LoginRequiredMixin, UpdateView):
    model = Anamnesis
    template_name = 'consultorios/consulta/anamnesis/anamnesis_form.html'
    pk_url_kwarg = 'anamnesis_id'
    form_class = AnamnesisPacienteForm

    def get_context_data(self, **kwargs):
        context = super(AnamnesisPacienteUpdate, self).get_context_data(**kwargs)
        context.update({'detalle': self.object.consulta_detalle})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Se han actualizado los datos de anamnesis.")
        return JsonResponse({'success': True})


class HistoriaClinicaList(LoginRequiredMixin, TemplateView):
    template_name = 'consultorios/consulta/consulta_historia.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        hoy = datetime.datetime.now()

        p_fechas = request.GET.get('fechas', None)

        if p_fechas:
            fechas = p_fechas.split("-")
            p_desde = fechas[0]
            p_hasta = fechas[1].split(" ")[1]
            desde = p_desde.split(" ")
            p_desde = desde[0]
            fecha_desde = datetime.datetime.strptime(p_desde, '%d/%m/%Y')
            fecha_hasta = datetime.datetime.strptime(p_hasta, '%d/%m/%Y')
        else:
            fecha_desde = hoy
            fecha_hasta = hoy
        """
        obtenemos los detalles de la consulta que se encuentra finalizadas o canceladas
        """
        consultas = ConsultaDetalle.objects.filter(paciente=self.kwargs['paciente_id'],
                                                   consulta__fecha__gte=fecha_desde,
                                                   consulta__fecha__lte = fecha_hasta,
                                                   estado=EstadoConsultaDetalle.objects.filter(
                                                       Q(pk=EstadoConsultaDetalle.objects.get(codigo='E')) |
                                                       Q(pk=EstadoConsultaDetalle.objects.get(codigo='C'))))
        # obtenemos el d
        ultima_consulta = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])

        context.update({
            'fecha_input': p_fechas if p_fechas else None,
            'detalle': ultima_consulta,
            'consultas': consultas
        })

        return super(TemplateView, self).render_to_response(context)


class GeneratePDF(View):
    """Clase solo de prueba de pdf."""
    pk_url_kwarg = "detalle_id"

    def get(self, request, *args, **kwargs):
        template = get_template('consultorios/consulta/consulta_resumen.html')

        detalle = ConsultaDetalle.objects.get(pk=4)
        print("detalle id = ", detalle)

        consulta = Consulta.objects.get(pk=3)

        # anamnesis del paciente
        anamnesis = Anamnesis.objects.filter(paciente=4, consulta_detalle=4).order_by('-pk')

        # diagnosticos del paciente.
        diagnosticos = Diagnostico.objects.filter(paciente=4,
                                                  consulta_detalle=4).order_by('-pk')
        # evoluciones del paciente
        evoluciones = EvolucionPaciente.objects.filter(paciente=4,
                                                       consulta_detalle=4).order_by('-pk')
        # ordenes de estudio del paciente
        ordenes = ConsultaOrdenEstudio.objects.filter(paciente=4,
                                                      consulta_detalle=4).order_by('-pk')
        # prescripciones del paciente
        prescripciones = ConsultaPrescripcion.objects.filter(paciente=4,
                                                             consulta_detalle=4).order_by('-pk')
        # tratamientos del paciente
        tratamientos = Tratamiento.objects.filter(paciente=4,
                                                  consulta_detalle=4).order_by('-pk')

        context = {
            'consulta': consulta,
            'detalle': detalle,
            'diagnosticos': diagnosticos,
            'evoluciones': evoluciones,
            'ordenes': ordenes,
            'prescripciones': prescripciones,
            'tratamientos': tratamientos,
            'anamnesis': anamnesis
        }

        html = template.render(context)
        pdf = render_to_pdf('consultorios/consulta/consulta_resumen.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class ConsultaDetalleHistoriaClinica(LoginRequiredMixin, DetailView):
    model = ConsultaDetalle
    template_name = "consultorios/detalle_consulta_medica.html"
    pk_url_kwarg = "consulta_id"

    def get_context_data(self, **kwargs):
        context = super(ConsultaDetalleHistoriaClinica, self).get_context_data(**kwargs)
        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['consulta_id'])
        context.update({'detalle': detalle,
                        'anamnesis': Anamnesis.objects.filter(consulta_detalle=detalle).order_by('-pk'),
                        'diagnosticos': Diagnostico.objects.filter(consulta_detalle=detalle).order_by('-pk'),
                        'evoluciones': EvolucionPaciente.objects.filter(consulta_detalle=detalle).order_by('-pk'),
                        'tratamientos': Tratamiento.objects.filter(consulta_detalle=detalle).order_by('-pk'),
                        'ordenes': ConsultaOrdenEstudio.objects.filter(consulta_detalle=detalle).order_by('-pk'),
                        'prescripciones': ConsultaPrescripcion.objects.filter(paciente=detalle.paciente,
                                                                              consulta_detalle=detalle.id).order_by('-pk')
                        })
        return context


class HistoriaClinicaPDF(View):

    def get(self, request, *args, **kwargs):
        template = get_template('consultorios/consulta/consulta_resumen_pdf.html')

        detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])

        # anamnesis del paciente
        anamnesis = Anamnesis.objects.filter(consulta_detalle=detalle).order_by('-pk')

        # diagnosticos del paciente.
        diagnosticos = Diagnostico.objects.filter(consulta_detalle=detalle).order_by('-pk')

        # evoluciones del paciente
        evoluciones = EvolucionPaciente.objects.filter(consulta_detalle=detalle).order_by('-pk')

        # ordenes de estudio del paciente
        ordenes = ConsultaOrdenEstudio.objects.filter(consulta_detalle=detalle).order_by('-pk')
        # prescripciones del paciente
        prescripciones = ConsultaPrescripcion.objects.filter(paciente=detalle.paciente,
                                                             consulta_detalle=detalle.id).\
            order_by('-pk')
        # tratamientos del paciente
        tratamientos = Tratamiento.objects.filter(consulta_detalle=detalle).order_by('-pk')

        context = {
            'detalle': detalle,
            'diagnosticos': diagnosticos,
            'evoluciones': evoluciones,
            'ordenes': ordenes,
            'prescripciones': prescripciones,
            'tratamientos': tratamientos,
            'anamnesis': anamnesis
        }

        html = template.render(context)
        pdf = render_to_pdf('consultorios/consulta/consulta_resumen_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class HistoriaClinicaConsultar(LoginRequiredMixin, TemplateView):
    """
    permite consultar la historia clinica de los pacientes.
    """
    template_name = 'consultorios/consulta/consultar_historia_paciente.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        p_paciente = request.GET.get('paciente', None)

        if not p_paciente:
            paciente = Paciente.objects.all()
        else:
            paciente = Paciente.objects.filter(pk=p_paciente)
            consultas = ConsultaDetalle.objects.filter(paciente=p_paciente)

        context.update({
            'paciente_select': Paciente.objects.get(pk=p_paciente) if p_paciente else None,
            'pacientes_list': Paciente.objects.all(),
            'pacientes': paciente

        })

        return super(TemplateView, self).render_to_response(context)


class PacienteFichaClinicaView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = 'pacientes/ficha_clinica.html'
    context_object_name = 'paciente'
    pk_url_kwarg = 'paciente_id'

    def get_datos_basicos(self):
        return Paciente.objects.get(pk=self.kwargs['paciente_id'])

    def get_direcciones(self):
        return Direccion.objects.filter(paciente__id=self.kwargs['paciente_id'])

    def get_datos_padres(self):
        return PacientePadre.objects.filter(paciente__id=self.kwargs['paciente_id'])

    def get_educacion(self):
        if PacienteNivelEducativo.objects.filter(paciente__id=self.kwargs['paciente_id']).exists():
            return PacienteNivelEducativo.objects.get(paciente__id=self.kwargs['paciente_id'])
        else:
            return None

    def get_seguros_medicos(self):
        return PacienteSeguroMedico.objects.filter(paciente__id=self.kwargs['paciente_id'])

    def get_ocupaciones(self):
        return PacienteOcupacion.objects.filter(paciente__id=self.kwargs['paciente_id'])

    def get_telefono(self):
        return Telefono.objects.get(paciente__id=self.kwargs['paciente_id'])

    def get_correo_electronico(self):
        if CorreoElectronico.objects.filter(paciente__id=self.kwargs['paciente_id']).exists():
            return CorreoElectronico.objects.filter(paciente__id=self.kwargs['paciente_id'])[0]
        else:
            return None

    def get_vivienda(self):
        if Vivienda.objects.filter(paciente__id=self.kwargs['paciente_id']).exists():
            return Vivienda.objects.filter(paciente__id=self.kwargs['paciente_id'])[0]
        else:
            return None

    def get_servicio_sanitario(self):
        if ServicioSanitario.objects.filter(paciente__id=self.kwargs['paciente_id']).exists():
            return ServicioSanitario.objects.filter(paciente__id=self.kwargs['paciente_id'])[0]
        else:
            return None

    def get_servicio_basico(self):
        if ServicioBasicos.objects.filter(paciente__id=self.kwargs['paciente_id']).exists():
            return ServicioBasicos.objects.filter(paciente__id=self.kwargs['paciente_id'])[0]
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super(PacienteFichaClinicaView, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.get_datos_basicos(),
            'telefono': self.get_telefono(),
            'direcciones': self.get_direcciones(),
            'padres': self.get_datos_padres(),
            'seguros': self.get_seguros_medicos(),
            'educacion': self.get_educacion(),
            'ocupaciones': self.get_ocupaciones(),
            'vivienda':self.get_vivienda(),
            'servicio_sanitario':self.get_servicio_sanitario(),
            'servicio_basico':self.get_servicio_basico(),
            'correo':self.get_correo_electronico(),
            })
        return context


class PacienteFichaClinicaPDF(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        template = get_template('pacientes/ficha_clinica_pdf.html')

        paciente = Paciente.objects.get(pk=self.kwargs['paciente_id'])
        telefono = Telefono.objects.get(paciente__id=self.kwargs['paciente_id'])
        direcciones = Direccion.objects.filter(paciente__id=self.kwargs['paciente_id'])
        padres = PacientePadre.objects.filter(paciente__id=self.kwargs['paciente_id'])

        if PacienteSeguroMedico.objects.filter(paciente=paciente).exists():
            seguros = PacienteSeguroMedico.objects.filter(paciente__id=self.kwargs['paciente_id'])
        else:
            seguros = ['']

        if PacienteNivelEducativo.objects.filter(paciente__id=self.kwargs['paciente_id']).exists():
            educacion = PacienteNivelEducativo.objects.get(paciente__id=self.kwargs['paciente_id'])
        else:
            educacion = ['']
        ocupaciones = PacienteOcupacion.objects.filter(paciente__id=self.kwargs['paciente_id'])

        if Vivienda.objects.filter(paciente=paciente).exists():
            vivienda = Vivienda.objects.filter(paciente__id=self.kwargs['paciente_id'])[0]
        else:
            vivienda = ['']

        if CorreoElectronico.objects.filter(paciente=paciente).exists():
            correos = CorreoElectronico.objects.filter(paciente__id=self.kwargs['paciente_id'])
        else:
            correos = ['']

        if ServicioSanitario.objects.filter(paciente=paciente).exists():
            servicio_sanitario = ServicioSanitario.objects.filter(paciente__id=self.kwargs['paciente_id'])[0]
        else:
            servicio_sanitario = ['']

        if ServicioBasicos.objects.filter(paciente=paciente).exists():
            servicio_basico = ServicioBasicos.objects.filter(paciente__id=self.kwargs['paciente_id'])
        else:
            servicio_basico = ['']


        context = {
            'paciente': paciente,
            'telefono': telefono,
            'direcciones': direcciones,
            'padres': padres,
            'seguros': seguros,
            'educacion': educacion,
            'ocupaciones': ocupaciones,
            'correos':correos,
            'vivienda':vivienda,
            'servicio_sanitario':servicio_sanitario,
            'servicio_basico':servicio_basico,
        }

        html = template.render(context)
        pdf = render_to_pdf('pacientes/ficha_clinica_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class ConsultaHistoriaByPacienteView(LoginRequiredMixin, TemplateView):
    """
    permite obtener la historia clinica completa del paciente.
    """
    template_name = 'consultorios/consulta/consulta_historia_paciente.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        pacientes = Paciente.objects.get(pk=self.kwargs['paciente_id'])

        # obtenemos la consuta detalle
        #detalle = ConsultaDetalle.objects.get(pk=self.kwargs['detalle_id'])

        # actualizamos el estado del detalle de la consulta a "en proceso"


        anamnesis = Anamnesis.objects.filter(paciente__id=self.kwargs['paciente_id']).order_by('pk')

        diagnosticos = Diagnostico.objects.filter(paciente__id=self.kwargs['paciente_id']).order_by('pk')

        evoluciones = EvolucionPaciente.objects.filter(paciente__id=self.kwargs['paciente_id']).order_by('pk')

        ordenes = ConsultaOrdenEstudio.objects.filter(paciente__id=self.kwargs['paciente_id']).order_by('pk')

        prescripciones = ConsultaPrescripcion.objects.filter(paciente__id=self.kwargs['paciente_id']).order_by('pk')

        tratamientos = Tratamiento.objects.filter(paciente__id=self.kwargs['paciente_id']).order_by('pk')

        context.update({
            'diagnosticos': diagnosticos,
            'evoluciones': evoluciones,
            'ordenes': ordenes,
            'prescripciones': prescripciones,
            'tratamientos': tratamientos,
            'anamnesis': anamnesis,
        })

        # return super(TemplateView, self).render_to_response(context)
        return render(request=request, template_name=self.template_name, context=context)




