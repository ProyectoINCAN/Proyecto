from django.contrib import admin

# Register your models here.
from apps.consultorios.models import Especialidad, Medico, Departamento, HorarioMedico


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'habilitado']
    list_per_page = 15

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['apellidos', 'nombres', 'tipo_doc', 'nro_doc']
    list_per_page = 15

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'habilitado']
    list_per_page = 15

@admin.register(HorarioMedico)
class HorarioMedicoAdmin(admin.ModelAdmin):
    #list_display = ['codigo', 'nombre', 'habilitado']
    list_per_page = 15