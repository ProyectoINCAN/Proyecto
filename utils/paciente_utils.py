

def limpiar_nro_doc(nro_doc):
    """"Retira puntos y espacios del nro de documento"""
    nro_doc = nro_doc.strip()
    return nro_doc.replace('.', '')


def get_nrodoc_alternativo(paciente):
    """"Genera el número de documento alternativo para pacientes que no posean documento de identidad"""
    from apps.principal.models import ParametroSistema
    fecha_nacimiento = str(paciente.fecha_nacimiento.__format__('%d-%m-%Y'))
    sys = ParametroSistema.objects.get(id=1)
    print("system", sys.secuencia)
    print("paciente", paciente.apellidos)
    print("paciente", paciente.nombres)
    print("paciente", paciente.fecha_nacimiento)

    secuencia = sys.secuencia+1
    print("hola1", secuencia)
    nro_doc_alt = paciente.apellidos[0]+paciente.nombres[0]+fecha_nacimiento+'_'+str(secuencia)  # agregar parametro_sys.secuencia
    sys.secuencia = secuencia
    sys.save()
    print("salgo")
    return nro_doc_alt


def capitalizar(cadena):
    """Convierte la primera letra de una cadena a mayúscula y el resto a minúsculas"""
    ret = ''
    for nombre in cadena.split():
        ret = str(ret) + ' ' + str(nombre.capitalize())
    return ret.strip()


# PRUEBAS
# nrodoc = '4.767.907'
# print(limpiar_nro_doc(nrodoc))

# paciente = Paciente(nombres="Francisco", apellidos="Martinez", fecha_nacimiento=datetime.date.today())
# print(get_nrodoc_alternativo(paciente))

# nombres = ' 44  francisco faBian   martinez'
# print(capitalizar(nombres))