from django import forms
from apps.internaciones.models import *


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento

        exclude = ['habilitado']

        labels = {
            'nombre': 'Nombre',
            'forma_farmaceutica': 'Forma Farmaceutica',
            'nro_lote': 'Número Lote',
            'cantidada': 'Cantidad',
            'fabricado': 'Fecha Fabricación',
            'vencimiento': 'Fecha Venc.',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'forma_farmaceutica': forms.TextInput(attrs ={'class': 'form-control', 'style':'text-transform:uppercase;'}),
            'nro_lote': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidada': forms.NumberInput(attrs={'class': 'form-control'}),
            'fabricado': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'tipificacion': forms.Select(attrs={'class': 'form-control selectsearch'}),
            'vencimiento': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/aaaa'}),

        }

    def clean(self):
        pass


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
