from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from apps.consultorios.forms import MedicoModelForm, UserModelForm, Medico2ModelForm
from apps.consultorios.models import Medico
from apps.pacientes.models import Paciente


class MedicoList(ListView):
    model = Medico
    template_name = 'consultorios/medico_list.html'


class MedicoCreate(CreateView):
    model = Medico
    template_name = 'consultorios/medico_form.html'
    form_class = MedicoModelForm
    second_form_class = UserModelForm
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
    form_class = UserModelForm
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


class Medico2Create(CreateView):
    model = Medico
    template_name = 'consultorios/medico2_form.html'
    form_class = Medico2ModelForm
    success_url = reverse_lazy('consultorios:medico_listar')

    # def get_context_data(self, **kwargs):
    #     context = super(MedicoCreate, self).get_context_data(**kwargs)
    #     if 'form' not in context:
    #         context['form'] = self.form_class(self.request.GET)
    #     if 'form2' not in context:
    #         context['form2'] = self.second_form_class(self.request.GET)
    #     return context

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object
    #     form = self.form_class(request.POST)
    #     form2 = self.second_form_class(request.POST)
    #     if form.is_valid() and form2.is_valid():
    #         medico = form.save(commit=False)
    #         user = form2.save(commit=True)
    #         medico.usuario = user
    #         print("usuario = " + medico.usuario.username + " contraseña = " + medico.usuario.password + " id = " + str(medico.usuario.id))
    #         medico.save()
    #         return HttpResponseRedirect(self.get_success_url())
    #     else:
    #         return self.render_to_response(self.get_context_data(form=form, form2=form2))