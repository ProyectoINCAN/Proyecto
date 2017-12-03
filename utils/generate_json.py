from django.core import serializers

from apps.agendamientos.models import EstadoAgenda
from apps.consultorios.models import Departamento, DiasSemana, Especialidad, EstadoConsulta, EstadoConsultaDetalle, \
    GrupoAtencion, OrdenEstudio, TipoMedicamento, Turno
from apps.pacientes.models import Agua, Area, Barrio, Departamento, Desague, Distrito, EliminacionBasura, EstadoCivil, \
    Nacionalidad, Pais, NivelEducativo, Pared, Piso, Profesion, SeguroMedico, ServicioBasico, Sexo, SituacionLaboral, \
    Techo, TipoCorreoElectronico, TipoDoc, TipoTelefono
from apps.seguridad.models import RegionSanitaria

# TODO: Probar la generación


def generar_json_agendamientos():
    datos = EstadoAgenda.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo


def generar_json_consultorios():
    datos = Departamento.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = DiasSemana.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Especialidad.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = EstadoConsulta.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = EstadoConsultaDetalle.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = EstadoConsultaDetalle.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = GrupoAtencion.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = OrdenEstudio.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = TipoMedicamento.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Turno.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo


def generar_json_internaciones():
    # TODO: agregar los datos
    pass


def generar_json_pacientes():
    datos = Agua.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Area.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Pais.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Nacionalidad.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Departamento.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Distrito.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Barrio.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Agua.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Desague.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = EliminacionBasura.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = EstadoCivil.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = NivelEducativo.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Pared.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Piso.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Profesion.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = SeguroMedico.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = ServicioBasico.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Sexo.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = SituacionLaboral.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = Techo.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = TipoCorreoElectronico.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = TipoDoc.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = TipoTelefono.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo

    datos = RegionSanitaria.objects.all()
    data = serializers.serialize(datos, 'json')
    print(data)  # TODO: guardar directamente en un archivo
