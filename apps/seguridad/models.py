from django.db import models
from apps.pacientes.models import Distrito, Area


# Create your models here.
from utils.upperField import UpperCharField


class Establecimiento(models.Model):
    codigo = UpperCharField(max_length=2, blank=False, primary_key=True, uppercase=True)
    nombre = UpperCharField(max_length=60, blank=False, uppercase=True)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Establecimiento"
        verbose_name_plural = "Establecimientos"


class RegionSanitaria(models.Model):
    codigo = UpperCharField(max_length=2, blank=False, primary_key=True, uppercase=True)
    nombre = UpperCharField(max_length=60, blank=False, uppercase=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Región Sanitaria"
        verbose_name_plural = "Regiones Sanitarias"


class ParametroSistema(models.Model):
    nombre = UpperCharField(max_length=60, blank=False, uppercase=True)
    region_sanitaria = models.ForeignKey(RegionSanitaria, models.SET_NULL, blank=True, null=True, verbose_name="Región Sanitaria")
    distrito = models.ForeignKey(Distrito, models.SET_NULL, blank=True, null=True)
    establecimiento = models.ForeignKey(Establecimiento, models.SET_NULL, blank=True, null=True)
    area = models.ForeignKey(Area, models.SET_NULL, blank=True, null=True)
    telefono = UpperCharField(max_length=100, blank=True, null=True, uppercase=True)
    correo_electronico = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Correo electrónico")
    direccion = UpperCharField(max_length=255, blank=True, null=True, uppercase=True)
    secuencia = models.IntegerField(null=True)  # secuencia numérica para los nros de documento alternativos

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Parámetro del Sistema"
        verbose_name_plural = "Parámetros del Sistema"