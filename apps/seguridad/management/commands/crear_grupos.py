from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.crear_grupos()

    def crear_grupos(self):
        if Group.objects.filter(name='Medico').exists() is False:
            newgroup = Group.objects.create(name='Medico')

        if Group.objects.filter(name='Enfermero').exists() is False:
            newgroup = Group.objects.create(name='Enfermero')

        if Group.objects.filter(name='Administrativo').exists() is False:
            newgroup = Group.objects.create(name='Administrativo')

        if Group.objects.filter(name='Administrativo_Ventanilla').exists() is False:
            newgroup = Group.objects.create(name='Administrativo_Ventanilla')
