from django import forms


from apps.agendamientos.models import Agenda, AgendaDetalle
#from django_select2 import forms as select2form
from django_select2 import forms as select2form


class AgendaForm(forms.ModelForm):

    class Meta:
        model = Agenda

        fields = [
            'medico',
            'especialidad',
            'fecha',
            'turno',
            'cantidad',
            'estado',
        ]

        labels = {
            'medico': 'Médico',
            'especialidad': 'Especialidad',
            'fecha': 'Fecha',
            'turno': 'Turno',
            'cantidad': 'Cantidad',
            'estado': 'Estado',
        }

        widgets = {
            'especialidad': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'medico': forms.Select(attrs={'class': 'form-control selectsearch', 'id': 'medico_id', 'style':'width: 100%'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'turno': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'estado': forms.Select(attrs={'class': 'form-control selectsearch', 'style':'width: 100%'}),
        }


class AgendaDetalleForm(forms.ModelForm):
    confirmado=forms.BooleanField(initial=True)

    class Meta:
        model = AgendaDetalle
        # exclude = ('agenda',)
        fields = [
            # 'agenda',
            'paciente',
            # 'orden',
            'confirmado',
        ]

        labels = {
            # 'agenda': 'Agenda',
            'paciente': 'Paciente',
            # 'orden': 'Orden',
            'confirmado': 'Confirmado',
        }

        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'confirmado': forms.RadioSelect(attrs={'class': 'form-control', 'style':'width: 100%'}),
        }
