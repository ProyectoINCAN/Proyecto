from django.contrib import admin

# Register your models here.
from apps.pacientes.models import TipoDoc, EstadoCivil


#registrar usando decorador, para evitar usar el método register
@admin.register(TipoDoc)
class TipoDocAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'habilitado']


#registrar usando el método register
class EstadoCivilAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'habilitado']
admin.site.register(EstadoCivil, EstadoCivilAdmin)

