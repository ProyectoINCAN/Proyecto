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
            # 'estado',
        ]

        labels = {
            'medico': 'Médico',
            'especialidad': 'Especialidad',
            'fecha': 'Fecha',
            'turno': 'Turno',
            'cantidad': 'Cantidad',
            # 'estado': 'Estado',
        }

        widgets = {
            'especialidad': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                                'required': 'required'}),
            'medico': forms.Select(attrs={'class': 'form-control selectsearch', 'id': 'medico_id',
                                          'style': 'width: 100%', 'required': 'required'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa',
                                            'required': 'required'}),
            'turno': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
                                         'required': 'required'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'required': 'required'}),
            # 'estado': forms.Select(attrs={'class': 'form-control selectsearch', 'style': 'width: 100%',
            #                               'required': 'required'}),
        }

    def clean(self):
        fecha = self.data.get('fecha')
        print("fecha", fecha)
        if fecha:
            medico = self.cleaned_data.get('medico')
            turno = self.cleaned_data.get('turno')

            # verifica que la fecha ingresada no sea menor a la fecha de hoy
            fecha_date = datetime.datetime.strptime(fecha, '%d/%m/%Y').date()
            if fecha_date < datetime.date.today():
                self.add_error('fecha', 'No se puede crear una agenda en una fecha anterior a hoy.')

            # verifica que la fecha sea una fecha en la que el médico atiende
            horario_weekday_list = []
            for horario in HorarioMedico.objects.filter(medico=medico, turno=turno, habilitado=True):
                horario_weekday_list.append(horario.dia_semana.python_weekday)

            if fecha_date.weekday() not in horario_weekday_list:
                dia = DiasSemana.objects.get(python_weekday=fecha_date.weekday())
                fecha_str = '{} {}'.format(dia.nombre, fecha_date.strftime("%d/%m/%Y"))
                self.add_error('fecha', 'El médico no atiende en fecha {}'.format(fecha_str))

            dia = datetime.datetime.strptime(fecha, '%d/%m/%Y').weekday()

            if not HorarioMedico.objects.filter(medico=medico, dia_semana__python_weekday=dia, turno=turno,
                                                habilitado=True).exists():
                dias = HorarioMedico.objects.filter(medico=medico, habilitado=True)
                d = ' '
                for dia in dias:
                    d += dia.dia_semana.nombre + '. Turno: ' + dia.turno.nombre + '; '
                self.add_error('fecha', 'Los días de atención son: {}'.format(d))

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
