from django.contrib import admin

# Register your models here.
from apps.pacientes.models import TipoDoc, EstadoCivil, SeguroMedico, Barrio, Localidad, Region, Pais


#registrar usando decorador, para evitar usar el método register
@admin.register(TipoDoc)
class TipoDocAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'habilitado']
    list_per_page = 2

#registrar usando el método register
class EstadoCivilAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'habilitado']
    list_per_page = 2
admin.site.register(EstadoCivil, EstadoCivilAdmin)

@admin.register(SeguroMedico)
class SeguroMedicoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'habilitado']
    list_per_page = 2

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre','habilitado']
    list_per_page = 2


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['nombre','pais', 'habilitado']
    list_per_page = 2

@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    list_display = ['nombre','region', 'habilitado']
    list_per_page = 2

@admin.register(Barrio)
class BarrioAdmin(admin.ModelAdmin):
    list_display = ['nombre','localidad', 'habilitado']
    list_per_page = 2

