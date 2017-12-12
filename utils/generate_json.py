import os

import django
from django.core import serializers

from apps.agendamientos.models import EstadoAgenda
from apps.consultorios import models as con
from apps.consultorios.models import DiasSemana, Especialidad, EstadoConsulta, EstadoConsultaDetalle, \
    GrupoAtencion, OrdenEstudio, TipoMedicamento, Turno, OrdenEstudioDetalle
from apps.pacientes import models as pac
from apps.pacientes.models import Agua, Area, Barrio, Desague, Distrito, EliminacionBasura, EstadoCivil, \
    Nacionalidad, Pais, NivelEducativo, Pared, Piso, Profesion, SeguroMedico, ServicioBasico, Sexo, SituacionLaboral, \
    Techo, TipoCorreoElectronico, TipoDoc, TipoTelefono, Dependencia, Etnia, Ocupacion, Vinculo
from apps.principal.models import Establecimiento, ParametroSistema


def generar_archivo_json(data_list, nombre_archivo):
    tmp_file = "tmp.json"
    f = open(tmp_file, "w")
    j_list = []
    for d in data_list:
        if len(d) > 0:
            j = serializers.serialize('json', d, indent=1)
            f.write(j.__str__().replace("[", ",").replace("]", ""))
            j_list.append(j)

    f.close()

    with open(tmp_file, 'r') as tmp:
        lineas = tmp.read().splitlines()
        lineas[0] = "["  # primera línea
        lineas[-1] = "]"  # última linea línea

        archivo = open(nombre_archivo, "w")
        for linea in lineas:
            archivo.writelines(linea + "\n")

        archivo.close()

    os.remove(f.name)
    return j_list


def generar_json_agendamientos():
    data_list = []
    datos = EstadoAgenda.objects.all()
    data_list.append(datos)
    generar_archivo_json(data_list, "default_data_agendamientos.json")


def generar_json_pacientes():
    data_list = []
    datos = Agua.objects.all()
    data_list.append(datos)

    datos = Area.objects.all()
    data_list.append(datos)

    datos = Pais.objects.all()
    data_list.append(datos)

    datos = pac.Departamento.objects.all()
    data_list.append(datos)

    datos = Distrito.objects.all()
    data_list.append(datos)

    datos = Barrio.objects.all()
    data_list.append(datos)

    datos = Dependencia.objects.all()
    data_list.append(datos)

    datos = Desague.objects.all()
    data_list.append(datos)

    datos = EliminacionBasura.objects.all()
    data_list.append(datos)

    datos = EstadoCivil.objects.all()
    data_list.append(datos)

    datos = Etnia.objects.all()
    data_list.append(datos)

    datos = Pais.objects.all()
    data_list.append(datos)

    datos = Nacionalidad.objects.all()
    data_list.append(datos)

    datos = NivelEducativo.objects.all()
    data_list.append(datos)

    datos = Ocupacion.objects.all()
    data_list.append(datos)

    datos = Pared.objects.all()
    data_list.append(datos)

    datos = Piso.objects.all()
    data_list.append(datos)

    datos = Profesion.objects.all()
    data_list.append(datos)

    datos = SeguroMedico.objects.all()
    data_list.append(datos)

    datos = ServicioBasico.objects.all()
    data_list.append(datos)

    datos = Sexo.objects.all()
    data_list.append(datos)

    datos = SituacionLaboral.objects.all()
    data_list.append(datos)

    datos = Techo.objects.all()
    data_list.append(datos)

    datos = TipoCorreoElectronico.objects.all()
    data_list.append(datos)

    datos = TipoDoc.objects.all()
    data_list.append(datos)

    datos = TipoTelefono.objects.all()
    data_list.append(datos)

    datos = Vinculo.objects.all()
    data_list.append(datos)

    generar_archivo_json(data_list, "default_data_pacientes.json")


def generar_json_principal():

    # estos en raw porque tuvo problemas
    data_list = []
    datos = []

    for dato in Establecimiento.objects.raw("select * from seguridad_establecimiento"):
        datos.append(dato)
    data_list.append(datos)

    for dato in ParametroSistema.objects.raw("""select * from seguridad_parametrosistema"""):
        datos.append(dato)
    data_list.append(datos)

    generar_archivo_json(data_list, "default_data_principal.json")


def generar_json_consultorios():
    data_list = []
    datos = con.Departamento.objects.all()
    data_list.append(datos)

    datos = DiasSemana.objects.all()
    data_list.append(datos)

    datos = Especialidad.objects.all()
    data_list.append(datos)

    datos = EstadoConsulta.objects.all()
    data_list.append(datos)

    datos = EstadoConsultaDetalle.objects.all()
    data_list.append(datos)

    datos = GrupoAtencion.objects.all()
    data_list.append(datos)

    datos = TipoMedicamento.objects.all()
    data_list.append(datos)

    datos = OrdenEstudio.objects.all()
    data_list.append(datos)

    datos = OrdenEstudioDetalle.objects.all()
    data_list.append(datos)

    datos = Turno.objects.all()
    data_list.append(datos)

    data_list.append(datos)
    generar_archivo_json(data_list, "default_data_consultorios.json")
