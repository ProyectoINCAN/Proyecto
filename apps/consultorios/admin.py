from django.contrib import admin

# Register your models here.
from apps.consultorios.models import Especialidad, Medico, Departamento, HorarioMedico, Consultorio, OrdenEstudio, Turno


@admin.register(Consultorio)
class ConsultorioAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'habilitado']
    list_per_page = 15


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'habilitado']
    list_per_page = 15


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['apellidos', 'nombres', 'tipo_doc', 'nro_doc']
    filter_horizontal = ['especialidad', ]
    list_per_page = 15


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'habilitado']
    list_per_page = 15


@admin.register(HorarioMedico)
class HorarioMedicoAdmin(admin.ModelAdmin):
    list_display = ['medico', 'dia_semana', 'turno', 'hora_inicio', 'hora_fin', 'habilitado']
    list_per_page = 15


@admin.register(OrdenEstudio)
class OrdenEstudioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'estado']
    list_per_page = 15


@admin.register(Turno)
class TurnomAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'habilitado']
    list_per_page = 15


