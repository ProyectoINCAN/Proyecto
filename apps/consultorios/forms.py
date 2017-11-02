from django import forms
from django.contrib.auth.models import User

from apps.consultorios.models import Medico, EvolucionPaciente, HorarioMedico,\
    Enfermero, Administrativo, OrdenEstudio, OrdenEstudioDetalle
from django_select2 import forms as select2form

from apps.internaciones.models import Diagnostico


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nombres', 'apellidos', 'tipo_doc', 'nro_doc', 'nro_registro_profesional', 'sexo', 'fecha_nacimiento',
                  'lugar_nacimiento', 'nacionalidad', 'estado_civil', 'etnia',  # 'fecha_ingreso',
                  'especialidad']
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'tipo_doc': 'Tipo de documento',
            'nro_doc': 'Nro. de documento',
            'nro_registro_profesional': 'Nro. Registro Profesional',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'lugar_nacimiento': 'Lugar de Nacimiento',
            'nacionalidad': 'Nacionalidad',
            'estado_civil': 'Estado Civil',
            'etnia': 'Etnia',
            'especialidad': 'Especialidad'
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'nro_registro_profesional': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control datepicker',
                                                       'placeholder': 'dd/mm/aaaa'}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'etnia': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'especialidad':  select2form.Select2MultipleWidget(attrs={'class': 'form-control selectsearch-multiple', 'style':'width: 100%'})
        }


class EnfermeroForm(forms.ModelForm):
    class Meta:
        model = Enfermero
        fields = ['nombres', 'apellidos', 'tipo_doc', 'nro_doc', 'nro_registro_profesional', 'sexo', 'fecha_nacimiento', 'lugar_nacimiento',
                  'nacionalidad']
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'tipo_doc': 'Tipo de documento',
            'nro_doc': 'Número de documento',
            'nro_registro_profesional': 'Nro. Registro Profesional',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'lugar_nacimiento': 'Lugar de nacimiento',
            'nacionalidad': 'Nacionalidad',
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'nro_registro_profesional': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control datepicker',
                                                       'placeholder': 'dd/mm/aaaa'}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control selectsearch'}),
        }


class AdministrativoForm(forms.ModelForm):
    class Meta:
        model = Administrativo
        fields = ['nombres', 'apellidos', 'tipo_doc', 'nro_doc', 'sexo', 'fecha_nacimiento', 'lugar_nacimiento',
                  'nacionalidad']
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'tipo_doc': 'Tipo de documento',
            'nro_doc': 'Número de documento',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'lugar_nacimiento': 'Lugar de nacimiento',
            'nacionalidad': 'Nacionalidad',
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control datepicker',
                                                       'placeholder': 'dd/mm/aaaa'}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control selectsearch'}),
        }


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password_id")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")


# class UserModelForm(forms.ModelForm):
#     error_messages = {
#         'password_mismatch': "Las contraseñas no coinciden.",
#     }
#     password1 = forms.CharField(label="Contraseña",
#                                 widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),)
#     password2 = forms.CharField(label="Confirmación de contraseña",
#                                 widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
#                                 help_text="Vuelva a ingresar la contraseña para confirmar.")
#
#     class Meta:
#         model = User
#         fields = ("username", "password", "password1", "password2")
#
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
#             # 'password1': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
#             # 'password2': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
#         }
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2
#
#     def save(self, commit=True):
#         user = super(UserModelForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

    # class Meta:
    #     model = User
    #     fields = ['username', 'password']
    #     labels = {
    #         'username': 'Nombre de usuario',
    #         'password': 'Contraseña',
    #     }
    #     widgets = {
    #         'username': forms.CharField(attrs={'class': 'form-control'}),
    #         'password': forms.PasswordInput(),
    #     }


class EvolucionPacienteModelForm(forms.ModelForm):
    class Meta:
        model = EvolucionPaciente
        fields = ['fecha', 'hora', 'observaciones', 'medico', ]
        labels = {
            'fecha': 'Fecha',
            'hora': 'Hora',
            'observaciones': 'Observaciones',
            'medico': 'Médico'
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'medico': forms.TextInput(attrs={'class': 'form-control'}),
        }


class HorarioMedicoModelForm(forms.ModelForm):
    class Meta:
        model = HorarioMedico
        fields = ['medico', 'hora_inicio', 'hora_fin', 'cod_departamento', 'dia_semana', 'turno', 'cantidad',
                  'habilitado', ]
        labels = {
            'medico': 'Médico',
            'hora_inicio': 'Hora inicio',
            'hora_fin': 'Hora fin',
            'cod_departamento': 'Departamento',
            'dia_semana': 'Día de la semana',
            'turno': 'Turno',
            'cantidad': 'Cantidad',
            'habilitado': 'Habilitado'
        }
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control timepicker text-center'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control timepicker text-center'}),
            'cod_departamento': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'dia_semana': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'turno': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class OrdenEstudioForm(forms.ModelForm):
    class Meta:
        model = OrdenEstudio
        fields = ['nombre', 'descripcion']

        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrdenEstudioDetalleForm(forms.ModelForm):
    class Meta:
        model = OrdenEstudioDetalle
        exclude = ['orden_estudio']

        labels = {
            'nombre': 'Nombre',
            'observacion': 'Observación'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class DiagnosticoPacienteForm(forms.ModelForm):

    class Meta:
        model = Diagnostico
        exclude = ['paciente', 'medico', 'fecha']

        labels = {
            'cie10': 'CIE10',
            'observacion': 'Observación'
        }
        widgets = {
            'cie10': forms.TextInput(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }