from django.db import models

# Create your models here.
class TipoReferencia(models.Model):
    codigo = models.CharField(max_length=2, blank=False)
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Tipo Referencia"
        verbose_name_plural = "Tipos de Referencias"

class CIE10(models.Model):
    codigo = models.CharField(max_length=2, blank=False)
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "CIE10"
        verbose_name_plural = "CIE10"

class CondicionEgreso(models.Model):
    codigo = models.CharField(max_length=2, blank=False)
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Condición Egreso"
        verbose_name_plural = "Condición Egreso"

class TipoEgreso(models.Model):
    codigo = models.CharField(max_length=2, blank=False)
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Tipo de Egreso"
        verbose_name_plural = "Tipo de Egreso"

