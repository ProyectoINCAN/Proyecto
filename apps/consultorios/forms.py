import datetime

from django import forms

from apps.consultorios.models import *
from django_select2 import forms as select2form

from apps.internaciones.models import Diagnostico


class MedicoForm(forms.ModelForm):

    class Meta:
        model = Medico
        fields = ['nombres', 'apellidos', 'tipo_doc', 'nro_doc', 'nro_registro_profesional', 'sexo', 'fecha_nacimiento',
                  'lugar_nacimiento', 'nacionalidad', 'estado_civil', 'especialidad', 'email', 'direccion', 'telefono','habilitado']
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
            'email': 'Email',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'especialidad': 'Especialidad',
            'habilitado': 'Habilitado'
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;',
                                              'required': 'required'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;',
                                                'required': 'required'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                            'required': 'required'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;',
                                              'required': 'required'}),
            'nro_registro_profesional': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                                               'style': 'text-transform:uppercase;'}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                        'required': 'required'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control datepicker', 'required': 'required',
                                                       'placeholder': 'dd/mm/aaaa'}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                                    'required': 'required'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                                'required': 'required'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                                'required': 'required'}),
            'especialidad': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 100%',
                                                        'required': 'required'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
        }


class EnfermeroForm(forms.ModelForm):
    class Meta:
        model = Enfermero
        fields = ['nombres', 'apellidos', 'tipo_doc', 'nro_doc', 'nro_registro_profesional', 'sexo', 'fecha_nacimiento',
                  'lugar_nacimiento', 'nacionalidad','habilitado']
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
            'habilitado':'Habilitado'
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'nro_registro_profesional': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control datepicker',
                                                       'placeholder': 'dd/mm/aaaa'}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
        }


class AdministrativoForm(forms.ModelForm):
    class Meta:
        model = Administrativo
        fields = ['nombres', 'apellidos', 'tipo_doc', 'nro_doc', 'sexo', 'fecha_nacimiento', 'lugar_nacimiento',
                  'nacionalidad', 'habilitado']
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'tipo_doc': 'Tipo de documento',
            'nro_doc': 'Número de documento',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'lugar_nacimiento': 'Lugar de nacimiento',
            'nacionalidad': 'Nacionalidad',
            'habilitado': 'Habilitado'
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;',
                                              'required': 'required'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;',
                                                'required': 'required'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                            'required': 'required'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'sexo': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                        'required': 'required'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa',
                                                       'required': 'required'}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                                    'required': 'required'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                                'required': 'required'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
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


class EvolucionPacienteForm(forms.ModelForm):
    class Meta:
        model = EvolucionPaciente
        fields = ['observaciones', ]
        labels = {
            'observaciones': 'Observaciones',
        }
        widgets = {
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'required': 'required',
                                                   'style': 'text-transform:uppercase; width: 100%'}),
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
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control timepicker text-center',
                                                  'required': 'required'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control timepicker text-center', 'required': 'required'}),
            'cod_departamento': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                                    'required': 'required'}),
            'dia_semana': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                              'required': 'required'}),
            'turno': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                         'required': 'required'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'number'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
        }

    def clean(self):
        # cantidad = self.data.get('cantidad')
        hora_inicio = self.data.get('hora_inicio')
        hora_fin = self.data.get('hora_fin')

        if hora_fin:
            if hora_fin < hora_inicio:
                self.add_error('hora_fin', "La 'Hora fin' no puede ser menor a la 'Hora inicio'.")


class OrdenEstudioForm(forms.ModelForm):
    class Meta:
        model = OrdenEstudio
        fields = ['nombre', 'descripcion']

        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                                 'style': 'text-transform:uppercase;width: 100%'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                                 'style': 'text-transform:uppercase;width: 100%'}),
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
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                                 'style': 'text-transform:uppercase;'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'required': 'required',
                                                 'style': 'text-transform:uppercase;width: 100%'}),
        }


class DiagnosticoPacienteForm(forms.ModelForm):

    class Meta:
        model = Diagnostico
        exclude = ['paciente', 'medico', 'fecha', 'consulta_detalle']

        labels = {
            'cie10': 'CIE-10',
            'observacion': 'Observación'
        }
        widgets = {
            'cie10': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                         'required': 'required', 'autofocus': 'autofocus'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control',
                                                 'required': 'required',
                                                 'style': 'text-transform:uppercase; width: 100%'}),
        }


class OrdenEstudioPacienteForm(forms.ModelForm):

    class Meta:
        model = ConsultaOrdenEstudio
        exclude = ['paciente', 'consulta_detalle', 'fecha_solicitud', 'interpretacion', 'fecha_presentacion']

        labels = {
            'orden_estudio': 'Estudio',
            'observacion': 'Observación',
        }
        widgets = {
            'orden_estudio': forms.Select(attrs={'class': 'form-control selectsearch', 'required': 'required',
                                                 'style': 'width: 100%'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'required': 'required',
                                                 'style': 'text-transform:uppercase; width: 100%'}),
            'fecha_presentacion': forms.DateInput(attrs={'class': 'form-control datepicker',
                                                         'placeholder': 'dd/mm/aaaa'}),
        }


class PrescripcionPacienteForm(forms.ModelForm):

    class Meta:
        model = ConsultaPrescripcion
        exclude = ['paciente', 'consulta_detalle', 'fecha']

        labels = {
            'medicamento': 'Medicamento',
            'posologia': 'Posología',
            'cantidad': 'Cantidad',
        }
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                               'required': 'required', 'autofocus': 'autofocus'}),
            'posologia': forms.Textarea(attrs={'class': 'form-control', 'required': 'required',
                                               'style': 'text-transform:uppercase; width: 100%'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required',
                                                 'style': 'width: 100%'}),
        }


class TratamientoPacienteForm(forms.ModelForm):

    class Meta:
        model = Tratamiento

        fields = ['descripcion', 'observacion']

        labels = {
            'descripcion': 'Descripción',
            'observacion': 'Observación',
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                                  'style': 'text-transform:uppercase; width: 100%',
                                                  'autofocus': 'autofocus'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'required': 'required',
                                                 'style': 'text-transform:uppercase; width: 100%'}),
        }

    def clean(self):
        descripcion = self.cleaned_data['descripcion']
        if descripcion is None or descripcion == '':
            self.add_error('descripcion', 'Campo obligatorio')


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento

        fields = ['nombre', 'tipificacion', 'forma_farmaceutica',
                  'nro_lote', 'cantidad', 'fabricado', 'vencimiento', 'habilitado']

        labels = {
            'nombre': 'Nombre',
            'forma_farmaceutica': 'Forma Farmacéutica',
            'nro_lote': 'Número Lote',
            'cantidad': 'Cantidad',
            'fabricado': 'Fecha Fabricación',
            'vencimiento': 'Fecha Venc.',
            'habilitado': 'Habilitado',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control autofocus', 'style': 'text-transform:uppercase;',
                                             'required': 'required'}),
            'forma_farmaceutica': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                                      'required': 'required'}),
            'nro_lote': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'fabricado': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa',
                                                'required': 'required'}),
            'tipificacion': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                                'required': 'required'}),
            'vencimiento': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa',
                                                  'required': 'required'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),

        }

    def clean(self):
        if self.cleaned_data.get('cantidad') <= 0:
            self.add_error('cantidad', 'La cantidad debe ser mayor a cero')

        fecha_fabricacion = self.cleaned_data.get('fabricado')
        fecha_venc = self.cleaned_data.get('vencimiento')
        if fecha_fabricacion > fecha_venc:
            self.add_error('fabricado', 'La fecha de fabricación no puede ser superior a la fecha de vencimiento')

        if fecha_venc <= datetime.date.today():
            self.add_error('vencimiento', 'No se pueden cargar medicamentos vencidos')

        if fecha_fabricacion >= datetime.date.today():
            self.add_error('fabricado', 'No se pueden cargar medicamentos con fecha de fabricación posterior a hoy.')

        # validamos el número de lote, sino existe el número ingresado ya registrado
        if self.cleaned_data.get('nro_lote'):
            if Medicamento.objects.filter(nro_lote=self.cleaned_data.get('nro_lote')).exists():
                self.add_error('nro_lote', 'Número de lote ya existe')

    def __init__(self, *args, tipo=None, **kwargs):
        super(MedicamentoForm, self).__init__(*args, **kwargs)
        self.fields['tipificacion'].queryset = TipoMedicamento.objects.filter(habilitado=True)
        if tipo:
            self.fields['tipificacion'].initial = TipoMedicamento.objects.filter(pk=tipo).values('nombre')


class TipoMedicamentoForm(forms.ModelForm):
    class Meta:
        model = TipoMedicamento

        exclude = ['habilitado']

        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'required': 'required',
                                                 'autofocus': 'autofocus',
                                                 'style': 'text-transform:uppercase;'}),
        }


class AnamnesisPacienteForm(forms.ModelForm):
    class Meta:
        model = Anamnesis
        fields = ['observacion']
        labels = {
            'observacion': 'Observaciones',
        }
        widgets = {
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'required': 'required',
                                                 'autofocus': 'autofocus',
                                                 'style': 'text-transform:uppercase;'}),
        }

    def clean(self):
        observacion = self.cleaned_data['observacion']
        if observacion == '':
            self.add_error('observacion', 'Campo obligatorio')
