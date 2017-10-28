from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from apps.consultorios.models import EstadoConsultaDetalle


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.crear_estado_consulta()

    def crear_estado_consulta(self):
        if EstadoConsultaDetalle.objects.filter(codigo='V').exists() is False:
            EstadoConsultaDetalle.objects.create(codigo='V', nombre='Vigente')

        if EstadoConsultaDetalle.objects.filter(codigo='P').exists() is False:
            EstadoConsultaDetalle.objects.create(codigo='P', nombre='Pendiente')

        if EstadoConsultaDetalle.objects.filter(codigo='F').exists() is False:
            EstadoConsultaDetalle.objects.create(codigo='F', nombre='Finalizado')