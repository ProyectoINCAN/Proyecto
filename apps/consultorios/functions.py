from apps.consultorios.models import ConsultaDetalle, EstadoConsultaDetalle, EstadoConsulta


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

    if not ConsultaDetalle.objects.filter(consulta=consulta,
                                          estado=EstadoConsultaDetalle.objects.get(codigo="P")).exists():
        # si no existe ninguna consulta detalle de la consulta cabecera en estado PENDIENTE, cambia a FINALIZADO
        cambiar_estado_consulta(consulta, EstadoConsulta.objects.get(codigo="F"))
    else:
        cambiar_estado_consulta(consulta, EstadoConsulta.objects.get(codigo="V"))
