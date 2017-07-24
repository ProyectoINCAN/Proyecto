from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from apps.agendamientos.models import Agenda, AgendaDetalle

# Create your views here.

from apps.agendamientos.forms import AgendaForm, AgendaDetalleForm

agendaCodigo = 0
def index(request):
    # form = AgendaForm()
    return render(request, 'agendamientos/index.html')


def agenda_nuevo(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        print('oguahe koape')
        if form.is_valid():#consulta si el formulario es valido
            form.save()  #guarda
            messages.success(request, 'Datos guardados')
            return redirect ('agendamientos:agenda_listar')
                # redirect ('agendamientos:index')
    else:
        print("metodo noes POST")
        form = AgendaForm()

    return render(request, 'agendamientos/agenda_form.html', {'form': form})


# def agenda_list(request):
#     agenda = Agenda.objects.all().order_by('id')
#     contexto = {'agendas':agenda}
#     return render(request, 'agendamientos/agenda_list.html', contexto)


class AgendaList(ListView):
    model = Agenda
    template_name = '/agendamientos/agenda_list.html'
    paginate_by = 15

#
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
    return render(request, 'agendamientos/agenda_delete.html', {'agenda':agenda})


def prueba(request):
    # agenda = Agenda.objects.all().order_by('id')
    # contexto = {'agendas':agenda}
    return render(request, 'base/prueba.html')



class AgendaDetalleList(ListView):
    model = AgendaDetalle
    template_name = 'agendamientos/agenda_detail.html'


class AgendaDetalleCreate(CreateView):
    model = AgendaDetalle()
    print("hola")
    form_class = AgendaDetalleForm
    template_name = 'agendamientos/agenda_detalle_form.html'
    success_url = reverse_lazy('agendamientos:agenda_detalle_listar')


def agendaDetalleCreate(request):
    if request.method == 'POST':
        form = AgendaDetalleForm(request.POST)
        print('oguahe koape')
        global agendaCodigo
        print("codigo de agenda ",agendaCodigo)
        if form.is_valid():#consulta si el formulario es valido
            agendaDetalle = form.save(commit=False)
            agendaDetalle.agenda_id = agendaCodigo
            agendaDetalle.save()  #guarda
            messages.success(request, 'Datos guardados')
            return redirect ('agendamientos:agenda_detalle', agendaCodigo)
                # redirect ('agendamientos:index')
    else:
        print("metodo noes POST")
        form = AgendaDetalleForm()
    return render(request, 'agendamientos/agenda_detalle_form.html', {'form': form})

class AgendaDetalleUpdate(UpdateView):
    model = AgendaDetalle
    form_class = AgendaDetalleForm
    template_name = 'agendamientos/agenda_detalle_form.html'
    success_url = reverse_lazy('agendamientos:agenda_detalle_listar')


class AgendaDetalleDelete(DeleteView):
    model = AgendaDetalle
    template_name = 'agendamientos/agenda_detalle_delete.html'
    success_url = reverse_lazy('agendamientos:agenda_detalle_listar')


def agendaDetalleDelete(request, agenda_detalle_id):
    agendaDetalle = AgendaDetalle.objects.get(id=agenda_detalle_id)
    if request.method=='GET':
        agenda = agendaDetalle.agenda_id
        agendaDetalle.delete()
        return redirect('agendamientos:agenda_detalle', agenda)
    else:
        form = AgendaDetalleForm()
    return render(request, 'agendamientos/agenda_detalle_form.html',{'form':form})


class AgendaDetalleDetail(DetailView):

    model = AgendaDetalle

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AgendaDetalleDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['agenda_list'] = AgendaDetalle.objects.all()
        return context


class AgendaAgendaDetalleList(ListView):
    # template_name = 'books/books_by_publisher.html'
    template_name = 'agendamientos/agendaDetalle_by_agenda.html'


    def get_queryset(self):
        print("Jose")
        global agendaCodigo
        self.agenda = get_object_or_404(Agenda, id=self.args[0])

        agendaCodigo = self.agenda.id
        print("fdsagfjh",agendaCodigo)
        return AgendaDetalle.objects.filter(agenda=self.agenda)


# class AgendaDetalleCreate(CreateView):
#     model = AgendaDetalle
#     template_name = 'agendamientos/agenda_detalle_form.html'
#     form_class = AgendaDetalleForm
#     second_form_class = AgendaForm
#     success_url = reverse_lazy('agendamientos:agenda_detalle_listar')
#
#     def get_context_data(self, **kwargs):
#         context = super(AgendaDetalleCreate, self).get_context_data(**kwargs)
#         if 'form' not in context:
#             context['form'] = self.form_class(self.request.GET)
#         if 'form2' not in context:
#             context['form2'] = self.second_form_class(self.request.GET)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object
#         form = self.form_class(request.POST) #AgendaDetalleForm
#         form2 = self.second_form_class(request.POST) #AgendaForm
#         print("llego")
#         print(str(form.is_valid()) + " " + str(form2.is_valid()))
#         if form.is_valid() and form2.is_valid():
#             print("llego2")
#             agenda_detalle = form.save(commit=False)
#             agenda_detalle.agenda = form2.save()
#             agenda_detalle.save()
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return self.render_to_response(self.get_context_data(form=form, form2=form2))
