import datetime

from django import forms


from apps.agendamientos.models import Agenda, AgendaDetalle
#from django_select2 import forms as select2form
from django_select2 import forms as select2form

from apps.consultorios.models import HorarioMedico, DiasSemana


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
            'especialidad': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'medico': forms.Select(attrs={'class': 'form-control selectsearch', 'id': 'medico_id',
                                          'style': 'width: 100%'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'turno': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'estado': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}),
        }

    def clean(self):
        fecha = self.data.get('fecha')
        print("fecha", fecha)
        if fecha:
            dia = datetime.datetime.strptime(fecha, '%d/%m/%Y').weekday()
            # sumamos dos dia a los dias para basarnos en la tabla dias de la semana
            # en caso de ser (6) domingo se setea a uno(1)
            if dia == 6:
                dia = 1
            else:
                dia += 2
            medico = self.cleaned_data.get('medico')
            turno = self.cleaned_data.get('turno')
            if not HorarioMedico.objects.filter(medico=medico, dia_semana__id=dia, turno=turno).exists():
                dias = HorarioMedico.objects.filter(medico=medico)
                d = ' '
                for dia in dias:
                    d += dia.dia_semana.nombre + ' Turno:' + dia.turno.nombre + ' '
                self.add_error('fecha', 'Los días de atención son  {}'.format(d))
        else:
            pass


class AgendaDetalleForm(forms.ModelForm):
    confirmado = forms.BooleanField(initial=True)

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
