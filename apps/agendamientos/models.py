from django.db import models

# Create your models here.


class Pared(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Pared"
        verbose_name_plural = "Paredes"


class Techo(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Techo"
        verbose_name_plural = "Techos"


class Piso(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Piso"
        verbose_name_plural = "Pisos"


class Dependencia(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"


class Agua(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Agua"
        verbose_name_plural = "Aguas"


class EliminacionBasura(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Eliminación Basura"
        verbose_name_plural = "Eliminación de Basuras"


class Desagua(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Desagua"
        verbose_name_plural = "Desagua"


class ServicioBasico(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Servicio Básico"
        verbose_name_plural = "Servicio Básico"











