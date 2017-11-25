import django_select2
from django import forms
from django.db import models as django_models
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2Widget

from apps.pacientes.models import *


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
            'nacionalidad',
            'lugar_nacimiento',
            'distrito',
            'estado_civil',
            'etnia'

        ]

        labels = {

            'nombres':'Nombres:',
            'apellidos': 'Apellidos:',
            'tipo_doc':'Tipo Documento:',
            'nro_doc': 'Nro de Documento:',
            'nro_doc_alternativo':'Documento Alternativo',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de Nac.',
            'lugar_nacimiento': 'Lugar de Nac.',
            'distrito': 'Lugar de Residencia',
            'nacionalidad': 'Nacionalidad',
            'estado_civil': 'Estado Civil',
            'etnia': 'Etnia',
             }

        widgets = {
            'nombres': forms.TextInput(attrs ={'class': 'form-control', 'style':'text-transform:uppercase;','required':'required',}),
            'apellidos': forms.TextInput(attrs ={'class': 'form-control', 'style':'text-transform:uppercase;', 'required':'required',}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'text-transform:uppercase;', 'style':'width: 100%', 'required':'required',}),
            'nro_doc': forms.TextInput(attrs ={'class': 'form-control','required':'required',}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'text-transform:uppercase;','style':'width: 100%', 'required':'required',}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'distrito': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%', 'required':'required',}),
            'nacionalidad':  forms.Select(attrs={'class':'form-control selectsearch', 'style':'width: 100%', 'required':'required',}),
            'etnia': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;', 'style':'width: 100%','required':'required',}),
            'estado_civil': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;', 'style':'width: 100%', 'required':'required',}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;', 'style':'width: 100%','required':'required',}),
        }

    def clean(self):
        pass


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
            'tipo': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
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
            'descripcion',
            'nro_casa',
            'residencia_ocasional',
            'referencia',
        ]

        labels = {
            'descripcion':'Dirección',
            'departamento': 'Departamento',
            'distrito': 'Distrito',
            'barrio': 'Barrio',
            'area': 'Area',
            'Sector': 'Sector',
            'manzana': 'Manzana',
            'direccion': 'Dirección',
            'nro_casa': 'Número',
            'residencia_ocasional': 'Residencia Ocasional',
            'referencia': 'Referencia',
        }
        widgets = {
            'departamento': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'distrito': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'barrio': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'area': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',}),
            'sector': forms.TextInput(attrs={'class': 'form-control','style':'text-transform:uppercase;'}),
            'manzana': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'nro_casa': forms.TextInput(attrs={'class': 'form-control'}),
            'residencia_ocasional': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
        }


class PacienteSeguroMedicoForm(forms.ModelForm):

    class Meta:
        model = PacienteSeguroMedico

        fields = [
            'seguro_medico',
            'detalle'
        ]
        labels = {
            'seguro_medico': 'Seguro Médico',
            'detalle': 'Observación'
        }
        widgets = {
            'seguro_medico': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'detalle': forms.TextInput(attrs={'class': 'form-control'}),
        }


class NivelEducativoForm(forms.ModelForm):

    class Meta:
        model = PacienteNivelEducativo

        fields = [
            'nivel_educativo',
            'completo',
            'anho_cursado',
        ]

        labels = {
            'nivel_educativo': 'Nivel Educativo ',
            'completo': 'Completo',
            'anho_cursado':'Año Cursado'
        }

        widgets = {
            'nivel_educativo': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'completo':forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'anho_cursado': forms.TextInput(attrs={'class': 'form-control'}),
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
        model = PacienteOcupacion

        fields = [
            'ocupacion',
        ]
        labels= { 'descripcion': 'Ocupación',}

        widgets = {
            'descripcion': forms.Select(attrs={'class': 'form-control selectsearch'}),
        }


class PacienteOcupacionForm(forms.ModelForm):

    class Meta:
        model = PacienteOcupacion

        fields = [

            'situacion_laboral_id',
            'profesion',
            'ocupacion'
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
    asume_sustento=forms.BooleanField(initial=True)

    class Meta:
        model = PacientePadre
        exclude = ['paciente', 'padre']

        labels = {
            'nombres': 'Nombres:',
            'apellidos': 'Apellidos:',
            'tipo_doc': 'Tipo Documento:',
            'nro_doc': 'Número de Documento:',
            'sexo': 'Sexo:',
            'fecha_nacimiento': 'Fecha de Nacimiento:',
            'lugar_nacimiento': 'Lugar de Nacimiento:',
            'nacionalidad': 'Nacionalidad:',
            'estado_civil': 'Estado Civil:',
            'etnia': 'Etnia:',
            'ocupacion': 'Ocupación:',
            'nivel_educativo': 'Nivel Educactivo:',
            'otro': 'Otro, especificar:',
            'asume_sustento':'Asume el sustento de la familia:'
        }

        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control','style':'text-transform:uppercase;','required':'required',}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;','required':'required',}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch','style':'text-transform:uppercase;', 'style':'width: 100%', 'required':'required',}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;','required':'required',}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch','style':'text-transform:uppercase;', 'style':'width: 100%', 'required':'required','id':'mySelect'}),
            'fecha_nacimiento': forms.DateInput(
                attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control selectsearch','style':'text-transform:uppercase;', 'style':'width: 100%', 'required':'required',}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control selectsearch','style':'text-transform:uppercase;', 'style':'width: 100%', 'required':'required',}),
            'estado_civil': forms.Select(attrs={'class': 'form-control selectsearch','style':'text-transform:uppercase;', 'style':'width: 100%', 'required':'required',}),
            'etnia': forms.Select(attrs={'class': 'form-control selectsearch','style':'text-transform:uppercase;', 'style':'width: 100%', 'required':'required',}),
            'ocupacion': forms.Select(attrs={'class': 'form-control selectsearch','style':'text-transform:uppercase;', 'style':'width: 100%', 'required':'required',}),
            'nivel_educativo': forms.Select(attrs={'class': 'form-control selectsearch','style':'text-transform:uppercase;', 'style':'width: 100%', 'required':'required',}),
            'otro': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'asume_sustento':forms.RadioSelect(attrs={'class': 'form-control', 'style':'width: 100%'}),
        }


class PacienteNivelEducativoForm(forms.ModelForm):
    class Meta:
        model = PacienteNivelEducativo

        fields = [

            'nivel_educativo',
            'completo',
            'anho_cursado'
        ]

        labels = {
            'nivel_educativo':  'Nivel Educativo',
            'completo': 'Ha culminado',
            'anho_cursado': 'Año Cursado',
        }

        widgets = {
            'nivel_educativo': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'completo': forms.Select(attrs={'class': 'form-control selectsearch'}),

        }

    def clean(self):
        completo = self.cleaned_data.get('completo')
        cursado = self.cleaned_data.get('anho_cursado')
        if completo == "":
            self.add_error('completo', 'Debe seleccionar si cúlmino el nivel educactivo')
        else:
            if not cursado or cursado < 0:
                self.add_error('anho_cursado', 'Debe ingresar el año cursado')


