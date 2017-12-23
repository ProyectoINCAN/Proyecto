from distutils.command import register

import django_select2
from django import forms
from django.db import models as django_models
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2Widget
from django_select2 import forms as select2form

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

            'nombres': 'Nombres:',
            'apellidos': 'Apellidos:',
            'tipo_doc': 'Tipo Documento:',
            'nro_doc': 'Nro de Documento:',
            'nro_doc_alternativo': 'Documento Alternativo',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de Nac.',
            'lugar_nacimiento': 'Lugar de Nac.',
            'distrito': 'Lugar de Residencia',
            'nacionalidad': 'Nacionalidad',
            'estado_civil': 'Estado Civil',
            'etnia': 'Etnia',
        }

        widgets = {
            'nombres': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'required': 'required'}),
            'apellidos': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'required': 'required'}),
            'tipo_doc': forms.Select(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'style': 'width: 100%',
                       'required': 'required', 'id': 'id_tipo_doc'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                                        'style': 'width: 100%', 'required': 'required', }),
            'fecha_nacimiento': forms.DateInput(
                attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'distrito': forms.Select(
                attrs={'class': 'form-control selectsearch', 'style': 'width: 100%', 'required': 'required', }),
            'nacionalidad': forms.Select(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'required': 'required'}),
            'etnia': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                                         'style': 'width: 100%', 'required': 'required', }),
            'estado_civil': forms.Select(
                attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                       'style': 'width: 100%', 'required': 'required', }),
            'lugar_nacimiento': forms.Select(
                attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                       'style': 'width: 100%', 'required': 'required', }),
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

            'tipo': 'Tipo de teléfono',
            'numero': 'Número de teléfono',

        }

        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'confirmado': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
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
            'descripcion': 'Dirección',
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
            'departamento': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'distrito': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'barrio': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'area': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%', }),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'manzana': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'nro_casa': forms.TextInput(attrs={'class': 'form-control'}),
            'residencia_ocasional': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
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
            'seguro_medico': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'detalle': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
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
            'anho_cursado': 'Año Cursado'
        }

        widgets = {
            'nivel_educativo': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'completo': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
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
            'descripcion': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
        }


class OcupacionForm(forms.ModelForm):
    class Meta:
        model = PacienteOcupacion

        fields = [
            'ocupacion',
        ]
        labels = {'descripcion': 'Ocupación', }

        widgets = {
            'descripcion': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
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
            'ocupacion': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'situacion_laboral_id': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'profesion': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
        }


class PacientePadreForm(forms.ModelForm):
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
            'asume_sustento': 'Asume el sustento de la familia:'
        }

        widgets = {
            'nombres': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'required': 'required', }),
            'apellidos': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'required': 'required', }),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                                            'style': 'width: 100%', 'required': 'required', 'id': 'id_tipo_doc'}),
            'nro_doc': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'required': 'required',
                       'id': 'nro_doc'}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                                        'style': 'width: 100%', 'required': 'required', 'id': 'mySelect'}),
            'fecha_nacimiento': forms.DateInput(
                attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'lugar_nacimiento': forms.Select(
                attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                       'style': 'width: 100%', 'required': 'required', }),
            'nacionalidad': forms.Select(
                attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                       'style': 'width: 100%', 'required': 'required', }),
            'estado_civil': forms.Select(
                attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                       'style': 'width: 100%', 'required': 'required', }),
            'etnia': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                                         'style': 'width: 100%', 'required': 'required', }),
            'ocupacion': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                                             'style': 'width: 100%'}),
            'nivel_educativo': forms.Select(
                attrs={'class': 'form-control selectsearch', 'style': 'text-transform:uppercase;',
                       'style': 'width: 100%', 'required': 'required', }),
            'otro': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'asume_sustento': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
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
            'nivel_educativo': 'Nivel Educativo',
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


class ViviendaForm(forms.ModelForm):
    class Meta:
        model = Vivienda

        fields = [
            'pared',
            'techo',
            'piso',
            'dependencia',
            'hacinamiento',
            'nro_personas_hogar',
            'comparte_cama',
            'nro_dormitorio',
        ]
        labels = {
            'pared': 'Pared',
            'techo': 'Techo',
            'piso': 'Piso',
            'dependencia': 'Dependencias',
            'hacinamiento': 'Hacinamiento',
            'nro_personas_hogar': 'Nº de Personas en el Hogar',
            'comparte_cama': 'Comparte Cama',
            'nro_dormitorio': 'Nº Dormitorios'
        }
        widgets = {
            'pared': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'techo': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'piso': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'nro_personas_hogar': forms.NumberInput(attrs={'class': 'form-control'}),
            'nro_dormitorio': forms.NumberInput(attrs={'class': 'form-control'}),
            'dependencia': forms.SelectMultiple(attrs={'class': 'form-control selectsearch-multiple',
                                                       'style': 'width: 100%'}),
            'hacinamiento': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
            'comparte_cama': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),

        }


class ServicioSanitarioForm(forms.ModelForm):
    class Meta:
        model = ServicioSanitario

        fields = [
            'agua',
            'eliminacion_basura',
            'desagua',
        ]
        labels = {
            'agua': 'Agua:',
            'eliminacion_basura': 'Eliminación de Basura:',
            'desagua': 'El baño se desagua en:',
        }
        widgets = {
            'agua': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'eliminacion_basura': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'desagua': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
        }


class ServiciosBasicosForm(forms.ModelForm):
    class Meta:
        model = ServicioBasicos

        fields = [
            'luz_electrica',
            'telefono_linea_baja',
            'telefono_linea_celular',
            'heladera',
            'televisor',
            'otros',
        ]
        labels = {
            'luz_electrica': 'Luz Eléctrica',
            'telefono_linea_baja': 'Teléf. Línea Baja',
            'telefono_linea_celular': 'Teléf. Celular',
            'heladera': 'Heladera',
            'televisor': 'Televisor',
            'otros': 'Otros',
        }
        widgets = {
            'luz_electrica': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
            'telefono_linea_baja': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
            'telefono_linea_celular': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
            'heladera': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
            'televisor': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
            'otros': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
        }


class AcompañanteForm(forms.ModelForm):
    class Meta:
        model = Acompanhante

        fields = [
            'tipo_doc',
            'nro_doc',
            'nombres',
            'apellidos',
            'tipo_telefono',
            'numero',
            'vinculo',
        ]
        labels = {
            'tipo_doc': 'Tipo Documento',
            'nro_doc': 'Nro. Doc',
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'tipo_telefono': 'Tipo Teléfono',
            'numero': 'Número',
            'vinculo': 'Vinculo',
        }
        widgets = {
            'nombres': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'required': 'required'}),
            'apellidos': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'required': 'required'}),
            'tipo_doc': forms.Select(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'style': 'width: 100%',
                       'required': 'required', 'id': 'id_tipo_doc'}),

            'nro_doc': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'required': 'required',
                       'id': 'nro_doc'}),
            'tipo_telefono': forms.Select(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'style': 'width: 100%',
                       'required': 'required', }),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'vinculo': forms.Select(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'style': 'width: 100%',
                       'required': 'required', }),
        }


class CorreoElectronicoForm(forms.ModelForm):
    class Meta:
        model = CorreoElectronico

        fields = [
            'tipo',
            'direccion',
        ]
        labels = {
            'tipo': 'Tipo Correo Electrónico',
            'direccion': 'Correo',
        }
        widgets = {
            'direccion': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(
                attrs={'class': 'form-control', 'style': 'text-transform:uppercase;', 'style': 'width: 100%',
                       'required': 'required', }),
        }
