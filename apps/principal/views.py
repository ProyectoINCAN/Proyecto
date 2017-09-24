from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render
from django.db import connection
# Create your views here.
from apps.pacientes.models import Distrito, Nacionalidad, Departamento
import json


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

