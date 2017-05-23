from django import forms


from apps.agendamientos.models import Agenda, AgendaDetalle
#from django_select2 import forms as select2form
from django_select2 import forms as select2form



#clase AgendaForm para el formulario de agendamiento de pacientes.
class AgendaForm(forms.ModelForm):

    class Meta:
        model = Agenda

        fields = [
            'especialidad',
            'fecha',
            'medico',
            'turno',
            'cantidad',
            'estado',
        ]

        labels = {
            'especialidad':'Especialidad',
            'fecha': 'Fecha',
            'medico': 'Médico',
            'turno':'Turno',
            'cantidad': 'Cantidad',
            'estado': 'Estado',
        }

        widgets = {
            'especialidad': select2form.Select2Widget(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs ={'class':'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'turno': select2form.Select2Widget(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs ={'class': 'form-control'}),
            'estado': forms.Select(attrs ={'class':'form-control'}),
        }



class AgendaDetalleForm(forms.ModelForm):

    class Meta:
        model = AgendaDetalle

        fields = [
            'paciente',
            'orden',
            'confirmado',
        ]

        labels = {
            'paciente': 'Paciente',
            'orden': 'Orden',
            'confirmado': 'Confirmado',
        }

        widgets = {
            'paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
            'confirmado':forms.CheckboxInput(attrs={'class': 'form-control'}),
        }




