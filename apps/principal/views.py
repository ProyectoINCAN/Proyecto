from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from apps.pacientes.models import Distrito


def distrito(request):
    departamento = request.GET.get('departamento', None)
    print('entro en distrito')
    data = {
        'distrito' : Distrito.objects.filter(departamento=departamento)
    }
    return JsonResponse(data)