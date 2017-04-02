from django.db import models

# Create your models here.
from django.utils.timezone import now


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

    def __str__(self):
        return self.descripcion

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


class Etnia(models.Model):
    nombre = models.CharField(max_length=30, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["id"]
        verbose_name = "Etnia"
        verbose_name_plural = "Etnias"


class Profesion(models.Model):
    nombre = models.CharField(max_length=30, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Profesión"
        verbose_name_plural = "Profesiones"


class Pais(models.Model):
    codigo = models.CharField(max_length=3, blank=False)
    nombre = models.CharField(max_length=30, blank=False)
    nombre_iso = models.CharField(max_length=30, blank=False)
    codigo_alpha3 = models.CharField(max_length=3, blank=False)
    codigo_numerico = models.IntegerField(blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "País"
        verbose_name_plural = "Países"


class Region(models.Model):
    nombre = models.CharField(max_length=60, blank=False)
    pais = models.ForeignKey(Pais, models.SET_NULL, blank=True,null=True,)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Región"
        verbose_name_plural = "Regiones"


class Localidad(models.Model):
    nombre = models.CharField(max_length=60, blank=False)
    region = models.ForeignKey(Region, models.SET_NULL, blank=True,null=True,)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"


class Barrio(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    localidad = models.ForeignKey(Localidad, models.SET_NULL, blank=True,null=True,)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Barrio"
        verbose_name_plural = "Barrios"


class SeguroMedico(models.Model):
    nombre = models.CharField(max_length=60, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Seguro Médico"
        verbose_name_plural = "Seguros Médicos"


class Area(models.Model):
    codigo = models.CharField(max_length=2, blank=False)
    nombre = models.CharField(max_length=60, blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Área"
        verbose_name_plural = "Áreas"


class Ocupacion(models.Model):
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["descripcion"]
        verbose_name = "Ocupación"
        verbose_name_plural = "Ocupaciones"


class SituacionLaboral(models.Model):
    codigo = models.CharField(max_length=2, blank=False)
    descripcion = models.CharField(max_length=50, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["id"]
        verbose_name = "Situación Laboral"
        verbose_name_plural = "Situaciones Laborales"


class PacienteOcupacion(models.Model):
    situacion_laboral_id = models.ForeignKey(SituacionLaboral, models.DO_NOTHING, blank=False, null=False)
    ocupacion_id = models.ForeignKey(Ocupacion, models.DO_NOTHING, blank=False, null=False)
    #renumeracion = models.BooleanField(default=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.profesion

    class Meta:
        ordering = ["situacion_laboral_id"]
        verbose_name = "Ocupación del Paciente"
        verbose_name_plural = "Ocupaciones del Paciente"



class PacienteNivelEducativo(models.Model):
    nivel_educativo_id = models.ForeignKey(NivelEducativo, models.DO_NOTHING, blank=False, null=False)
    completo = models.BooleanField(default=True)
    anho_cursado = verbose_name="Año Cursado"

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nivel_educativo_id"]
        verbose_name = "Nivel Educativo"
        verbose_name_plural = "Niveles Educativos"


class Paciente(models.Model):
    nombres = models.CharField(max_length=100, blank=False)
    apellidos = models.CharField(max_length=100, blank=False)
    tipo_doc = models.ForeignKey(TipoDoc, models.DO_NOTHING, blank=False, null=False, verbose_name="Tipo de documento")
    nro_doc = models.CharField(max_length=15, blank=False, null=False, verbose_name="Número de documento", unique=True)
    sexo = models.ForeignKey(Sexo, models.DO_NOTHING, blank=False, null=False)
    fecha_nacimiento = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fecha de nacimiento")
    lugar_nacimiento = models.ForeignKey(Localidad, models.DO_NOTHING, blank=False, null=False, verbose_name="Lugar de nacimiento")
    nacionalidad = models.ForeignKey(Pais, models.DO_NOTHING, blank=False, null=False)
    estado_civil = models.ForeignKey(EstadoCivil, models.DO_NOTHING, blank=False, null=False)
    etnia = models.ForeignKey(Etnia, models.DO_NOTHING, blank=False, null=False)
    nivel_educativo = models.ForeignKey(PacienteNivelEducativo, models.DO_NOTHING, default="", blank=False, null=False)
    seguro_medico = models.ForeignKey(SeguroMedico, models.DO_NOTHING, blank=False, null=False, verbose_name="Seguro médico")
    situacion_laboral = models.ForeignKey(SituacionLaboral, models.DO_NOTHING, blank=False, null=False, verbose_name="Situación laboral")
    profesion = models.ManyToManyField(Profesion, verbose_name='Profesión')
    ocupacion = models.ForeignKey(PacienteOcupacion, models.DO_NOTHING, default="", blank=False, null=False, verbose_name="Ocupación")
    fecha_registrado = models.DateTimeField(default=now, null=False) #en el admin.py poner "exclude = ('fecha_registrado',)" para que no se muestre el campo

    def __str__(self):
        return self.apellidos + ", " + self.nombres

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"


class Direccion(models.Model):
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    descripcion = models.CharField(max_length=100, blank=False)
    localidad = models.ForeignKey(Localidad, models.DO_NOTHING, blank=False, null=False)
    barrio = models.ForeignKey(Barrio, models.DO_NOTHING, blank=False, null=False)
    area = models.ForeignKey(Area, models.DO_NOTHING, blank=False, null=False)
    sector = models.CharField(max_length=100, blank=False)
    manzana = models.CharField(max_length=60, blank=False)
    nro_casa = models.IntegerField(blank=False)
    residencia_ocasional = models.CharField(max_length=300, blank=False)
    referencia = models.CharField(max_length=200, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["paciente"]
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"


class MedidaPaciente(models.Model):
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    peso = models.IntegerField(blank=False)
    talla = models.IntegerField(blank=False)

    def __str__(self):
        return self.peso + ", " + self.talla

    class Meta:
        ordering = ["id"]
        verbose_name = "Medida del Paciente"
        verbose_name_plural = "Medidas del Paciente"


class TipoTelefono(models.Model):
    codigo = models.CharField(max_length=1, blank=False)
    descripcion = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ['descripcion']
        verbose_name = 'Tipo de teléfono'
        verbose_name_plural = 'Tipos de teléfono'


class Telefono(models.Model):
    numero = models.CharField(max_length=80, blank=False, null=False)
    tipo = models.ForeignKey(TipoTelefono, models.DO_NOTHING, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.peso + ", " + self.talla

    class Meta:
        ordering = ['paciente', 'id']
        verbose_name = 'Teléfono'
        verbose_name_plural = 'Teléfonos'


class TipoCorreoElectronico(models.Model):
    codigo = models.CharField(max_length=1, blank=False, verbose_name='código')
    descripcion = models.CharField(max_length=50, blank=False, verbose_name='descripción')

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ['descripcion']
        verbose_name = 'Tipo de correo electrónico'
        verbose_name_plural = 'Tipos de correo electrónico'


class CorreoElectronico(models.Model):
    direccion = models.CharField(max_length=100, blank=False, null=False, verbose_name='dirección')
    tipo = models.ForeignKey(TipoCorreoElectronico, models.DO_NOTHING, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.peso + ", " + self.talla

    class Meta:
        ordering = ['paciente', 'id']
        verbose_name = 'Correo Electrónico'
        verbose_name_plural = 'Correos Electrónicos'


class Acompañante(models.Model):
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    nombres = models.CharField(max_length=100, blank=False)
    apellidos = models.CharField(max_length=100, blank=False)
    nro_doc = models.CharField(max_length=15, blank=False, null=False, verbose_name="Número de documento", unique=True)
    telefono = models.ForeignKey(Telefono, models.DO_NOTHING, blank=False, null=False)
    vinculo = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombres"]
        verbose_name = "Acompañante"
        verbose_name_plural = "Acompañantes"