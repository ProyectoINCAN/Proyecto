
from django.contrib.auth.models import User
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


def ver_permisos(usuario_id, permiso_buscado):
    """
    Funcion para comprobar que un usuario tenga permisos habilitados sobre la vista
    recibia como parametro
    :param usuario: codigo de usuario
    :param permiso_buscado: nombre del permiso
    :return: True o False
    """

    print("Id_user = "+ usuario_id)

    print("Permiso = "+ permiso_buscado)
    #buscamos al usuario por el usuario_id
    user= User.objects.get(id = usuario_id)

    #obtenemos todos los permisos
    list_permisos = user.get_all_permissions()
    tiene_permiso = False

    for permiso in list_permisos:
        #el permiso de admeinistrador tiene acceso a todos
        if user.groups.get().name == "Administrador":
            tiene_permiso = True
            break
        else:
            if permiso == permiso_buscado:
                tiene_permiso = True
                break
    if tiene_permiso:
        print("El usuario posee permiso")
        permission = True
    else:
        print("El usuario no posee permiso")
        permission = False
    return permission
