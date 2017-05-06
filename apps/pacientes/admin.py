from django.contrib import admin

# Register your models here.
from apps.pacientes.models import TipoDoc, EstadoCivil, SeguroMedico, Barrio, Pais, Paciente, Sexo, \
    Etnia, NivelEducativo, SituacionLaboral, Profesion, Area, Ocupacion, Direccion, PacienteSeguroMedico, Distrito, \
    Departamento, PacientePadre, Nacionalidad


#registrar usando decorador, para evitar usar el método register
@admin.register(TipoDoc)
class TipoDocAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'habilitado']
    list_per_page = 15


#registrar usando el método register
class EstadoCivilAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'habilitado']
    list_per_page = 15
admin.site.register(EstadoCivil, EstadoCivilAdmin)


@admin.register(SeguroMedico)
class SeguroMedicoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'habilitado']
    list_per_page = 15


@admin.register(Sexo)
class SexoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'habilitado']
    list_per_page = 15


@admin.register(Etnia)
class EtniaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'habilitado']
    list_per_page = 15


@admin.register(NivelEducativo)
class NivelEducativoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'habilitado']
    list_per_page = 15


@admin.register(SituacionLaboral)
class SituacionLaboralAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'habilitado']
    list_per_page = 15


@admin.register(Profesion)
class ProfesionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'habilitado']
    list_per_page = 15


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre','habilitado']
    list_per_page = 15


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre','pais', 'habilitado']
    list_per_page = 15


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'departamento', 'habilitado']
    list_per_page = 15


@admin.register(Barrio)
class BarrioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'distrito', 'habilitado']
    list_filter = ['nombre', 'distrito', 'habilitado']
    list_per_page = 15


@admin.register(Nacionalidad)
class NacionalidadAdmin(admin.ModelAdmin):
    list_display = ['nacionalidad',]
    list_per_page = 15


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['fecha_nacimiento']
    #modificado para crear los primeros datos en call center.
    list_per_page = 15
    #filter_horizontal = ['profesion']
    exclude = ('fecha_registrado', 'nro_doc_alternativo')


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre']
    list_per_page = 15


@admin.register(Ocupacion)
class OcupacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion','habilitado']
    list_per_page = 15


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ['id', 'paciente','distrito']
    list_per_page = 15


@admin.register(PacienteSeguroMedico)
class SeguroMedicoAdmin(admin.ModelAdmin):
    list_display = ['seguro_medico', 'paciente']
    list_per_page = 15


@admin.register(PacientePadre)
class PacientePadreAdmin(admin.ModelAdmin):
    list_display = ['apellidos', 'nombres',]
    exclude = ('padre',)
    filter_horizontal = ['paciente']
    list_per_page = 15



