from datetime import date, timedelta

from apps.consultorios.models import HorarioMedico, DiasSemana


def get_fecha_agendamiento_siguiente(agenda):
    """
    Retorna la siguiente fecha disponible de agendamiento del médico para casos de cancelación de agenda

    :param agenda: agenda que se cancela
    :return: fecha
    """

    horario_medico = HorarioMedico.objects.filter(medico=agenda.medico, )
    dias_consultorio = []
    for horario in horario_medico:
        dias_consultorio.append(horario.dia_semana.id)
    print(dias_consultorio)
    if len(dias_consultorio) == 0:
        raise Exception("No existe parámetro de Horario Médico para ", agenda.medico)
    # year, month, day = (int(x) for x in fecha_anterior.split('-'))
    fecha_anterior = agenda.fecha
    dia_semana = fecha_anterior.weekday() + 1  # weekday empieza desde lunes, index 0
    print("dia_semana: ", dia_semana, "weekday: ", fecha_anterior.weekday())
    if dia_semana != 6:
        dia_semana += 1
    else:
        dia_semana = 1

    # print(dia_semana)
    fecha_siguiente = fecha_anterior
    lista_dias = []

    # cargo la lista de dias empezando del día de la semana de la fecha_anterior
    for x in range(0, 7):
        lista_dias.append(dia_semana)
        if dia_semana < 7:
            dia_semana += 1
        else:
            dia_semana = 1

    if len(dias_consultorio) == 1:
        # si atiende un solo dia a la semana, se le agregan 7 dias
        fecha_siguiente = fecha_anterior + timedelta(days=7)
    else:
        for dia in lista_dias:
            print("  dias_consultorio: ", dias_consultorio, "dia_semana: ", dia_semana, "; dia: ", dia)
            if dia_semana != dia:
                print("    fecha sgte: ", fecha_siguiente)
                fecha_siguiente += timedelta(days=1)
                if dia in dias_consultorio:
                    break

    return fecha_siguiente
