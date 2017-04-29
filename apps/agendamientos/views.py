from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

from apps.agendamientos.forms import AgendaForm


# def index(request):
#     return HttpResponse("Index")

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
            return redirect ('agendamientos:index')
                # redirect ('agendamientos:index')
    else:
        print("metodo noes POST")
        form = AgendaForm()

    return render(request, 'agendamientos/agenda_form.html', {'form': form})



