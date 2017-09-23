from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from apps.pacientes.models import Distrito, Nacionalidad, Departamento


def distrito(request, id_departamento):
    distrito = Distrito.objects.filter(departamento=id_departamento).order_by('id')
    data = serializers.serialize('json', distrito)
    return JsonResponse(data, safe=False)

def distritoByDepartamento(request, departamento):
    distrito = Distrito.objects.get(departamento=departamento).order_by('id')
    data = serializers.serialize('json', distrito)
    return JsonResponse(data, safe=False)


def nacionalidad(request, nacionalidad_id):
    nacionalidad = Nacionalidad.objects.filter(id=nacionalidad_id)
    data = serializers.serialize('json', nacionalidad)
    return JsonResponse(data, safe=False)


def departamento(request, pais_codigo):
    print('paisa', pais_codigo)
    departamento = Departamento.objects.filter(pais=pais_codigo).order_by('id')
    print('departamento', departamento)
    # nacionalidad = Nacionalidad.objects.filter(pais_id=nacionalidad_id)
    data = serializers.serialize('json', departamento)
    return JsonResponse(data, safe=False)

