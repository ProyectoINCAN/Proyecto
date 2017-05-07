from django import forms


from apps.agendamientos.models import Agenda, AgendaDetalle

#clase AgendaForm para el formulario de agendamiento de pacientes.
class AgendaForm(forms.ModelForm):

    class Meta:
        model = Agenda

        fields = [
            'medico',
            'fecha',
            'consultorio',
            'turno',
            'cantidad',
            'estado',

        ]

        labels = {
            'medico': 'Médico',
            'fecha': 'Fecha',
            'consultorio':'Consultorio',
            'turno':'Turno',
            'cantidad': 'Cantidad',
            'estado': 'Estado',
        }

        widgets = {
            'medico': forms.Select(attrs ={'class':'form-control'}),
            'fecha': forms.DateInput(attrs={'class':'form-control'} ),
            'consultorio': forms.Select(attrs ={'class':'form-control'}),
            'turno': forms.Select(attrs ={'class':'form-control'}),
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




