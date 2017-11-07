

from apps.agendamientos.models import Agenda, EstadoAgenda, AgendaDetalle
from apps.agendamientos.queries import get_max_fecha_disponible
from apps.agendamientos.utils import get_fecha_agendamiento_siguiente


def set_detalle_a_agenda(agenda, agenda_detalles):
    for detalle in agenda_detalles:
        nuevo_detalle = AgendaDetalle(agenda=agenda, paciente=detalle.paciente, orden=detalle.orden,
                                      observacion=detalle.observacion, confirmado=False)
        print("detalle procesado: ", detalle, " nuevo_detalle.agenda.id:", nuevo_detalle.agenda.id, "agenda.id:",agenda.id)
        nuevo_detalle.save()


def cancelar_agenda(agenda_id, tipo):
    """
    Función para cancelar la agenda de un médico
    :param agenda_id: la agenda que se va a cancelar
    :param tipo: tipo de cancelación. Puede ser (tipo=1) la última
    fecha de consulta del médico o (tipo=2) la siguiente fecha inmediata de consulta del médico
    :return:
    """

    # agenda_retornada = None
    if int(tipo) == 1:
        # Última fecha: pasa el agendamiento a la máxima fecha disponible
        agenda = Agenda.objects.get(pk=agenda_id)
        agenda.estado = EstadoAgenda(codigo="C")  # agenda en estado cancelado
        max_fecha_disponible = get_max_fecha_disponible(agenda)
        agenda.fecha = max_fecha_disponible
        nueva_fecha = get_fecha_agendamiento_siguiente(agenda)
        print("nueva fecha:", nueva_fecha)
        nueva_agenda = Agenda(medico=agenda.medico, fecha=nueva_fecha, turno=agenda.turno,
                              especialidad=agenda.especialidad, cantidad=agenda.cantidad,
                              estado=EstadoAgenda.objects.get(codigo="P"))
        agenda.save()
        nueva_agenda.save()
        # relaciona con los detalles
        agenda_detalles = AgendaDetalle.objects.filter(agenda=agenda)
        print("agenda_detalles:", agenda_detalles)  # borrar
        set_detalle_a_agenda(nueva_agenda, agenda_detalles)
        agenda_retornada = nueva_agenda

    else:
        # TIPO 2: Siguiente fecha
        # La nueva fecha es del siguiente día en que atiende el médico. Las siguientes agendas se pasan sucesivamente
        # a la siguiente fecha disponible
        agenda = Agenda.objects.get(pk=agenda_id)
        agendas = Agenda.objects.filter(medico=agenda.medico, especialidad=agenda.especialidad, turno=agenda.turno,
                                        fecha__gte=agenda.fecha, estado=agenda.estado).exclude(fecha=agenda.fecha).order_by('fecha')

        print(agendas)
        # cambio de fecha las agendas posteriores
        for a in agendas:
            print("agenda.id", a.pk, "fecha anterior = ", a.fecha)
            nueva_fecha = get_fecha_agendamiento_siguiente(a)
            print("   nueva fecha = ", nueva_fecha)
            a.fecha = nueva_fecha
            a.save()

        # guardo la agenda nueva con los mismos datos que la agenda cancelada
        nueva_fecha = get_fecha_agendamiento_siguiente(agenda)
        agenda_retornada = Agenda(medico=agenda.medico, especialidad=agenda.especialidad, turno=agenda.turno,
                                  fecha=nueva_fecha, estado=EstadoAgenda.objects.get(codigo="P"))
        agenda_retornada.fecha = nueva_fecha
        agenda_retornada.save()

        # cambio de estado la agenda cancelada
        agenda.estado = EstadoAgenda(codigo="C")
        agenda.save()

    print("agenda retornada = ", agenda_retornada)
    return agenda_retornada


def get_origen_url_agendamiento(origen):
    # dependiendo del valor de 'origen' redirige a tal o cual url de donde se solicitó
    # TODO: agregar más si fuera necesario
    if origen == str(1):
        # redirige a agendar por fecha disponible
        origen_url = '/agendamientos/agendas/'
    elif origen == str(2):
        # redirige a agendas por rango de fechas
        origen_url = '/agendamientos/agenda_fecha/'
    else:
        # DEFAULT: redirige a agendar por fecha disponible
        origen_url = '/agendamientos/agendas/'
    return origen_url