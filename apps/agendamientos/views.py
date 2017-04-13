from django.shortcuts import render, redirect

# Create your views here.

from apps.agendamientos.forms import AgendaForm



def agenda_view(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():#consulta si el formulario es valido
            form.save()  #guarda
        return redirect ('paciente:index')
    else:
        form = AgendaForm()

    return  render (request, 'agendamientos/agenda_form.html',{'form':form})
