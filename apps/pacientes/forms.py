from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.pacientes.models import Paciente


#clase PacienteForm para el formulario de agendamiento de pacientes.
#15/04/17
class PacienteForm(forms.ModelForm):
    #nombres =forms.CharField(max_length=100, required=True)
    #apellidos = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Paciente




        fields = [
            'nombres',
            'apellidos',
            'tipo_doc',
            'nro_doc',
            'nro_doc_alternativo',
            'sexo',
            'fecha_nacimiento',
            'lugar_nacimiento',
            'nacionalidad',
            'estado_civil',
            'etnia',
        ]



        labels = {
            'nombres':'Nombres',
            'apellidos':'Apellidos',
            'tipo_doc':'Tipo de Documento',
            'nro_doc': 'Número de Documento',
            'nro_doc_alternativo':'Documento Alternativo',
            'sexo':'Sexo',
            'fecha_nacimiento':'Fecha de Nacimiento',
            'lugar_nacimiento':'Lugar de Nacimiento',
            'nacionalidad':'Nacionalidad',
            'estado_civil':'Estado Civil',
            'etnia':'Etnia',
             }

        #help_texts = {
         #   'fecha_nacimiento': _('La fecha debe estar en formato DD/MM/YYYY.'),
        #}

        #widgets = {
         #   'nombres': forms.TextInput(attrs ={'class': 'form-control'}),
          #  'apellidos': forms.TextInput(attrs ={'class': 'form-control'}),
           # 'nro_doc': forms.TextInput(attrs ={'class': 'form-control'}),
            #'nro_doc_alternativo': forms.TextInput(attrs ={'class': 'form-control'}),
            #'sexo': forms.TextInput(attrs={'class':'form-control'}),
            #'fecha_nacimiento': forms.TextInput(attrs ={'class': 'form-control'}),
            #'lugar_nacimiento': forms.TextInput(attrs ={'class': 'form-control'}),
            #'nacionalidad': forms.TextInput(attrs ={'class': 'form-control'}),
            #'estado_civil': forms.TextInput(attrs ={'class': 'form-control'}),
            #'etnia': forms.TextInput(attrs ={'class': 'form-control'}),
        #}

        # validacion
        def clean(self):
            print(self.cleaned_data)
            return self.cleaned_data

            # Validamos que el autor no sea menor a 3 caracteres

        def clean_nombres(self):
            diccionario_limpio = self.cleaned_data

            nombres = diccionario_limpio.get('nombres')

            if len(nombres) < 3:
                raise forms.ValidationError("El autor debe contener mas de tres caracteres")

            return nombres

