from django import forms
from django.db import models as django_models
from django.utils.translation import ugettext_lazy as _
from apps.pacientes.models import Paciente, Direccion, PacienteNivelEducativo, Telefono

from django.contrib.admin import widgets
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS

#clase PacienteForm para el formulario de agendamiento de pacientes.
#15/04/17
class PacienteForm(forms.ModelForm):
    #nombres =forms.CharField(max_length=100, required=True)
    #apellidos = forms.CharField(max_length=100, required=True)


    """
     05/05/17
     cambios de paciente form
      Primero se cargar los datos basicos en call center.

    """

    class Meta:
        model = Paciente


        exclude = ['nro_doc_alternativo',]


        fields = [
            'nombres',
            'apellidos',
            'tipo_doc',
            'nro_doc',
            'sexo',

        ]



        labels = {
            'nombres':'Nombres',
            'apellidos':'Apellidos',
            'tipo_doc':'Tipo de Documento',
            'nro_doc': 'Número de Documento',
            'nro_doc_alternativo':'Documento Alternativo',
            'sexo':'Sexo',

             }

        #help_texts = {
         #   'fecha_nacimiento': _('La fecha debe estar en formato DD/MM/YYYY.'),
        #}

        widgets = {
         #   'nombres': forms.TextInput(attrs ={'class': 'form-control'}),
          #  'apellidos': forms.TextInput(attrs ={'class': 'form-control'}),
           # 'nro_doc': forms.TextInput(attrs ={'class': 'form-control'}),
            #'nro_doc_alternativo': forms.TextInput(attrs ={'class': 'form-control'}),
            #'sexo': forms.TextInput(attrs={'class':'form-control'}),
            #'fecha_nacimiento': suit.widgets.SuitDateWidget,
            #'lugar_nacimiento': forms.TextInput(attrs ={'class': 'form-control'}),
            #'nacionalidad': forms.TextInput(attrs ={'class': 'form-control'}),
            #'estado_civil': forms.TextInput(attrs ={'class': 'form-control'}),
            #'etnia': forms.TextInput(attrs ={'class': 'form-control'}),
        }

        #validacion para la creacion de un nuevo paciente


class TelefonoForm(forms.ModelForm):

    class Meta:
        model = Telefono

        fields = [
            'numero',
            'tipo',

        ]

        labels = {
            'numero': 'Número',
            'tipo': 'Tipo',

        }

        # widgets = {
        #     'numero': forms.TextInput(attrs={'class': 'form-control'}),
        #     'orden': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'confirmado':forms.CheckboxInput(attrs={'class': 'form-control'}),
        # }






class DireccionForm(forms.ModelForm):

    class Meta:
        model = Direccion

        fields = [
            'descripcion',
            'departamento',
            'distrito',
            'barrio',
            'area',
            'sector',
            'manzana',
            'nro_casa',
            'residencia_ocasional',
            'referencia',
        ]

        labels = {
            'descripcion': 'Descripcion',
            'departamento': 'Departamento',
            'distrito': 'Distrito',
            'barrio': 'Barrio',
            'Sector': 'Sector',
            'manzana': 'Manzana',
            'nro_casa': 'nro_casa',
            'residencia_ocasional': 'Residencia Ocasional',
            'referencia': 'Referencia',
        }

class NivelEducativoForm(forms.ModelForm):

    class Meta:
        model = PacienteNivelEducativo

        fields = [
            'nivel_educativo',
            'completo',
        ]

        labels = {
            'nivel_educativo': 'Nivel Educativo ',
            'completo': 'Culminó '
        }


