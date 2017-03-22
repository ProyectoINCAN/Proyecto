from django.db import models

# Create your models here.

class TipoDoc(models.Model):
    codigo = models.CharField(max_length=3, blank=False)
    descripcion = models.CharField(max_length=50, blank=False)
    habilitado = models.BooleanField(default=True)

    #método para que retorne el objeto en formato de string
    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"


class Sexo(models.Model):
    codigo = models.CharField(max_length=1, blank=False)
    descripcion = models.CharField(max_length=30, blank=False)
    habilitado = models.BooleanField(default=True)

    class Meta:
        ordering = ["descripcion"]
        verbose_name = "Sexo"
        verbose_name_plural = "Sexos"

class EstadoCivil(models.Model):
    codigo = models.CharField(max_length=2, blank=False)
    nombre = models.CharField(max_length=30, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Estado Civil"
        verbose_name_plural = "Estados Civiles"

class NivelEducativo(models.Model):
    nombre = models.CharField(max_length=50, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Nivel Educativo"
        verbose_name_plural = "Niveles Educativos"

