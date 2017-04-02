from django.db import models

# Create your models here.
from apps.pacientes.models import Paciente


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


class Vivienda(models.Model):
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    pared = models.ForeignKey(Pared, models.DO_NOTHING, blank=False, null=False)
    techo = models.ForeignKey(Techo, models.DO_NOTHING, blank=False, null=False)
    piso = models.ForeignKey(Piso, models.DO_NOTHING, blank=False, null=False)
    dependencia = models.ForeignKey(Dependencia, models.DO_NOTHING, blank=False, null=False)
    hacinamiento = models.BooleanField(default=True)
    nro_personas_hogar = models.IntegerField(blank=False, verbose_name="Nro. de Personas en el Hogar")
    comparte_cama = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ["pared"]
        verbose_name = "Vivienda"
        verbose_name_plural = "Viviendas"


class ServicioSanitario(models.Model):
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    agua = models.ForeignKey(Agua, models.DO_NOTHING, blank=False, null=False)
    eliminacion_basura = models.ForeignKey(EliminacionBasura, models.DO_NOTHING, blank=False, null=False)
    desagua = models.ForeignKey(Desagua, models.DO_NOTHING, blank=False, null=False)

    def __str__(self):
        return self.paciente

    class Meta:
        ordering = ["paciente"]
        verbose_name = "Servicio Sanitario"
        verbose_name_plural = "Servicios Sanitarios"


class ServicioBasicos(models.Model):
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    luz_electrica = models.BooleanField(default=True)
    telefono_linea_baja = models.BooleanField(default=True)
    telefono_linea_ceular = models.BooleanField(default=True)
    heladera = models.BooleanField(default=True)
    televisor = models.BooleanField(default=True)
    otros = models.BooleanField(default=True)

    def __str__(self):
        return self.paciente

    class Meta:
        ordering = ["paciente"]
        verbose_name = "Servcio Básico"
        verbose_name_plural = "Servicios Básicos"








