from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from apps.consultorios.models import EstadoConsultaDetalle, EstadoConsulta


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.crear_estado_consulta()

    def crear_estado_consulta(self):
        if EstadoConsulta.objects.filter(codigo='V').exists() is False:
            EstadoConsulta.objects.create(codigo='V', nombre='Vigente')

        if EstadoConsulta.objects.filter(codigo='P').exists() is False:
            EstadoConsulta.objects.create(codigo='P', nombre='Pendiente')

        if EstadoConsulta.objects.filter(codigo='F').exists() is False:
            EstadoConsulta.objects.create(codigo='F', nombre='Finalizado')

        if EstadoConsulta.objects.filter(codigo='C').exists() is False:
            EstadoConsulta.objects.create(codigo='C', nombre='Cancelado')