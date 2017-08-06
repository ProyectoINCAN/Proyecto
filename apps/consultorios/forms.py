from django import forms
from django.contrib.auth.models import User

from apps.consultorios.models import Medico, Especialidad, EvolucionPaciente, HorarioMedico
# from lib.chosen import forms as chosenforms
from django_select2 import forms as select2form


class MedicoModelForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nombres', 'apellidos', 'tipo_doc', 'nro_doc', 'nro_registro_medico', 'sexo', 'fecha_nacimiento',
                  'lugar_nacimiento', 'nacionalidad', 'estado_civil', 'etnia',  # 'fecha_ingreso',
                  'especialidad']
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'tipo_doc': 'Tipo de documento',
            'nro_doc': 'Número de documento',
            'nro_registro_medico': 'Nro. Registro Médico',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'lugar_nacimiento': 'Lugar de nacimiento',
            'nacionalidad': 'Nacionalidad',
            'estado_civil': 'Estado Civil',
            'etnia': 'Etnia',
            'especialidad': 'Especialidad'
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_doc': select2form.Select2Widget(attrs={'class': 'form-control'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'nro_registro_medico': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'etnia': forms.Select(attrs={'class': 'form-control'}),
            'especialidad':  select2form.Select2MultipleWidget(attrs={'class': 'form-control'}, choices=Especialidad.objects.all())
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        # self.fields['fecha_ingreso'].required = False


class UserModelForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "Las contraseñas no coinciden.",
    }
    password1 = forms.CharField(label="Contraseña",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),)
    password2 = forms.CharField(label="Confirmación de contraseña",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
                                help_text="Vuelva a ingresar la contraseña para confirmar.")

    class Meta:
        model = User
        fields = ("username",)

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # 'password1': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
            # 'password2': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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
        fields = ['medico', 'hora_inicio', 'hora_fin', 'cod_departamento', 'dia_semana', 'turno', 'cantidad', 'habilitado', ]
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
            'medico': select2form.Select2Widget(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control timepicker text-center'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control timepicker text-center'}),
            'cod_departamento': select2form.Select2Widget(attrs={'class': 'form-control'}),
            'dia_semana': select2form.Select2Widget(attrs={'class': 'form-control'}),
            'turno': select2form.Select2Widget(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

