from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils.timezone import now

from apps.pacientes.models import TipoDoc, Sexo, EstadoCivil, Etnia, Distrito, Nacionalidad, Paciente

# Create your models here.
from utils import paciente_utils
from utils.upperField import UpperCharField, UpperTextField


class Consultorio(models.Model):
    descripcion = UpperCharField(max_length=100, blank=False, uppercase=True)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["descripcion"]
        verbose_name = "Consultorio"
        verbose_name_plural = "Consultorios"


# class EspecialidadManager(models.Manager):
#     def especialidad_by_medico(self, medico):
#         from django.db import connection
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 select string_agg(e.nombre, ', ') as especialidades
#                 from consultorios_medico m
#                 join consultorios_medico_especialidad me on m.id = me.medico_id
#                 join consultorios_especialidad e on me.especialidad_id = e.id
#                 where m.id = ? """, medico)
#         especialidades_by_medico = cursor.fetchone()
#         return especialidades_by_medico


class Especialidad(models.Model):
    nombre = UpperCharField(max_length=60, blank=False, uppercase=True)
    habilitado = models.BooleanField(default=True)
    # objects = EspecialidadManager()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"


class Medico(models.Model):
    nombres = UpperCharField(max_length=100, blank=False, uppercase=True)
    apellidos = UpperCharField(max_length=100, blank=False, uppercase=True)
    tipo_doc = models.ForeignKey(TipoDoc, models.DO_NOTHING, blank=False, null=False, verbose_name="Tipo de documento")
    nro_doc = UpperCharField(max_length=50, blank=False, null=False, verbose_name="Número de documento", unique=True,
                             uppercase=True)
    nro_registro_profesional = UpperCharField(max_length=50, blank=False, null=False,  uppercase=True,
                                              verbose_name="Número de Registro Profesional", unique=True)
    sexo = models.ForeignKey(Sexo, models.DO_NOTHING, blank=False, null=False)
    fecha_nacimiento = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fecha de nacimiento")
    lugar_nacimiento = models.ForeignKey(Distrito, models.DO_NOTHING, blank=False, null=False,
                                         verbose_name="Lugar de nacimiento")
    nacionalidad = models.ForeignKey(Nacionalidad, models.DO_NOTHING, blank=False, null=False, default=1)
    estado_civil = models.ForeignKey(EstadoCivil, models.DO_NOTHING, blank=False, null=False)
    etnia = models.ForeignKey(Etnia, models.DO_NOTHING, blank=False, null=False, default=1)
    fecha_ingreso = models.DateField(auto_now=True, null=False)
    especialidad = models.ManyToManyField(Especialidad)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    habilitado = models.BooleanField(default=True)


    def __str__(self):
        return self.apellidos + ", " + self.nombres

    def get_full_name(self):
        return '{} {}'.format(self.nombres, self.apellidos)

    def get_dr_full_name(self):
        return '{} {} {}'.format("DR." if self.sexo.codigo == "M" else "DRA.", self.nombres, self.apellidos)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nro_doc = paciente_utils.limpiar_nro_doc(self.nro_doc)
        super(Medico, self).save()

    def get_especialidades(self, id):
        especialidades = ", ".join(self.objects.raw("""
                                     select string_agg(e.nombre, ', ') as especialidades
                                     from consultorios_medico m
                                     join consultorios_medico_especialidad me on m.id = me.medico_id
                                     join consultorios_especialidad e on me.especialidad_id = e.id
                                     where m.id = %d
                                 """, id))
        return especialidades

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"


class Enfermero(models.Model):
    nombres = UpperCharField(max_length=100, blank=False, uppercase=True)
    apellidos = UpperCharField(max_length=100, blank=False, uppercase=True)
    tipo_doc = models.ForeignKey(TipoDoc, models.DO_NOTHING, blank=False, null=False, verbose_name="Tipo de documento")
    nro_doc = UpperCharField(max_length=50, blank=False, null=False, verbose_name="Número de documento", unique=True,
                             uppercase=True)
    nro_registro_profesional = UpperCharField(max_length=50, blank=True, null=True, uppercase=True, unique=True,
                                              verbose_name="Número de Registro Profesional")
    sexo = models.ForeignKey(Sexo, models.DO_NOTHING, blank=False, null=False)
    fecha_nacimiento = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fecha de nacimiento")
    lugar_nacimiento = models.ForeignKey(Distrito, models.DO_NOTHING, blank=False, null=False,
                                         verbose_name="Lugar de nacimiento")
    nacionalidad = models.ForeignKey(Nacionalidad, models.DO_NOTHING, blank=False, null=False, default=1)
    fecha_ingreso = models.DateField(auto_now=True, null=False)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.apellidos + ", " + self.nombres

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nro_doc = paciente_utils.limpiar_nro_doc(self.nro_doc)
        super(Enfermero, self).save()

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "Enfermero"
        verbose_name_plural = "Enfermeros"


class Administrativo(models.Model):
    nombres = UpperCharField(max_length=100, blank=False, uppercase=True)
    apellidos = UpperCharField(max_length=100, blank=False, uppercase=True)
    tipo_doc = models.ForeignKey(TipoDoc, models.DO_NOTHING, blank=False, null=False, verbose_name="Tipo de documento")
    nro_doc = UpperCharField(max_length=50, blank=False, null=False, verbose_name="Número de documento", unique=True,
                             uppercase=True)
    nro_registro_profesional = UpperCharField(max_length=50, blank=False, null=False, uppercase=True,
                                              verbose_name="Número de Registro Profesional")
    sexo = models.ForeignKey(Sexo, models.DO_NOTHING, blank=False, null=False)
    fecha_nacimiento = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fecha de nacimiento")
    lugar_nacimiento = models.ForeignKey(Distrito, models.DO_NOTHING, blank=False, null=False,
                                         verbose_name="Lugar de nacimiento")
    nacionalidad = models.ForeignKey(Nacionalidad, models.DO_NOTHING, blank=False, null=False, default=1)
    fecha_ingreso = models.DateField(auto_now=True, null=False)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.apellidos + ", " + self.nombres

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nro_doc = paciente_utils.limpiar_nro_doc(self.nro_doc)
        super(Administrativo, self).save()

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "Administrativo"
        verbose_name_plural = "Administrativos"


class Departamento(models.Model):
    codigo = UpperCharField(max_length=3, blank=False, primary_key=True, uppercase=True)
    nombre = UpperCharField(max_length=60, blank=False, uppercase=True)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"


class Turno(models.Model):
    codigo = UpperCharField(max_length=1, blank=False, primary_key=True, uppercase=True)
    nombre = UpperCharField(max_length=60, blank=False, uppercase=True)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"


class DiasSemana(models.Model):
    nombre = UpperCharField(max_length=10, uppercase=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["id"]
        verbose_name = "Día"
        verbose_name_plural = "Días"


class HorarioMedico(models.Model):
    medico = models.ForeignKey(Medico, models.DO_NOTHING, blank=False, null=False, verbose_name="Médico")
    hora_inicio = models.TimeField(blank=False, null=False)
    hora_fin = models.TimeField(blank=False, null=False)
    cod_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, blank=False, null=False,
                                         verbose_name="Departamento")
    dia_semana = models.ForeignKey(DiasSemana, models.DO_NOTHING, blank=False, null=False,
                                   verbose_name="Día de la semana")
    turno = models.ForeignKey(Turno, models.DO_NOTHING, blank=False, null=False, verbose_name="Turno")
    cantidad = models.IntegerField(default=20)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.medico.__str__() + '. Día: ' + self.dia_semana.__str__() + '. Turno: ' + self.turno.__str__()

    class Meta:
        ordering = ["medico"]
        verbose_name = "Horario Médico"
        verbose_name_plural = "Horarios de Médicos"


class OrdenEstudio(models.Model):
    nombre = UpperCharField(max_length=100, blank=False, uppercase=True)
    descripcion = UpperCharField(default="", max_length=80, blank=False, uppercase=True, verbose_name="Descripción")

    def __str__(self):
        return "{} ".format(self.nombre)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Orden de Estudio"
        verbose_name_plural = "Ordenes de Estudios"


class OrdenEstudioDetalle(models.Model):
    """En caso de que la orden de estudio sea específica.
    Ejemplo: Para un análisis de sangre, se puede especificar qué se quiere analizar:
    Conteo de globulos rojos, blancos, plaquetas, etc..."""
    orden_estudio = models.ForeignKey(OrdenEstudio, on_delete=DO_NOTHING, verbose_name="Orden de estudio")
    nombre = UpperCharField(uppercase=True, blank=False, max_length=100)
    observacion = UpperTextField(blank=True, uppercase=True)

    def __str__(self):
        return "{} ".format(self.nombre)


class EstadoConsulta(models.Model):
    codigo = UpperCharField(max_length=1, blank=False, primary_key=True, uppercase=True)
    nombre = UpperCharField(max_length=50, blank=False, uppercase=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Estado consulta'
        verbose_name_plural = 'Estados de consulta'


class EstadoConsultaDetalle(models.Model):
    codigo = UpperCharField(max_length=1, blank=False, primary_key=True, uppercase=True)
    nombre = UpperCharField(max_length=50, blank=False, uppercase=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Estado consulta'
        verbose_name_plural = 'Estados de consulta'


class Consulta(models.Model):
    fecha = models.DateField(auto_now=True, blank=False, null=False, verbose_name="Fecha de consulta")
    estado = models.ForeignKey(EstadoConsulta, on_delete=DO_NOTHING, blank=False, null=False)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, blank=True, null=True)
    medico = models.ForeignKey(Medico, models.DO_NOTHING, blank=False, null=False)
    turno = models.ForeignKey(Turno, models.DO_NOTHING, blank=False, null=False)
    # hora_inicio = models.TimeField(auto_now=True)

    def __str__(self):
        return self.fecha

    class Meta:
        ordering = ['fecha']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'


class ConsultaDetalle(models.Model):
    orden = models.IntegerField()
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    consulta = models.ForeignKey(Consulta, models.DO_NOTHING, blank=False, null=False)
    estado = models.ForeignKey(EstadoConsultaDetalle, models.DO_NOTHING, blank=True, null=True)
    confirmado = models.BooleanField(default=False)
    hora_inicio = models.TimeField(auto_now=False, null=True)
    hora_fin = models.TimeField(auto_now=False, null=True)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Detalle de consulta'
        verbose_name_plural = 'Detalles de consulta'


class Tratamiento(models.Model):
    consulta_detalle = models.ForeignKey(ConsultaDetalle, models.DO_NOTHING, blank=False, null=False)
    descripcion = UpperCharField(max_length=255, blank=True, uppercase=True, verbose_name="Descripción")
    observacion = UpperTextField(blank=True, uppercase=True, verbose_name="Observación")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ['consulta_detalle']
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'


class ConsultaOrdenEstudio(models.Model):
    consulta_detalle = models.ForeignKey(ConsultaDetalle, models.DO_NOTHING, blank=False, null=False)
    orden_estudio = models.ForeignKey(OrdenEstudio, models.DO_NOTHING, blank=False, null=False,
                                      verbose_name="Orden de estudio")
    interpretacion = UpperTextField(blank=True, uppercase=True, verbose_name="Interpretación")
    observacion = UpperTextField(blank=True, uppercase=True, verbose_name="Observación")
    fecha_presentacion = models.DateField(auto_now=False, blank=True, null=True, verbose_name="Fecha de presentación")
    fecha_solicitud = models.DateField(auto_now=True, blank=True, null=True, verbose_name="Fecha de solicitud")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.orden_estudio

    class Meta:
        ordering = ['consulta_detalle']
        verbose_name = 'Consulta - Orden de estudio'
        verbose_name_plural = 'Consulta - Órdenes de estudio'


class EvolucionPaciente(models.Model):
    fecha = models.DateField(default=now, null=False)
    hora = models.TimeField(default=now, null=False)
    observaciones = models.TextField(blank=True)
    medico = models.ForeignKey(Medico, on_delete=DO_NOTHING, verbose_name="Firma")
    paciente = models.ForeignKey(Paciente, on_delete=DO_NOTHING)
    consulta_detalle = models.ForeignKey(ConsultaDetalle, on_delete=models.CASCADE, blank=True, null=True, default="")

    class Meta:
        ordering = ['fecha', 'hora']
        verbose_name = 'Evolución del paciente'
        verbose_name_plural = 'Evoluciones del paciente'


class TipoMedicamento(models.Model):
    """Según su tipo de adquisición (VENTA LIBRE, CONTROLADO, PREPARADO)"""
    nombre = UpperCharField(max_length=50, blank=False, uppercase=True)
    descripcion = UpperCharField(max_length=100, blank=True, uppercase=True)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering=["nombre"]
        verbose_name="Tipo de Medicamento"
        verbose_name_plural = "Tipos de Medicamentos"


class Medicamento(models.Model):
    COMPRIMIDO = 'CO'
    CAPSULA = 'CA'
    LIQUIDO_ORAL = 'LO'
    INYECTABLE = 'IN'
    OVULO = 'OV'
    CREMA = 'CR'
    SOLUCION = 'SO'
    AEROSOL = 'AE'
    FORMA_FARMACEUTICA_CHOICES = (
        (COMPRIMIDO, 'COMPRIMIDO'),
        (CAPSULA, 'CAPSULA'),
        (LIQUIDO_ORAL, 'LÍQUIDO ORAL'),
        (INYECTABLE, 'INYECTABLE'),
        (OVULO, 'OVULO'),
        (CREMA, 'CREMA'),
        (SOLUCION, 'SOLUCIÓN'),
        (AEROSOL, 'AEROSOL'),
    )
    nombre = UpperCharField(max_length=100, blank=False, uppercase=True)
    forma_farmaceutica = UpperCharField(max_length=2, choices=FORMA_FARMACEUTICA_CHOICES, blank=False, uppercase=True,
                                        verbose_name="Forma farmacéutica")
    nro_lote = UpperCharField(max_length=100, blank=True, verbose_name="Número de Lote", uppercase=True)
    cantidad = models.IntegerField(blank=False, verbose_name="Cantidad")
    fabricado = models.DateField(auto_now=False, blank=True, null=True, verbose_name="Fecha fabricación")
    vencimiento = models.DateField(auto_now=False, blank=True, null=True, verbose_name="Fecha vencimiento")
    tipificacion = models.ForeignKey(TipoMedicamento, on_delete=models.CASCADE, blank=False, null=False,
                                     verbose_name="Tipificación")
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"


class ConsultaPrescripcion(models.Model):
    consulta_detalle = models.ForeignKey(ConsultaDetalle, models.DO_NOTHING, blank=False, null=False)
    medicamento = models.ForeignKey(Medicamento, models.DO_NOTHING, blank=False, null=False, verbose_name="Medicamento")
    posologia = UpperTextField(blank=True, uppercase=True, verbose_name="POSOLOGIA")
    fecha = models.DateField(auto_now=True, blank=True, null=True, verbose_name="Fecha")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.IntegerField(blank=False, verbose_name="Cantidad")

    def __str__(self):
        return self.consulta_prescripcion

    class Meta:
        ordering = ['consulta_detalle']
        verbose_name = 'Consulta - Prescripción'
        verbose_name_plural = 'Consulta - Prescripciones'


class GrupoAtencion(models.Model):
    codigo = UpperCharField(max_length=2, blank=False, primary_key=True, uppercase=True)
    nombre = UpperCharField(max_length=100, blank=False, uppercase=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Grupo de atención'
        verbose_name_plural = 'Grupos de atención'


class PlanSeguimiento(models.Model):
    consulta_detalle = models.ForeignKey(ConsultaDetalle, models.DO_NOTHING, blank=False, null=False)
    especialidad = models.ForeignKey(Especialidad, models.DO_NOTHING, blank=False, null=False)
    departamento = models.ForeignKey(Departamento, models.DO_NOTHING, blank=False, null=False)
    grupo_atencion = models.OneToOneField(GrupoAtencion, models.DO_NOTHING, blank=False, null=False)

    def __str__(self):
        return self.especialidad

    class Meta:
        ordering = ['consulta_detalle']
        verbose_name = 'Plan de seguimiento'
        verbose_name_plural = 'Planes de seguimiento'


class Anamnesis(models.Model):
    consulta_detalle = models.ForeignKey(ConsultaDetalle, on_delete=models.CASCADE, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=False, null=False)
    # observacion = models.CharField(max_length=250, blank=False, null=False)
    observacion = UpperTextField(blank=True, uppercase=True)

    class Meta:
        verbose_name = 'Anamnesis'
