from django.shortcuts import render
from django.core.urlresolvers import reverse
# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.internaciones.models import *
from apps.internaciones.forms import *
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse


class TipoMedicamentoListView(LoginRequiredMixin, ListView):
    model = TipoMedicamento
    context_object_name = 'tipos'
    template_name = 'internacion/tipo_medicamento/tipo_medicamento_list.html'

    def get_queryset(self):
        return TipoMedicamento.objects.filter(habilitado=True)


class TipoMedicamentoCreateView(LoginRequiredMixin, CreateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'internacion/tipo_medicamento/tipo_medicamento_crear.html'

    def get_success_url(self):
        return reverse('internaciones:tipo_medicamento')


class TipoMedicamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'internacion/tipo_medicamento/tipo_medicamento_editar.html'
    pk_url_kwarg = 'tipo_id'

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True})


class TipoMedicamentoDelete(LoginRequiredMixin, DeleteView):
    model = TipoMedicamento
    template_name = "internacion/tipo_medicamento/tipo_medicamento_eliminar.html"
    pk_url_kwarg = 'tipo_id'
    context_object_name = 'tipo'

    def post(self, request, *args, **kwargs):
        tipo = TipoMedicamento.objects.get(pk=kwargs['tipo_id'])
        tipo.habilitado = False
        tipo.save()
        return HttpResponseRedirect(reverse('internaciones:tipo_medicamento'))


class MedicamentoListView(LoginRequiredMixin, ListView):
    model = Medicamento
    context_object_name = 'medicamentos'
    template_name = 'internacion/medicamentos/medicamentos_list.html'

    def get_queryset(self):
        return Medicamento.objects.filter(habilitado=True)


class MedicamentoCreateView(LoginRequiredMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'internacion/medicamentos/medicamentos_form.html'

    def get_success_url(self):
        return reverse('internaciones:medicamentos')


class MedicamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'internacion/medicamentos/medicamentos_form.html'
    pk_url_kwarg = 'medicamento_id'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(MedicamentoUpdateView, self).get_form_kwargs()
        kwargs['tipo'] = Medicamento.objects.filter(pk=self.kwargs['medicamento_id']).values('tipificacion')
        return kwargs

    def get_success_url(self):
        return reverse('internaciones:medicamentos')


class MedicamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Medicamento
    template_name = "internacion/medicamentos/medicamentos_eliminar.html"
    pk_url_kwarg = 'medicamento_id'
    context_object_name = 'medicamento'

    def post(self, request, *args, **kwargs):
        medicamento = Medicamento.objects.get(pk=kwargs['medicamento_id'])
        medicamento.habilitado = False
        medicamento.save()
        return HttpResponseRedirect(reverse('internaciones:medicamentos'))

