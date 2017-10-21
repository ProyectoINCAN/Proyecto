from django import forms
from apps.internaciones.models import *


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento

        fields = ['nombre', 'tipificacion', 'forma_farmaceutica',
                  'nro_lote', 'cantidad', 'fabricado', 'vencimiento']

        labels = {
            'nombre': 'Nombre',
            'forma_farmaceutica': 'Forma Farmaceutica',
            'nro_lote': 'Número Lote',
            'cantidad': 'Cantidad',
            'fabricado': 'Fecha Fabricación',
            'vencimiento': 'Fecha Venc.',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control autofocus', 'style':'text-transform:uppercase;'}),
            'forma_farmaceutica': forms.TextInput(attrs ={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'nro_lote': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'fabricado': forms.DateInput(
                attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'tipificacion': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'vencimiento': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),

        }

    def clean(self):
        if self.cleaned_data['cantidad'] <= 0:
            self.add_error('cantidad', 'La cantidad debe ser mayor a cero')

        fecha_fabricacion =self.cleaned_data['fabricado']
        fecha_venc = self.cleaned_data['vencimiento']
        if fecha_fabricacion > fecha_venc:
            self.add_error('fabricado', 'La fecha de fabricación no puede ser inferior a la fecha de vencimiento')

    def __init__(self, *args, tipo= None, **kwargs):
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
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'descripcion': forms.Textarea(attrs={'rows': 2, 'cols': 45, 'style':'text-transform:uppercase;'}),
        }