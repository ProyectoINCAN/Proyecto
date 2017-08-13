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
            'especialidad': forms.Select(attrs ={'class':'form-control selectsearch'}),
            'medico': forms.Select(attrs ={'class':'form-control selectsearch'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'turno': forms.Select(attrs ={'class':'form-control selectsearch'}),
            'cantidad': forms.TextInput(attrs ={'class': 'form-control'}),
            'estado': forms.Select(attrs ={'class':'form-control selectsearch'}),
        }



class AgendaDetalleForm(forms.ModelForm):

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

            'paciente': forms.Select(attrs ={'class':'form-control selectsearch'}),
            # 'orden': forms.NumberInput(attrs={'class': 'form-control'}),
            'confirmado':forms.CheckboxInput(attrs={'class': 'form-control'}),
        }




