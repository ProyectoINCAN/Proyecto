from django.contrib.auth.models import User, Group
from django import forms
from django.contrib import messages
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from apps.consultorios.models import Medico, Enfermero, Administrativo


class UserForm(forms.ModelForm):
    medicos = forms.ModelChoiceField(
        queryset=Medico.objects.all(), required=False,
        widget=forms.Select(attrs={'class': 'form-control selectsearch'}))

    enfermeros = forms.ModelChoiceField(queryset=Enfermero.objects.all(), required=False,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control selectsearch', 'style': 'width: 100%'}))

    administrativo = forms.ModelChoiceField(queryset=Administrativo.objects.all(), required=False,
                                            widget=forms.Select(attrs={'class': 'form-control selectsearch',
                                                                       'style': 'width: 100%'}))
    MEDICO = 1
    ENFERMERO = 2
    ADMINISTRATIVO = 3

    TIPOS_USUARIOS = (
        (MEDICO, 'Medico'),
        (ENFERMERO, 'Enfermero'),
        (ADMINISTRATIVO, 'Administrativo')
    )
    tipos = forms.ChoiceField(choices=TIPOS_USUARIOS, widget=forms.Select(attrs={'class': 'form-control selectsearch'}))

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"), widget= forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                strip=False,
                                help_text=_("Enter the same password as before, for verification."))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',
                  'tipos', 'medicos', 'enfermeros', 'administrativo')

        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','required':'required'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def clean(self):
        # tipo 1 corresponde a los medicos, 2 corresponde a los administrativo y 3 corresponde a enfermeros.
        if int(self.cleaned_data.get('tipos')) == 1:
            if not self.cleaned_data.get('medicos'):
                self.add_error('medicos', 'Debe seleccionar el médico')
        elif int(self.cleaned_data.get('tipos')) == 2:
            if not self.data.get('enfermeros'):
                self.add_error('enfermero', 'Debe seleccionar el enfermero')
        elif int(self.cleaned_data.get('tipos')) == 3:
            if not self.data.get('administrativo'):
                self.add_error('administrativo', 'Debe seleccionar un administrativo')

        # validar el nombre de usuario
        usuario = self.cleaned_data.get('username')
        if User.objects.filter(username=usuario).exists():
            self.add_error('username', 'Ya existe un usuario con el nombre {}'.format(usuario))

    def save(self, commit=True):
        with transaction.atomic():
            user = super(UserForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            user.is_active = True
            user.save()
            grupo = Group.objects.get(pk=self.cleaned_data['tipos'])
            grupo.user_set.add(user)

            if int(self.cleaned_data.get('tipos'))== 1:
                medico = self.cleaned_data.get('medicos')
                medico.usuario = user
                medico.save()
            elif int(self.cleaned_data.get('tipos')) == 2:
                enfermero = self.cleaned_data.get('enfermeros')
                enfermero.usuario = user
                enfermero.save()
            # administrativo
            elif int(self.cleaned_data.get('tipos')) == 3:
                administrativo = self.cleaned_data.get('administrativos')
                administrativo.usuario = user
                administrativo.save()

            return user


class UserEditForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField(label=_("Password"))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_active')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'is_active' or field_name != 'password':
                class_css = 'form-control'

                self.fields[field_name].widget.attrs.update({
                    'class': class_css,
                    'placeholder': self.fields[field_name].label,
                })
            if field_name == 'is_active':
                self.fields[field_name].widget.attrs.update({
                    'class': 'big-checkbox',
                    'type': 'checkbox'
                })



class UserPasswordChangeForm(AdminPasswordChangeForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                strip=False,
                                help_text=_("Enter the same password as before, for verification."))

    class Meta:
        model = User

        fields = ('password1', 'password2')
        labels = {
            'password1': 'Contraseña',
            'password2': 'Repetir Contraseña',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        instance = kwargs.pop('instance')
        super().__init__(user, *args, **kwargs)



    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
