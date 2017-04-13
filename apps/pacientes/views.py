from django.shortcuts import render

# Create your views here.

def index(request):
    #return HttpResponse("Llego al index")
    return render(request, 'pacientes/index_paciente.html')
