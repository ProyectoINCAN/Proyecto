from django import forms


from apps.agendamientos.models import Agenda

#clase AgendaForm para el formulario de agendamiento de pacientes.
class AgendaForm(forms.ModelForm):

    class Meta:
        model = Agenda

        fields = [
            'medico',
            'fecha',
            'turno',
            'cantidad',
            'estado',

        ]

        labels = {
            'medico': 'Médico',
            'fecha': 'Fecha',
            'turno':'Turno',
            'cantidad': 'Cantidad',
            'estado': 'Estado',
        }

        widgets = {
            'medico': forms.Select(attrs ={'class':'form-control'}),
            'fecha': forms.DateInput(attrs={'class':'form-control'}),
            'turno': forms.Select(attrs ={'class':'form-control'}),
            'cantidad': forms.TextInput(attrs ={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class':'form-control'}),
        }


