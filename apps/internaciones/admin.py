from django.contrib import admin

# Register your models here.
from apps.internaciones.models import TipoReferencia, CIE10, CondicionEgreso, TipoEgreso, Egreso, DiagnosticoEgreso, \
    ViaIngreso


@admin.register(TipoReferencia)
class TipoReferenciaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'habilitado']
    list_per_page = 15


@admin.register(CIE10)
class CIE10Admin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'habilitado']
    list_per_page = 15


@admin.register(CondicionEgreso)
class CondicionEgresoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'habilitado']
    list_per_page = 15


@admin.register(TipoEgreso)
class TipoEgresoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'habilitado']
    list_per_page = 15


@admin.register(Egreso)
class EgresoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'condicion_egreso', 'dias_internacion']
    list_per_page = 15


@admin.register(DiagnosticoEgreso)
class DiagnosticoEgresoAdmin(admin.ModelAdmin):
    list_display = ['egreso', 'cie_10', 'principal']
    list_per_page = 15


@admin.register(ViaIngreso)
class ViaIngresoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'habilitado']
    list_per_page = 15