from django.db import models
from django.utils.timezone import now

from apps.pacientes.models import TipoDoc, Sexo, Localidad, Pais, EstadoCivil, Etnia

# Create your models here.


class Consultorio(models.Model):
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["descripcion"]
        verbose_name = "Consultorio"
        verbose_name_plural = "Consultorios"

class Especialidad(models.Model):
    codigo = models.CharField(max_length=3, blank=False, primary_key=True)
    nombre = models.CharField(max_length=60, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"

class Medico(models.Model):
    nombres = models.CharField(max_length=100, blank=False)
    apellidos = models.CharField(max_length=100, blank=False)
    tipo_doc = models.ForeignKey(TipoDoc, models.DO_NOTHING, blank=False, null=False, verbose_name="Tipo de documento")
    nro_doc = models.CharField(max_length=15, blank=False, null=False, verbose_name="Número de documento", unique=True)
    nro_registro_medico = models.CharField(max_length=15, blank=False, null=False, verbose_name="Número de Registro Médico", unique=True)
    sexo = models.ForeignKey(Sexo, models.DO_NOTHING, blank=False, null=False)
    fecha_nacimiento = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fecha de nacimiento")
    lugar_nacimiento = models.ForeignKey(Localidad, models.DO_NOTHING, blank=False, null=False, verbose_name="Lugar de nacimiento")
    nacionalidad = models.ForeignKey(Pais, models.DO_NOTHING, blank=False, null=False)
    estado_civil = models.ForeignKey(EstadoCivil, models.DO_NOTHING, blank=False, null=False)
    etnia = models.ForeignKey(Etnia, models.DO_NOTHING, blank=False, null=False)
    fecha_ingreso = models.DateField(auto_now=True, null=False)
    especialidad = models.ManyToManyField(Especialidad)

    def __str__(self):
        return self.apellidos + " " + self.nombres

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

class Departamento(models.Model):
    codigo = models.CharField(max_length=3, blank=False, primary_key=True)
    nombre = models.CharField(max_length=60, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"


class Turno(models.Model):
    codigo = models.CharField(max_length=3, blank=False, primary_key=True)
    nombre = models.CharField(max_length=60, blank=False)
    habilitado = models.BooleanField(default=True)


class HorarioMedico(models.Model):
    DIAS_SEMANA_CHOICES = (
        (1, 'Domingo'),
        (2, 'Lunes'),
        (3, 'Martes'),
        (4, 'Miércoles'),
        (5, 'Jueves'),
        (6, 'Viernes'),
        (7, 'Sábado'),
    )
    medico = models.ForeignKey(Medico, models.DO_NOTHING, blank=False, null=False, verbose_name="Médico")
    hora_inicio = models.TimeField(blank=False, null=False)
    hora_fin = models.TimeField(blank=False, null=False)
    cod_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, blank=False, null=False, verbose_name="Departamento")
    dia_semana = models.CharField(max_length=15, choices=DIAS_SEMANA_CHOICES, blank=False, null=False, verbose_name="Día de la semana")
    turno = models.ForeignKey(Turno, models.DO_NOTHING, blank=False, null=False, verbose_name="Turno")
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["medico"]
        verbose_name = "Horario Médico"
        verbose_name_plural = "Horarios de Médicos"


class OrdenEstudio(models.Model):
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.CharField(default="", max_length=80, blank=False)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Orden de Estudio"
        verbose_name_plural = "Ordenes de Estudios"