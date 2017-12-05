from django.core import serializers
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from apps.principal.forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from django.db import connection
# Create your views here.
from apps.pacientes.models import Distrito, Nacionalidad, Departamento, Barrio
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import render, redirect


def distrito(request, id_departamento):
    distrito = Distrito.objects.filter(departamento=id_departamento).order_by('id')
    data = serializers.serialize('json', distrito)
    return JsonResponse(data, safe=False)


def distritoByDepartamento(request, departamento=[]):
    distrito = Distrito.objects.get(departamento=departamento).order_by('id')
    data = serializers.serialize('json', distrito)
    return JsonResponse(data, safe=False)


def nacionalidad(request, nacionalidad_id):
    nacionalidad = Nacionalidad.objects.filter(id=nacionalidad_id)
    data = serializers.serialize('json', nacionalidad)
    return JsonResponse(data, safe=False)


def departamento(request, pais_codigo):
    """

    :param request:
    :param pais_codigo:
    :return:
    """
    print('paisa', pais_codigo)
    departamento = Departamento.objects.filter(pais=pais_codigo).values_list("id")
    depa =[]
    for dep in departamento:
        depa.append(dep[0])
    print("depa", depa)
    # print("departmento", depa.split(','))
    print("distrito", departamento)
    newList = [ str(t) for t in depa ]
    eje = ', '.join(newList)
    print("new", eje)
    query = '''SELECT *
        FROM pacientes_departamento dep
        join pacientes_distrito dist on dist.departamento_id = dep.id
        WHERE dep.id in ('''+eje+''')'''
    cursor = connection.cursor()
    cursor.execute(query)
    distrito = cursor.fetchall()
        # Distrito.objects.filter(departamento__in=departamento).order_by("departamento_id", "nombre").value_list('departamento.nombre')
    data = distrito
    return JsonResponse(json.dumps(data), safe=False)


def barrio(request, id_distrito):
    barrio = Barrio.objects.filter(distrito=id_distrito).order_by('id')
    data = serializers.serialize('json', barrio)
    return JsonResponse(data, safe=False)


class UsuarioList(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'usuarios'
    template_name = 'principal/usuarios/usuario_list.html'

    def get_usuarios(self):
        usuarios = User.objects.filter(is_superuser=False)
        listado_usuarios = []
        for usu in usuarios:
            grupo = usu.groups.all()
            listado_usuarios.append({
                'id': usu.id,
                'username': usu.username,
                'last_name': usu.last_name,
                'first_name': usu.first_name,
                'activo': usu.is_active,
                'grupo': grupo.values()[0]['name']
            })
        return listado_usuarios

    def get_context_data(self, **kwargs):
        context = super(UsuarioList, self).get_context_data(**kwargs)
        context.update({'usuarios': self.get_usuarios()})
        return context


class UsuarioCreateView(CreateView):
    model = User
    template_name = 'principal/usuarios/usuario_form.html'
    form_class = UserForm

    def get_success_url(self):
        messages.success(self.request, "Se ha creado un nuevo usuario.")
        return reverse('principal:user_list_global')


def user_update_view(request, user_id):
    # if this is a POST request we need to process the form data
    usuario = User.objects.get(pk=user_id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserEditForm(request.POST, instance=usuario)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('principal:user_list_global'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserEditForm(instance=usuario)

    extra_context = {
        'form': form,
        'usuario': usuario
    }

    return render(request, 'principal/usuarios/usuario_form.html', extra_context)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "principal/usuarios/usuario_eliminar.html"
    pk_url_kwarg = 'user_id'
    context_object_name = 'usuario'

    def post(self, request, *args, **kwargs):
        """desactivamos al usuario"""
        user = User.objects.get(pk=self.kwargs['user_id'])
        user.is_active = False
        user.save()
        messages.info(self.request, 'Se ha desactivado al usuario {}'.format(user.username))

        return HttpResponseRedirect(reverse('principal:user_list_global'))

    def get_success_url(self):
        return reverse('principal:user_list_global')


class UserUpdatePasswordView(LoginRequiredMixin, UpdateView):
    template_name = 'principal/usuarios/pass-change-form.html'
    model = User
    context_object_name = 'usuario'
    pk_url_kwarg = 'user_id'
    form_class = UserPasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(UserUpdatePasswordView, self).get_form_kwargs()
        kwargs.update({
            'user': User.objects.get(pk=self.kwargs['user_id']),
        })
        return kwargs

    def get_success_url(self):
        return reverse('principal:user_update_global', kwargs={'user_id': self.kwargs['user_id']})

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())





