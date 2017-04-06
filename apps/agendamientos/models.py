from django.db import models

# Create your models here.
from apps.consultorios.models import Medico, Turno, Consultorio
from apps.pacientes.models import Paciente


class EstadoAgenda(models.Model):
    codigo = models.CharField(max_length=1, blank=False, primary_key=True)
    nombre = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Estado agenda'
        verbose_name_plural = 'Estados de agenda'


class Agenda(models.Model):
    medico = models.ForeignKey(Medico, models.DO_NOTHING, blank=False, null=False)
    fecha = models.DateField(auto_now=False, blank=False, null=False) #TODO hacer funcion para que estire la siguiente fecha disponible del médico
    turno = models.ForeignKey(Turno, models.DO_NOTHING, blank=False, null=False)
    consultorio = models.ForeignKey(Consultorio, models.DO_NOTHING, blank=True, null=True)
    cantidad = models.IntegerField(default=20) #puede estar parametrizado
    estado = models.ForeignKey(EstadoAgenda, models.DO_NOTHING, blank=False, null=False) #TODO agregar default Pendiente que traiga de EstadoAgenda

    def __str__(self):
        return self.fecha + ", Turno: " + self.turno

    class Meta:
        ordering = ['fecha', 'turno']
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'


class AgendaDetalle(models.Model):
    agenda = models.ForeignKey(Agenda, models.DO_NOTHING, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    orden = models.IntegerField() #TODO incremento automático según el orden de llegada
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return self.fecha + ", Turno: " + self.turno

    class Meta:
        ordering = ['agenda', 'orden']
        verbose_name = 'Detalle de Agenda'
        verbose_name_plural = 'Detalles de Agenda'


