

def limpiar_nro_doc(nro_doc):
    """"Retira puntos y espacios del nro de documento"""
    nro_doc = nro_doc.strip()
    return nro_doc.replace('.', '')


def get_nrodoc_alternativo(paciente):
    """"Genera el número de documento alternativo para pacientes que no posean documento de identidad"""
    fecha_nacimiento = str(paciente.fecha_nacimiento.__format__('%d-%m-%Y'))  # todo cambiar formato a dd-mm-aaaa
    nro_doc_alt = paciente.apellidos[0]+paciente.nombres[0]+fecha_nacimiento  # agregar parametro_sys.secuencia
    return nro_doc_alt


# PRUEBAS
# nrodoc = '4.767.907'
# print(limpiar_nro_doc(nrodoc))

# paciente = Paciente(nombres="Francisco", apellidos="Martinez", fecha_nacimiento=datetime.date.today())
# print(get_nrodoc_alternativo(paciente))

