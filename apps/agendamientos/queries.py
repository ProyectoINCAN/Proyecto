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
        order by especialidad.nombre
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
    cursor = connection.cursor()
    cursor.execute(query, agenda_id)
    orden = cursor.fetchone()[0]
    return orden
