from collections import namedtuple

from django.db import connection

from apps.agendamientos.models import Agenda


def get_agenda_medico_especialidad():
    query = '''
        select max(agenda.id) as agenda_id, max(agenda.fecha) as fecha, agenda.cantidad, agenda.estado_id as estado_agenda,
        agenda.turno_id, turno.nombre as turno,
        medico.id medico_id, medico.nombres||', '||medico.apellidos as medico,
        especialidad.id as especialidad_id, especialidad.nombre as especialidad
        from agendamientos_agenda agenda
        join consultorios_medico medico on (medico.id = agenda.medico_id)
        join consultorios_especialidad especialidad on (especialidad.id = agenda.especialidad_id)
        join consultorios_turno turno on agenda.turno_id = turno.codigo
        where agenda.estado_id = 'P'
        group by agenda.cantidad, agenda.estado_id, agenda.turno_id, turno.nombre,
        medico.id, medico.nombres, medico.apellidos, especialidad.id, especialidad.nombre
        order by fecha, medico.apellidos, medico.nombres, especialidad.nombre
        '''
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    lista = []
    for elemento in results:
        lista.append(elemento)

    return lista


def get_agenda_detalle_orden(agenda_id):
    query = '''select coalesce(max(detalle.orden), 0)+1 as orden
        from agendamientos_agenda agenda
        join agendamientos_agendadetalle detalle on agenda.id = detalle.agenda_id
        where agenda.id = %s
        '''
    filters = [agenda_id]
    cursor = connection.cursor()
    cursor.execute(query, filters)
    orden = cursor.fetchone()[0]
    return orden


def get_max_fecha_disponible(agenda):
    """
    Obtiene la máxima fecha disponible de agendamiento para un médico
    :param agenda:
    :return:
    """
    filters = (agenda.medico.id, agenda.especialidad.id, agenda.turno.codigo, 'P',)
    query = """
    select max(fecha) as fecha from agendamientos_agenda
    where medico_id = %s and especialidad_id = %s and turno_id = %s and estado_id = %s
    """
    cursor = connection.cursor()
    cursor.execute(query, filters)
    result = cursor.fetchone()
    return result[0]


def get_agenda_detalle_lista_by_agenda(agenda_id):
    query = '''select ag_detalle.orden, paciente.nro_doc, paciente.nombres, paciente.apellidos,
    cast(extract(year  from age(paciente.fecha_nacimiento))as integer) as anho, distrito.nombre,
    tipo_tel.descripcion, telefono.numero, ag_detalle.observacion
    from pacientes_paciente paciente
    left join pacientes_distrito distrito on distrito.id = paciente.distrito_id
    left join pacientes_telefono telefono on telefono.paciente_id = paciente.id
    left join pacientes_tipotelefono tipo_tel on tipo_tel.codigo = telefono.tipo_id
    join agendamientos_agendadetalle ag_detalle on ag_detalle.paciente_id = paciente.id
    join agendamientos_agenda agenda on agenda.id = ag_detalle.agenda_id
    where agenda.id  = %s
        '''
    filters = [agenda_id]
    cursor = connection.cursor()
    cursor.execute(query, filters)
    agenda_detalle = cursor.fetchall()
    print('agenda', agenda_detalle)
    return agenda_detalle

# pruebas
# tmp_agenda = Agenda.objects.get(pk=1)
# r = get_max_fecha_disponible(tmp_agenda)
# print("result = ", r)
