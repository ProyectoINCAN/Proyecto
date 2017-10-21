from django.db import models

# Create your models here.
from apps.consultorios.models import Medico, Turno, Especialidad
from apps.pacientes.models import Paciente
from utils.upperField import UpperCharField


class EstadoAgenda(models.Model):
    codigo = UpperCharField(max_length=1, blank=False, primary_key=True, uppercase=True)
    nombre = UpperCharField(max_length=50, blank=False, uppercase=True)

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
    especialidad = models.ForeignKey(Especialidad, models.DO_NOTHING, blank=True, null=True)
    cantidad = models.IntegerField(null=True)  # Cantidad máxima definida en HorarioMedico
    estado = models.ForeignKey(EstadoAgenda, models.DO_NOTHING, blank=False, null=False, default='P')

    def __str__(self):
        return self.fecha.isoformat() + ", Turno: " + self.turno.nombre

    class Meta:
        ordering = ['fecha', 'id']
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'


class AgendaDetalleManager(models.Manager):
    """Manager de la clase AgendaDetalle. Aquí se pueden definir métodos de la clase personalizados
    que Django no trae por defecto"""

    def orden_llegada(self, agenda):
        """Devuelve el siguiente orden de llegada de paciente para agendar"""
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                select count(*) cantidad from agendamientos_agenda a
                join agendamientos_agendadetalle d on a.id = d.agenda_id
                where a.fecha = ?
                and medico_id = ?
                and turno_id = ? """, agenda.fecha, agenda.medico.id, agenda.turno.id)
            orden = cursor.fetchone()
            if not orden:
                orden = 0

            print("maximo orden " + orden)

        return orden+1  # todo controlar que no sea mayor al máximo por médico


class AgendaDetalle(models.Model):
    agenda = models.ForeignKey(Agenda, models.DO_NOTHING, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    orden = models.IntegerField()  # TODO incremento automático según el orden de llegada
    observacion = UpperCharField(max_length=50, blank=True, null=True, uppercase=True, default='');
    confirmado = models.BooleanField(default=True)
    objects = AgendaDetalleManager()  # Instanciar el Manager de la clase definido previamente

    def __str__(self):
        return str(self.agenda) + ", Turno: " + str(self.orden)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Detalle de Agenda'
        verbose_name_plural = 'Detalles de Agenda'


