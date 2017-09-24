from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from apps.consultorios.forms import MedicoForm, UserForm, EvolucionPacienteModelForm, HorarioMedicoModelForm, \
    EnfermeroForm
from apps.consultorios.models import Medico, EvolucionPaciente, HorarioMedico, Enfermero
from apps.pacientes.models import Paciente


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
    medico = Medico.objects.get(id=pk)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente.")
            return redirect("consultorios:medico_listar")
    else:
        form = MedicoForm(instance=medico)
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
    enfermero = Enfermero.objects.get(id=pk)
    if request.method == 'POST':
        form = EnfermeroForm(request.POST, instance=enfermero)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente.")
            return redirect("consultorios:enfermero_listar")
    else:
        form = EnfermeroForm(instance=enfermero)
    contexto = {'form': form}
    return render(request, 'consultorios/enfermero_form.html', contexto)


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
            print("usuario = " + medico.usuario.username + " contraseña = " + medico.usuario.password + " id = " + str(medico.usuario.id))
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
            print("usuario = " + usuario.username + " contraseña = " + usuario.password + " id = " + str(usuario.id))
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


