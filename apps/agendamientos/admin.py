from django.contrib import admin

# Register your models here.
from apps.agendamientos.models import Agenda


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'turno', 'medico', 'estado']
    list_per_page = 15
