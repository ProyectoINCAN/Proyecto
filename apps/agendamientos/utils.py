from datetime import date, timedelta

from apps.consultorios.models import HorarioMedico, DiasSemana


def get_fecha_agendamiento_siguiente(agenda):
    """
    Retorna la siguiente fecha disponible de agendamiento del médico para casos de cancelación de agenda

    :param agenda: agenda que se cancela
    :return: fecha
    """

    horario_medico = HorarioMedico.objects.filter(medico=agenda.medico, habilitado=True, turno=agenda.turno)
    dias_consultorio = []
    for horario in horario_medico:
        dias_consultorio.append(horario.dia_semana.python_weekday)
    # print(dias_consultorio)
    if len(dias_consultorio) == 0:
        raise Exception("No existe parámetro de Horario Médico para ", agenda.medico)
    # year, month, day = (int(x) for x in fecha_anterior.split('-'))
    fecha_anterior = agenda.fecha
    # dia_semana = fecha_anterior.weekday() + 1  # weekday empieza desde lunes, index 0
    dia_semana = fecha_anterior.weekday()  # weekday empieza desde lunes, index 0
    print("dia_semana: ", dia_semana, "weekday: ", fecha_anterior.weekday())
    # if dia_semana != 6:
    #     dia_semana += 1
    # else:
    #     dia_semana = 1

    # print(dia_semana)
    fecha_siguiente = fecha_anterior
    tmp_fecha = fecha_anterior
    lista_dias = []

    # cargo la lista de dias empezando del día de la semana de la fecha_anterior
    for x in range(0, 7):
        tmp_fecha = tmp_fecha + timedelta(days=1)
        lista_dias.append(tmp_fecha.weekday())
        # lista_dias.append(dia_semana)
        # if dia_semana < 7:
        #     dia_semana += 1
        # else:
        #     dia_semana = 1

    print("1. lista_dias", lista_dias, len(lista_dias))  # listadias borrar
    # tmp = 1/0 #borrar
    if len(dias_consultorio) == 1:
        # si atiende un solo dia a la semana, se le agregan 7 dias
        fecha_siguiente = fecha_anterior + timedelta(days=7)
    else:
        for dia in lista_dias:
            print("  2. dias_consultorio: ", dias_consultorio, "dia_semana: ", dia_semana, "; dia: ", dia)
            # if dia_semana != dia:
            print("    3. fecha sgte: ", fecha_siguiente)
            if dia in dias_consultorio:
                # if dia != dia_semana:
                fecha_siguiente += timedelta(days=1)
                print("  4.dias_consultorio: ", dias_consultorio, "dia_semana: ", dia_semana, "; fecha siguiente: ",
                      fecha_siguiente)

                break
            fecha_siguiente += timedelta(days=1)
    print("  5.dias_consultorio: ", dias_consultorio, "dia_semana: ", dia_semana, "; fecha siguiente: ", fecha_siguiente)
    # tmp = 1 / 0  # borrar
    return fecha_siguiente


def get_fecha_probable_agendamiento(horario_medico):
    fecha = date.today()
    horario_weekday_list = []
    semana_list = []
    for dia in range(0, 7):
        semana_list.append(fecha+timedelta(days=dia))  # lista de fechas de la semana empezando por weekday de hoy

    for horario in horario_medico:
        horario_weekday_list.append(horario.dia_semana.python_weekday)

    for dia in semana_list:
        if dia.weekday() in horario_weekday_list:
            print("dia retornado", dia)
            return dia


def get_cantidad_by_horario_medico_fecha(horario_medico, fecha):
    horario = horario_medico.filter(dia_semana__python_weekday=fecha.weekday()).first()
    cantidad = 0
    if horario:
        cantidad = horario.cantidad
    return cantidad
