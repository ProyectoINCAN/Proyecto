from django.db import models
from apps.pacientes.models import Distrito, Area


# Create your models here.
from utils.upperField import UpperCharField


class Establecimiento(models.Model):
    nombre = UpperCharField(max_length=60, blank=False, uppercase=True)
    telefono = UpperCharField(max_length=30, blank=True, uppercase=True)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Establecimiento"
        verbose_name_plural = "Establecimientos"


class ParametroSistema(models.Model):
    REGION_SANITARIA_CHOICES = (
        ('I', 'PRIMERA'),
        ('II', 'SEGUNDA'),
        ('III', 'TERCERA'),
        ('IV', 'CUARTA'),
        ('V', 'QUINTA'),
        ('VI', 'SEXTA'),
        ('VII', 'SÉPTIMA'),
        ('VIII', 'OCTAVA'),
        ('IX', 'NOVENA'),
        ('X', 'DÉCIMA'),
        ('XI', 'UNDÉCIMA'),
        ('XII', 'DUODÉCIMA'),
        ('XIII', 'DECIMO TERCEA'),
        ('XIV', 'DECIMO CUARTA'),
        ('XV', 'DECIMO QUINTA'),
        ('XVI', 'DECIMO SEXTA'),
        ('XVII', 'DECIMO SÉPTIMA'),
        ('XVIII', 'DECIMO OCTAVA')
    )
    nombre = UpperCharField(max_length=60, blank=False, uppercase=True)
    region_sanitaria = UpperCharField(max_length=5, choices=REGION_SANITARIA_CHOICES, blank=False, null=False,
                                      verbose_name="Región Sanitaria")
    distrito = models.ForeignKey(Distrito, models.SET_NULL, blank=True, null=True, related_name='distrito')
    establecimiento = models.ForeignKey(Establecimiento, models.SET_NULL, blank=True, null=True)
    area = models.ForeignKey(Area, models.SET_NULL, blank=True, null=True, related_name='area')
    telefono = UpperCharField(max_length=100, blank=True, null=True, uppercase=True)
    correo_electronico = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Correo electrónico")
    direccion = UpperCharField(max_length=255, blank=True, null=True, uppercase=True)
    secuencia = models.IntegerField()  # secuencia numérica para los nros de documento alternativos

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Parámetro del Sistema"
        verbose_name_plural = "Parámetros del Sistema"
