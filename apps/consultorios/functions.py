from apps.consultorios.models import ConsultaDetalle, EstadoConsultaDetalle, EstadoConsulta, HorarioMedico


def cambiar_estado_consulta(consulta, estado):
    """
    Cambia el estado de la consulta cabecera.
    :param consulta: objeto tipo Consulta
    :param estado: objeto tipo EstadoConsulta
    :return:
    """
    consulta.estado = estado
    consulta.save()


def verificar_estado_consulta(consulta):
    """verifica el estado de la consulta cabecera."""

    detalles = ConsultaDetalle.objects.filter(consulta=consulta)
    en_proceso = ConsultaDetalle.objects.filter(consulta=consulta, estado=EstadoConsultaDetalle.objects.get(codigo="E"))
    pendientes = ConsultaDetalle.objects.filter(consulta=consulta, estado=EstadoConsultaDetalle.objects.get(codigo="P"))
    finalizados = ConsultaDetalle.objects.filter(consulta=consulta, estado=EstadoConsultaDetalle.objects.get(codigo="F"))
    cancelados = ConsultaDetalle.objects.filter(consulta=consulta, estado=EstadoConsultaDetalle.objects.get(codigo="C"))

    if en_proceso.exists() or (cancelados.count() != detalles.count() and pendientes.count() != 0):
        # si existen en proceso (1) o la cantidad de cancelados es distinta a la cantidad de detalles cambia a VIGENTE
        cambiar_estado_consulta(consulta, EstadoConsulta.objects.get(codigo="V"))
    elif pendientes.count() == detalles.count():
        # si la cantidad de pendientes es igual a la cantidad de detalles, cambia a estado PENDIENTE
        cambiar_estado_consulta(consulta, EstadoConsulta.objects.get(codigo="P"))
    elif finalizados.count() == detalles.count() or pendientes.count() == 0:
        # si la cantidad de finalizados es igual a la cantidad de detalles, cambia a estado FINALIZADO
        cambiar_estado_consulta(consulta, EstadoConsulta.objects.get(codigo="F"))
    else:
        # si no se da ninguna de las anteriores, cambia a CANCELADO
        cambiar_estado_consulta(consulta, EstadoConsulta.objects.get(codigo="C"))


def existe_horario_medico(horario, metodo):
    """
    Verifica si ya existe el horario a crear o actualizar
    :param horario: el horario a crear o actualizar
    :param metodo: 'C': Create; 'U': Update
    :return: Boolean
    """

    if metodo == 'C':
        existe = HorarioMedico.objects.filter(medico=horario.medico, cod_departamento=horario.cod_departamento,
                                              dia_semana=horario.dia_semana, turno=horario.turno,
                                              habilitado=horario.habilitado).exists()
    else:
        # si se actualiza se verifica además la cantidad
        existe = HorarioMedico.objects.filter(medico=horario.medico, cod_departamento=horario.cod_departamento,
                                              dia_semana=horario.dia_semana, turno=horario.turno,
                                              habilitado=horario.habilitado, cantidad=horario.cantidad).exists()
    return existe
