

from apps.agendamientos.models import Agenda, EstadoAgenda
from apps.agendamientos.queries import get_max_fecha_disponible
from apps.agendamientos.utils import get_fecha_agendamiento_siguiente


def cancelar_agenda(agenda_id, tipo):
    """
    Función para cancelar la agenda de un médico
    :param agenda_id: la agenda que se va a cancelar
    :param tipo: tipo de cancelación. Puede ser (tipo=1) la última
    fecha de consulta del médico o (tipo=2) la siguiente fecha inmediata de consulta del médico
    :return:
    """

    if tipo == 1:
        # pasa el agendamiento a la máxima fecha disponible
        agenda = Agenda.objects.get(pk=agenda_id)
        agenda.estado = EstadoAgenda(codigo="C")  # agenda en estado cancelado
        nueva_fecha = get_max_fecha_disponible(agenda)
        nueva_agenda = Agenda(medico=agenda.medico, fecha=nueva_fecha, turno=agenda.turno,
                              especialidad=agenda.especialidad, cantidad=agenda.cantidad, estado="P")
        agenda.save()
        nueva_agenda.save()
    else:
        # La nueva fecha es del siguiente día en que atiende el médico. Las siguientes agendas se pasan sucesivamente
        # a la siguiente fecha disponible
        agenda = Agenda.objects.get(pk=agenda_id)
        filters = [agenda.medico.id, agenda.especialidad.id, agenda.turno.codigo, agenda.fecha, "P", ]
        agendas = Agenda.objects.raw("""select * from agendamientos_agenda where medico_id = %s and especialidad_id = %s
                                        and turno_id = %s and fecha >= %s and estado = %s order by fecha""", filters)

        for a in agendas:
            print("fecha anterior = ", a.fecha)
            nueva_fecha = get_fecha_agendamiento_siguiente(a.fecha, a.medico)
            print("nueva fecha = ", nueva_fecha)
            a.fecha = nueva_fecha
            a.save()

        agenda.estado = EstadoAgenda(codigo="C")
        agenda.save()
