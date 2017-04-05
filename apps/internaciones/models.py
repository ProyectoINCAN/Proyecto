from django.db import models

# Create your models here.
from apps.consultorios.models import Medico
from apps.pacientes.models import Paciente
from apps.seguridad.models import Establecimiento


class TipoReferencia(models.Model):
    codigo = models.CharField(max_length=2, blank=False, primary_key=True)
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Tipo Referencia"
        verbose_name_plural = "Tipos de Referencias"

class CIE10(models.Model):
    codigo = models.CharField(max_length=2, blank=False, primary_key=True)
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "CIE10"
        verbose_name_plural = "CIE10"

class CondicionEgreso(models.Model):
    codigo = models.CharField(max_length=2, blank=False, primary_key=True)
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Condición Egreso"
        verbose_name_plural = "Condición Egreso"

class TipoEgreso(models.Model):
    codigo = models.CharField(max_length=2, blank=False, primary_key=True)
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Tipo de Egreso"
        verbose_name_plural = "Tipo de Egreso"


class Egreso(models.Model):
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    fecha = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fecha de egreso")
    tipo = models.ForeignKey(TipoEgreso, models.DO_NOTHING, blank=False, null=False, verbose_name="Tipo de egreso")
    condicion_egreso = models.ForeignKey(CondicionEgreso, models.DO_NOTHING, blank=False, null=False, verbose_name="Condición al egreso")
    dias_internacion = models.IntegerField(blank=False, verbose_name="Días de interanción")
    nro_certificado_defuncion = models.IntegerField(blank=False, verbose_name="Nº del Certificado de Defunción")

    def __str__(self):
        return self.condicion_egreso

    class Meta:
        ordering = ["paciente"]
        verbose_name = "Egreso"
        verbose_name_plural = "Egresos"


class DiagnosticoEgreso(models.Model):
    egreso = models.ForeignKey(Egreso, models.DO_NOTHING, blank=False, null=False)
    cie_10 = models.ForeignKey(CIE10, models.DO_NOTHING, blank=False, null=False)
    principal = models.BooleanField(default=True)

    def __str__(self):
        return self.egreso

    class Meta:
        ordering = ["egreso"]
        verbose_name = "Diagnóstico Egreso"
        verbose_name_plural = "Diagnósticos del Egreso"


class ViaIngreso(models.Model):
    codigo = models.CharField(max_length=2, blank=False, primary_key=True)
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Ingreso Por"
        verbose_name_plural = "Ingresos Por"


class Ingreso(models.Model):
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    fecha = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fecha de ingreso")
    motivo = models.ForeignKey(CIE10, models.DO_NOTHING, blank=False, null=False)
    ingreso_por = models.ForeignKey(ViaIngreso, models.DO_NOTHING, blank=False, null=False)

    def __str__(self):
        return self.referencia

    class Meta:
        ordering = ["paciente"]
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"


class ReferenciaIngreso(models.Model):
    referencia_id = models.ManyToManyField(Ingreso, verbose_name='Referencia')
    tipo_referencia = models.ManyToManyField(TipoReferencia, verbose_name='Tipo Referencia')
    establecimiento = models.ManyToManyField(Establecimiento, verbose_name='Establecimiento')

    def __str__(self):
        return self.ingreso

    class Meta:
        ordering = ["id"]
        verbose_name = "Referencia de Ingreso"
        verbose_name_plural = "Referencias de Ingresos"


class Servicio(models.Model):
    nombre = models.CharField(max_length=60, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"


class Insumo(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    nro_lote = models.CharField(max_length=100, blank=False, verbose_name="Número de Lote")
    cantidad = models.IntegerField(blank=False, verbose_name="Cantidad")
    fabricado = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fabricado")
    vencimiento = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Vencimiento")
    tipificacion = models.CharField(max_length=100, blank=False, verbose_name="Tipificación")
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"


class Medicamento(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    forma_farmaceutica = models.CharField(max_length=200, blank=False)
    nro_lote = models.CharField(max_length=100, blank=False, verbose_name="Número de Lote")
    cantidad = models.IntegerField(blank=False, verbose_name="Cantidad")
    fabricado = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fabricado")
    vencimiento = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Vencimiento")
    tipificacion = models.CharField(max_length=100, blank=False, verbose_name="Tipificación")
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"


class Internado(models.Model):
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    tipo_ingreso = models.CharField(max_length=100, blank=False)
    puesto = models.CharField(max_length=100, blank=False)
    motivo = models.CharField(max_length=100, blank=False)
    medico_solitante = models.ForeignKey(Medico, models.SET_NULL, blank= True, null=True, related_name ="medicosolicitantec")
    medico_cabecera = models.ForeignKey(Medico, models.DO_NOTHING, blank=False, null=False,related_name ="medicos")
    forma_ingreso = models.CharField(max_length=150, blank=False)
    servicio =  models.ForeignKey(Servicio, models.DO_NOTHING, blank=False, null=False)
    observacion = models.CharField(max_length=300, blank=False)

    def __str__(self):
        return self.paciente

    class Meta:
        ordering = ["paciente"]
        verbose_name = "Internado"
        verbose_name_plural = "Internados"


class InternadoInsumo(models.Model):
    internado = models.ForeignKey(Internado, models.DO_NOTHING, blank=False, null=False)
    medicamento = models.ForeignKey(Medicamento, models.DO_NOTHING, blank=False, null=False)
    cantidad_medicamento = models.IntegerField(blank=False, verbose_name="Cantidad de Medicamento")
    insumo = models.ForeignKey(Insumo, models.DO_NOTHING, blank=False, null=False)
    cantidad_insumo = models.IntegerField(blank=False, verbose_name="Cantidad de Insumo")

    def __str__(self):
        return self.paciente

    class Meta:
        ordering = ["internado"]
        verbose_name = "Internado"
        verbose_name_plural = "Internados"