from django.core.exceptions import ValidationError


#validacion del nombre
def nombre_validation(value):
    '''valida el tamanho del campo del nombre del paciente'''
    if not len(value) > 4:
        raise ValidationError('Minimo 4 caracteres')

def charfield_validation(value):
    '''valida que el campo no acepte números'''

    #lista con las letras del abecedario y un espacio
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't',
              'u', 'v', 'w', 'x', 'y', 'z', ' ']
    #convierte a minuscula
    valor = value.lower()

    for elemento in valor:
        if elemento not in letras:
            raise ValidationError('El campo nombre no acepto números ')

def doc_validation(value):
    if not len(value) > 0:
        raise ValidationError('El campo no puede estar vacio')
