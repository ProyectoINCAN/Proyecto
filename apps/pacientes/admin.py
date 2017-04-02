from django.contrib import admin

# Register your models here.
from apps.pacientes.models import TipoDoc, EstadoCivil, SeguroMedico, Barrio, Localidad, Region, Pais, Paciente, Sexo, \
    Etnia, NivelEducativo, SituacionLaboral, Profesion, Area, Ocupacion


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

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['nombre','pais', 'habilitado']
    list_per_page = 15

@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    list_display = ['nombre','region', 'habilitado']
    list_per_page = 15

@admin.register(Barrio)
class BarrioAdmin(admin.ModelAdmin):
    list_display = ['nombre','localidad', 'habilitado']
    list_per_page = 15

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['apellidos','nombres', 'tipo_doc', 'nro_doc']
    list_per_page = 15
    #filter_horizontal = ['profesion']
    exclude = ('fecha_registrado',)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre']
    list_per_page = 15

@admin.register(Ocupacion)
class OcupacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion','habilitado']
    list_per_page = 15

