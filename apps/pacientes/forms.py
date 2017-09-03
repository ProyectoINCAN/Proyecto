from django import forms
from django.db import models as django_models
from django.utils.translation import ugettext_lazy as _
from apps.pacientes.models import *

from django_select2 import forms as select2form

from django.contrib.admin import widgets
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS


class PacienteForm(forms.ModelForm):
    """
     05/05/17
     cambios de paciente form
      Primero se cargar los datos basicos en call center.

    """

    class Meta:
        model = Paciente
        exclude = ['nro_doc_alternativo']

        fields = [
            'nombres',
            'apellidos',
            'tipo_doc',
            'nro_doc',
            'sexo',
            'fecha_nacimiento',
            'lugar_nacimiento',
            'nacionalidad',
            'estado_civil',
            'etnia'

        ]

        labels = {
            'nombres':'Nombres:',
            'apellidos': 'Apellidos:',
            'tipo_doc':'Tipo Doc:',
            'nro_doc': 'Número de Documento:',
            'nro_doc_alternativo':'Documento Alternativo',
            'sexo':'Sexo',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'lugar_nacimiento':'Lugar de Nacimiento',
            'nacionalidad': 'Nacionalidad',
            'estado_civil': 'Estado Civil',
            'etnia': 'Etnia',
             }

        widgets = {
            'nombres': forms.TextInput(attrs ={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs ={'class': 'form-control'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch'}),
             'nro_doc': forms.TextInput(attrs ={'class': 'form-control'}),
             'sexo': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'lugar_nacimiento':  forms.Select(attrs={'class': 'form-control selectsearch'}),
            'nacionalidad':  forms.Select(attrs={'class': 'form-control selectsearch'}),
            'estado_civil':  forms.Select(attrs={'class': 'form-control selectsearch'}),
             'etnia':  forms.Select(attrs={'class': 'form-control selectsearch'}),
        }

        #validacion para la creacion de un nuevo paciente


class TelefonoForm(forms.ModelForm):

    class Meta:
        model = Telefono

        fields = [
            'tipo',
            'numero',

        ]

        labels = {

            'tipo': 'Tipo de Telefono',
            'numero': 'Número',

        }

        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'confirmado':forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


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
            'area': 'Area',
            'manzana': 'Manzana',
            'nro_casa': 'Nro casa',
            'residencia_ocasional': 'Residencia Ocasional',
            'referencia': 'Referencia',
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'distrito': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'barrio': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'area': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'departamento': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'sector': forms.TextInput(attrs={'class': 'form-control'}),
            'nro_casa': forms.TextInput(attrs={'class': 'form-control'}),
            'manzana': forms.TextInput(attrs={'class': 'form-control'}),
            'residencia_ocasional': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SeguroMedicoForm(forms.ModelForm):

    class Meta:
        model =  PacienteSeguroMedico

        fields = [
            'seguro_medico'
        ]
        labels = {
            'seguro_medico': 'Seguro Médico'
        }
        widgets = {
            'seguro_medico': forms.Select(attrs={'class': 'form-control selectsearch'}),
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


class SituacionLaboralForm(forms.ModelForm):

    class Meta:
        model = SituacionLaboral

        fields = [
            'descripcion'
        ]

        labels = {
            'descripcion': 'Descripcion'
        }

        widgets = {
            'descripcion': forms.Select(attrs={'class': 'form-control selectsearch'}),
        }


class OcupacionForm(forms.ModelForm):

    class Meta:
        model = Ocupacion

        fields = ['descripcion']
        labels= { 'descripcion': 'Ocupación',}

        widgets = {
            'descripcion': forms.Select(attrs={'class': 'form-control selectsearch'}),
        }


class PacienteOcupacionForm(forms.ModelForm):

    class Meta:
        model = PacienteOcupacion

        fields = [
            'ocupacion',
            'situacion_laboral_id',
            'profesion'
        ]
        labels = {
            'ocupacion': 'Ocupación',
            'situacion_laboral_id': 'Situación Laboral',
            'profesion': 'Profesion',
        }
        widgets = {
            'ocupacion': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'situacion_laboral_id': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'profesion': forms.Select(attrs={'class': 'form-control selectsearch'}),
        }


class PacientePadreForm(forms.ModelForm):

    class Meta:
        model = PacientePadre
        exclude = ['paciente', 'padre']

        labels = {
            'nombres': 'Nombres:',
            'apellidos': 'Apellidos:',
            'tipo_doc': 'Tipo Doc:',
            'nro_doc': 'Número de Documento:',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'lugar_nacimiento': 'Lugar de Nacimiento',
            'nacionalidad': 'Nacionalidad',
            'estado_civil': 'Estado Civil',
            'etnia': 'Etnia',
        }

        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'fecha_nacimiento': forms.DateInput(
                attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'etnia': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'ocupacion': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'nivel_educativo': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'otro': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PacienteNivelEducativoForm(forms.ModelForm):
    class Meta:
        model = PacienteNivelEducativo

        exclude = ['paciente', 'anho_cursado']

        labels = {
            'nivel_educativo':  'Nivel Educativo',
            'completo': 'Termino',
        }

        widgets = {
            'nivel_educativo': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'completo': forms.Select(attrs={'class': 'form-control selectsearch'})
        }
