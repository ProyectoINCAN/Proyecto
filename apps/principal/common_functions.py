
#funcion para establecer los parametros recibidos de los filtros
def filtros_establecidos(request, tipo):
    if tipo == "index_paciente":
        try:
            if request.GET.get('paciente') == "" and request.GET.get('cedula') == "":
                return 0
            elif request.GET.get('paciente') != "" and request.GET.get('cedula') == "":
                return 1
            elif request.GET.get('paciente') == "" and request.GET.get('cedula') != "":
                return 2
            else:
                return 3
        except Exception as e:
            print("Parametros no establecidos")
            return 0
