import calendar
import datetime
from django.contrib import messages
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from multiprocessing import get_context, context

from apps.agendamientos.functions import cancelar_agenda
from apps.agendamientos.models import Agenda, AgendaDetalle, EstadoAgenda

# Create your views here.

from apps.agendamientos.forms import AgendaForm, AgendaDetalleForm
from apps.agendamientos.queries import get_agenda_medico_especialidad, get_agenda_detalle_orden, \
    get_agenda_detalle_lista_by_agenda, get_agenda_detalle_confirmar, \
    agenda_detalle_update_orden
from apps.agendamientos.utils import get_fecha_agendamiento_siguiente
from apps.consultorios.models import HorarioMedico, DiasSemana, Especialidad, Medico, Turno
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.internaciones.models import Medicamento
from apps.pacientes.models import Paciente
# def index(request):
#     # form = AgendaForm()
#     return render(request, 'agendamientos/index.html')


def agenda_nuevo(request, origen):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():  # consulta si el formulario es valido
            data = form.save()  # guarda
            messages.success(request, 'Datos guardados')
            return redirect('agendamientos:agenda_detalle', data.id, origen)
    else:
        print("metodo noes POST")
        form = AgendaForm()
    return render(request, 'agendamientos/agenda_form.html', {'form': form, 'origen': origen})


# def agenda_list(request):
#     agenda = Agenda.objects.all().order_by('id')
#     contexto = {'agendas':agenda}
#     return render(request, 'agendamientos/agenda_list.html', contexto)


class AgendaList(TemplateView):
    model = Agenda
    template_name = '/agendamientos/agenda_list.html'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        fecha_desde = request.GET.get('desde', None)
        fecha_hasta = request.GET.get('hasta', None)

        now = datetime.datetime.now()
        first_day = datetime.date(now.year, now.month, 1)

        if not fecha_desde or not fecha_hasta:
            fecha_desde = first_day
            fecha_hasta = now
        else:
            agendas = Agenda.objects.filter(fecha=fecha_desde)


# class AgendaByFechaList(ListView):
#     model = Agenda
#     template_name = '/agendamientos/agenda_by_fecha_list.html'
#     paginate_by = 15
#     model_form = AgendaForm
#
#     def get_context_data(self, **kwargs):
#         pass


class AgendaByFechaList(LoginRequiredMixin, TemplateView):
    template_name = 'agendamientos/agenda_by_fecha_list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        now = datetime.datetime.now()
        first_day = datetime.date(now.year, now.month, 1)
        p_fecha_desde = request.GET.get('fecha_desde', None)
        p_fecha_hasta = request.GET.get('fecha_hasta', None)
        p_especialidad = request.GET.get('especialidad', None)
        p_medico = request.GET.get('medico', None)
        p_estado = request.GET.get('estado', None)
        if p_fecha_desde:
            fecha_desde = datetime.datetime.strptime(p_fecha_desde, '%d/%m/%Y').date()
        else:
            fecha_desde = first_day

        if p_fecha_hasta:
            fecha_hasta = datetime.datetime.strptime(p_fecha_hasta, '%d/%m/%Y').date()
        else:
            fecha_hasta = now.date()

        list_agenda = Agenda.objects.filter(fecha__gte=fecha_desde, fecha__lte=fecha_hasta)

        if p_especialidad:
            especialidad = Especialidad.objects.get(pk=p_especialidad)
            list_agenda = list_agenda.filter(especialidad=especialidad)
        else:
            especialidad = None

        if p_medico:
            medico = Medico.objects.get(pk=p_medico)
            list_agenda = list_agenda.filter(medico=medico)
        else:
            medico = None

        if p_estado:
            estado = EstadoAgenda.objects.get(codigo=p_estado)
            list_agenda = list_agenda.filter(estado=estado)
            print(p_estado, estado, list_agenda, len(list_agenda))
        else:
            estado = None

        list_agenda = list_agenda.order_by('fecha')  # ordenamos

        context.update({'list_agenda': list_agenda,
                        'fecha_desde': fecha_desde,
                        'fecha_hasta': fecha_hasta,
                        'especialidad_select': especialidad if especialidad else None,
                        'especialidades': Especialidad.objects.all(),
                        'medico_select': medico if medico else None,
                        'medicos': Medico.objects.all(),
                        'estado_select': estado if estado else None,
                        'estados': EstadoAgenda.objects.all(),
                        'origen': 2
                        })

        return super(TemplateView, self).render_to_response(context)



# def agenda_edit(request, agenda_id):
#     agenda = Agenda.objects.get(id=agenda_id)
#     if request.method == 'GET':
#         form = AgendaForm(instance=agenda)
#         print("entro")
#     else:
#         form = AgendaForm(request.POST, instance=agenda)
#         if form.is_valid():
#             form.save()
#             print("entro")
#         return redirect('agendamientos:agenda_listar')
#     return render(request, 'agendamientos/agenda_form.html', {'form':form})


class AgendaUpdate(UpdateView):
    model = Agenda
    print("entro")
    form_class = AgendaForm
    template_name = 'agendamientos/agenda_form.html'
    success_url = reverse_lazy('agendamientos:agenda_listar')


def agenda_delete(request, id_agenda):
    agenda = Agenda.objects.get(id=id_agenda)
    if request.method == 'POST':
        agenda.delete()
        return redirect('agendamientos:agenda_listar')
    return render(request, 'agendamientos/agenda_delete.html', {'agenda': agenda})


def prueba(request):
    # agenda = Agenda.objects.all().order_by('id')
    # contexto = {'agendas':agenda}
    return render(request, 'base/prueba.html')


class AgendaDetalleList(ListView):
    model = AgendaDetalle
    template_name = 'agendamientos/agenda_detail.html'


class AgendaDetalleCreate(CreateView):
    model = AgendaDetalle()
    form_class = AgendaDetalleForm
    template_name = 'agendamientos/agenda_detalle_form.html'
    success_url = reverse_lazy('agendamientos:agenda_detalle_listar')


def agenda_detalle_crear2(request, agenda_id, paciente_id, origen):
    agenda_actual = Agenda.objects.get(pk=agenda_id)
    orden = get_agenda_detalle_orden(agenda_id)
    dias = DiasSemana.objects.all()
    paciente = Paciente.objects.get(pk=paciente_id)

    # necesito conocer el número de día para obtener el horario medico de ese día
    dia_semana = agenda_actual.fecha.weekday() + 2
    if dia_semana == 8:
        dia_semana = 1
    dia_horario = dias.filter(id=dia_semana)[0]
    print("medico:", agenda_actual.medico, "dia_semana:", dia_horario, "turno: ", agenda_actual.turno) # borrar
    try:
        horario_medico = HorarioMedico.objects.get(medico=agenda_actual.medico, dia_semana=dia_horario, turno=agenda_actual.turno)
    except ObjectDoesNotExist:
        messages.error(request, "No se encuentra Horario Médico para el Dr. %s. (Día: %s. Turno: %s) " % (agenda_actual.medico, dia_horario, agenda_actual.turno))
        return redirect('agendamientos:agenda_detalle_paciente_list', agenda_actual.id, origen)

    if orden > horario_medico.cantidad:
        agenda_nueva = Agenda(medico=agenda_actual.medico,
                              fecha=get_fecha_agendamiento_siguiente(agenda_actual),
                              turno=agenda_actual.turno, especialidad=agenda_actual.especialidad,
                              cantidad=agenda_actual.cantidad, estado=EstadoAgenda.objects.get(codigo="P"))
        agenda_nueva.save()
        orden = 1
        agenda_actual = agenda_nueva

    AgendaDetalle.objects.create(paciente=paciente, agenda=agenda_actual, orden=orden)

    return redirect('agendamientos:agenda_detalle', agenda_actual.id, origen)


def agenda_detalle_confirmar(request, agenda_id, paciente_id, origen):
    agenda_actual = Agenda.objects.get(pk=agenda_id)
    agenda_detalle = AgendaDetalle.objects.get(agenda=agenda_id, paciente= paciente_id)
    orden = get_agenda_detalle_confirmar(agenda_id)
    agenda_detalle_update_orden(orden, agenda_detalle)

    return redirect('agendamientos:agenda_detalle', agenda_actual.id, origen)


def agenda_detalle_crear(request, agenda_id, paciente_id):
    agenda_actual = Agenda.objects.get(pk=agenda_id)
    orden = get_agenda_detalle_orden(agenda_id)
    dias = DiasSemana.objects.all()
    if request.method == 'POST':
        form = AgendaDetalleForm(request.POST)
        if form.is_valid():
            try:
                agenda_detalle = form.save(commit=False)
                # necesito conocer el número de día para obtener el horario medico de ese día
                dia_semana = agenda_actual.fecha.weekday() + 2
                if dia_semana == 8:
                    dia_semana = 1
                dia_horario = dias.filter(id=dia_semana)[0]
                print("dia",dia_horario)
                horario_medico = HorarioMedico.objects.get(medico=agenda_actual.medico, dia_semana=dia_horario)
                # si la cantidad es superior a la establecida en el parámetro, se agrega una nueva agenda
                if orden > horario_medico.cantidad:
                    agenda_nueva = Agenda(medico=agenda_actual.medico,
                                          fecha=get_fecha_agendamiento_siguiente(agenda_actual),
                                          turno=agenda_actual.turno, especialidad=agenda_actual.especialidad,
                                          cantidad=agenda_actual.cantidad, estado=EstadoAgenda.objects.get(codigo="P"))
                    agenda_nueva.save()
                    orden = 1
                    agenda_actual = agenda_nueva
                agenda_detalle.agenda = agenda_actual
                agenda_detalle.orden = orden

                # valido que el paciente no esté ya registrado en esa agenda
                if bool(AgendaDetalle.objects.filter(agenda=agenda_actual, paciente=agenda_detalle.paciente)):
                    messages.error(request, "El paciente %s ya se encuentra registrado en esta agenda."
                                   % agenda_detalle.paciente)
                    return redirect('agendamientos:agenda_detalle', agenda_actual.id)

                agenda_detalle.save()
            except ObjectDoesNotExist:
                messages.error(request, "No se encuentra Horario Médico para el Dr. %s " % agenda_actual.medico)
            return redirect('agendamientos:agenda_detalle', agenda_actual.id)
        else:
            form = AgendaDetalleForm(request.POST)
            contexto = {'agenda': agenda_actual, 'form': form}
            return render(request, 'agendamientos/agenda_detalle_form.html', contexto)
    else:
        form = AgendaDetalleForm()
        contexto = {'agenda': agenda_actual, 'form': form}
        return render(request, 'agendamientos/agenda_detalle_form.html', contexto)


def agenda_detalle_edit(request, agenda_id, agenda_detalle_id):
    agenda_detalle = AgendaDetalle.objects.get(id=agenda_detalle_id)
    if request.method == 'GET':
        form = AgendaDetalleForm(instance=agenda_detalle)
    else:
        form = AgendaDetalleForm(request.POST, instance=agenda_detalle)
        if form.is_valid():
            form.save()
        return redirect('agendamientos:agenda_detalle', agenda_id)
    contexto = {'agenda': agenda_id, 'form': form}
    return render(request, 'agendamientos/agenda_detalle_form.html', contexto)


# def agendaDetalleCreate(request):
#     if request.method == 'POST':
#         form = AgendaDetalleForm(request.POST)
#         print('oguahe koape')
#         global agendaCodigo
#         print("codigo de agenda ",agendaCodigo)
#         if form.is_valid():#consulta si el formulario es valido
#             agendaDetalle = form.save(commit=False)
#             agendaDetalle.agenda_id = agendaCodigo
#             agendaDetalle.save()  #guarda
#             messages.success(request, 'Datos guardados')
#             return redirect ('agendamientos:agenda_detalle', agendaCodigo)
#                 # redirect ('agendamientos:index')
#     else:
#         print("metodo noes POST")
#         form = AgendaDetalleForm()
#     return render(request, 'agendamientos/agenda_detail.html', {'form': form})


class AgendaDetalleUpdate(UpdateView):
    model = AgendaDetalle
    form_class = AgendaDetalleForm
    template_name = 'agendamientos/agenda_detalle_form.html'
    success_url = reverse_lazy('agendamientos:agenda_detalle_listar')


class AgendaDetalleDelete(DeleteView):
    model = AgendaDetalle
    template_name = 'agendamientos/agenda_cancelar.html'
    success_url = reverse_lazy('agendamientos:agenda_detalle_listar')


def agenda_detalle_delete(request, agenda_detalle_id):
    agenda_detalle = AgendaDetalle.objects.get(id=agenda_detalle_id)
    if request.method == 'GET':
        agenda = agenda_detalle.agenda_id
        agenda_detalle.delete()
        return redirect('agendamientos:agenda_detalle', agenda)
    else:
        form = AgendaDetalleForm()
    return render(request, 'agendamientos/agenda_detalle_form.html', {'form': form})


class AgendaDetalleDetail(DetailView):
    model = AgendaDetalle

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AgendaDetalleDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['agenda_list'] = AgendaDetalle.objects.all()
        return context


def agenda_detalle_list(request, agenda_id, origen):
    agenda = Agenda.objects.get(pk=agenda_id)
    agenda_detalle = get_agenda_detalle_lista_by_agenda(agenda_id)

    if request.method == 'GET':
        form = AgendaForm(instance=agenda)
    else:
        form = AgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            form.save()

    # dependiendo del valor de 'origen' redirige a tal o cual url de donde se solicitó
    # TODO: agregar más si fuera necesario
    if origen == str(1):
        # redirige a agendar por fecha disponible
        origen_url = '/agendamientos/agendas/'
    elif origen == str(2):
        # redirige a agendas por rango de fechas
        origen_url = '/agendamientos/agenda_fecha/'
    else:
        # DEFAULT: redirige a agendar por fecha disponible
        origen_url = '/agendamientos/agendas/'

    contexto = {'agenda': agenda, 'agenda_detalle': agenda_detalle, 'origen': origen, 'origen_url': origen_url,
                'form': form}
    return render(request, 'agendamientos/agenda_detalle_by_agenda.html', contexto)


class AgendaDetalleCreateView(CreateView):
    model = AgendaDetalle
    template_name = "agendamientos/agenda_detalle_form.html"
    form_class = AgendaDetalleForm
    success_url = reverse_lazy('agendamientos:agenda_detalle_crear')

    def get_context_data(self, **kwargs):
        agenda = Agenda.objects.get(id=kwargs['pk'])

    def form_valid(self, form_class):
        form_class.instance.user_id = self.request.user.id
        return super(AgendaDetalleCreateView, self).form_valid(form_class)


def agenda_especialidad(request):
    if request.method == 'GET':
        p_especialidad = request.GET.get('especialidad', None)
        p_medico = request.GET.get('medico', None)
        p_turno = request.GET.get('turno', None)
        if p_especialidad:
            especialidad=Especialidad.objects.get(pk=p_especialidad)
        else:
            especialidad=None
        if p_medico:
            medico=Medico.objects.get(pk=p_medico)
        else:
            medico=None
        if p_turno:
            turno=Turno.objects.get(pk=p_turno)
        else:
            turno=None
        agenda = get_agenda_medico_especialidad(p_especialidad, p_medico, p_turno)
    else:
        form = AgendaForm()

    context = ({'especialidad_select': especialidad if especialidad else None,
                'especialidades': Especialidad.objects.all(),
                'medico_select': medico if medico else None,
                'medicos': Medico.objects.all(),
                'turno_select': turno if turno else None,
                'turnos': Turno.objects.all(),
                'object_list': agenda,
                'origen': 1})

    return render(request, 'agendamientos/agenda_especialidad_list.html', context)


@transaction.atomic
def agenda_cancelar(request, agenda_id, origen):
    tipo = request.POST["tipo"]  # TODO quitar el parametro 'origen'
    print("tipo: ", tipo)  # borrar
    agenda = Agenda.objects.get(id=agenda_id)
    if request.method == 'POST':
        agenda = cancelar_agenda(agenda.id, tipo)
        return JsonResponse(serializers.serialize("json", [agenda]), safe=False)


class PacienteByAgenda(LoginRequiredMixin, ListView):
    model = Paciente
    context_object_name = 'pacientes'
    template_name = 'agendamientos/agenda_detalle_paciente_list.html'

    def get_queryset(self):
        return Paciente.objects.exclude(agendadetalle__agenda=self.kwargs['agenda_id'])

    def get_context_data(self, **kwargs):
        context = super(PacienteByAgenda, self).get_context_data(**kwargs)
        origen = self.kwargs['origen']
        context.update({'agenda': Agenda.objects.get(pk=self.kwargs['agenda_id']), 'origen': origen})
        return context





