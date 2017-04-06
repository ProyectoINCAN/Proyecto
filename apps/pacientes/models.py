from django.db import models

# Create your models here.
from django.utils.timezone import now


class TipoDoc(models.Model):
    codigo = models.CharField(max_length=3, blank=False, primary_key=True)
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
    codigo = models.CharField(max_length=1, blank=False, primary_key=True)
    descripcion = models.CharField(max_length=30, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["descripcion"]
        verbose_name = "Sexo"
        verbose_name_plural = "Sexos"


class EstadoCivil(models.Model):
    codigo = models.CharField(max_length=2, blank=False, primary_key=True)
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
        ordering = ["nombre"]
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
    codigo = models.CharField(max_length=3, blank=False, primary_key=True)
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
    codigo = models.CharField(max_length=2, blank=False, primary_key=True)
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
    codigo = models.CharField(max_length=2, blank=False, primary_key=True)
    descripcion = models.CharField(max_length=50, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Situación Laboral"
        verbose_name_plural = "Situaciones Laborales"


class Paciente(models.Model):
    nombres = models.CharField(max_length=100, blank=False)
    apellidos = models.CharField(max_length=100, blank=False)
    tipo_doc = models.ForeignKey(TipoDoc, models.DO_NOTHING, blank=False, null=False, verbose_name="Tipo de documento")
    nro_doc = models.CharField(max_length=15, blank=True, null=False, verbose_name="Número de documento", unique=True)  #si no tiene nrodoc, por defecto debe guardar INICIAL_NOMBRE+INICIAL_APELLIDO+FECHA_NACIMIENTO
    sexo = models.ForeignKey(Sexo, models.DO_NOTHING, blank=False, null=False)                                          #Redefinir la función save para setee el dato en esos casos
    fecha_nacimiento = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fecha de nacimiento")
    lugar_nacimiento = models.ForeignKey(Localidad, models.DO_NOTHING, blank=False, null=False, verbose_name="Lugar de nacimiento")
    nacionalidad = models.ForeignKey(Pais, models.DO_NOTHING, blank=False, null=False)
    estado_civil = models.ForeignKey(EstadoCivil, models.DO_NOTHING, blank=False, null=False)
    etnia = models.ForeignKey(Etnia, models.DO_NOTHING, blank=False, null=False)
    fecha_registrado = models.DateTimeField(default=now, null=False)  # en el admin.py poner "exclude = ('fecha_registrado',)" para que no se muestre el campo


    #nivel_educativo = models.ForeignKey(PacienteNivelEducativo, models.DO_NOTHING, default="", blank=False, null=False)
    #seguro_medico = models.ForeignKey(SeguroMedico, models.DO_NOTHING, blank=False, null=False, verbose_name="Seguro médico")
    #situacion_laboral = models.ForeignKey(SituacionLaboral, models.DO_NOTHING, blank=False, null=False, verbose_name="Situación laboral")
    #profesion = models.ManyToManyField(Profesion, verbose_name='Profesión')
    #ocupacion = models.ForeignKey(PacienteOcupacion, models.DO_NOTHING, default="", blank=False, null=False, verbose_name="Ocupación")


    def __str__(self):
        return self.apellidos + ", " + self.nombres

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"


class Direccion(models.Model):
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)
    descripcion = models.CharField(max_length=100, blank=False)
    region = models.ForeignKey(Region, models.SET_NULL, blank=True, null=True, )
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
    codigo = models.CharField(max_length=1, blank=False, primary_key=True)
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
    codigo = models.CharField(max_length=1, blank=False, verbose_name='código', primary_key=True)
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
        return self.direccion

    class Meta:
        ordering = ['paciente', 'id']
        verbose_name = 'Correo Electrónico'
        verbose_name_plural = 'Correos Electrónicos'

# TODO class paciente padres
# class PacientePadre(models.Model):
#     nombres = models.CharField(max_length=100, blank=False)
#     apellidos = models.CharField(max_length=100, blank=False)
#     tipo_doc = models.ForeignKey(TipoDoc, models.DO_NOTHING, blank=False, null=False, verbose_name="Tipo de documento")
#     nro_doc = models.CharField(max_length=15, blank=False, null=False, verbose_name="Número de documento", unique=True)
#     sexo = models.ForeignKey(Sexo, models.DO_NOTHING, blank=False, null=False)
#     fecha_nacimiento = models.DateField(auto_now=False, blank=False, null=False, verbose_name="Fecha de nacimiento")
#     lugar_nacimiento = models.ForeignKey(Localidad, models.DO_NOTHING, blank=False, null=False,
#                                          verbose_name="Lugar de nacimiento")
#     nacionalidad = models.ForeignKey(Pais, models.DO_NOTHING, blank=False, null=False)
#     estado_civil = models.ForeignKey(EstadoCivil, models.DO_NOTHING, blank=False, null=False)
#     etnia = models.ForeignKey(Etnia, models.DO_NOTHING, blank=False, null=False)
#     nivel_educativo = models.ForeignKey(NivelEducativo, models.DO_NOTHING, blank=False, null=False)
#     seguro_medico = models.ForeignKey(SeguroMedico, models.DO_NOTHING, blank=False, null=False,
#                                       verbose_name="Seguro médico")
#     situacion_laboral = models.ForeignKey(SituacionLaboral, models.DO_NOTHING, blank=False, null=False,
#                                           verbose_name="Situación laboral")
#     profesion = models.ManyToManyField(Profesion, verbose_name='Profesión')
#     fecha_registrado = models.DateTimeField(default=now,
#                                             null=False)  # en el admin.py poner "exclude = ('fecha_registrado',)" para que no se muestre el campo
#
#     def __str__(self):
#         return self.apellidos + ", " + self.nombre
#
#     class Meta:
#         ordering = ['id']
#         verbose_name = 'Padre'
#         verbose_name_plural = 'Padres'


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


class PacienteProfesion(models.Model):
    profesion = models.ForeignKey(Profesion, models.DO_NOTHING, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False)  # relacion con el paciente

    def __str__(self):
        return self.profesion

    class Meta:
        ordering = ["profesion"]
        verbose_name = "Profesión de Paciente"
        verbose_name_plural = "Profesiones de Pacientes"


class PacienteNivelEducativo(models.Model):
    nivel_educativo = models.ForeignKey(NivelEducativo, models.DO_NOTHING, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, models.SET_NULL,blank=True,null=True,) #relacion con el paciente
    completo = models.BooleanField(default=True)
    anho_cursado = verbose_name="Año Cursado"

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nivel_educativo_id"]
        verbose_name = "Paciente Nivel Educativo"
        verbose_name_plural = "Paciente Niveles Educativos"


#paciente situacion laboral
class PacienteOcupacion(models.Model):
    paciente = models.ForeignKey(Paciente, models.SET_NULL, blank=True, null=True, )
    situacion_laboral_id = models.ForeignKey(SituacionLaboral, models.DO_NOTHING, blank=False, null=False)
    ocupacion = models.ForeignKey(Ocupacion, models.DO_NOTHING, blank=False, null=False)
    #renumeracion = models.BooleanField(default=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.profesion

    class Meta:
        ordering = ["paciente"]
        verbose_name = "Paciente Ocupación"
        verbose_name_plural = "Paciente Ocupación"


class PacienteSeguroMedico(models.Model):
    seguro_medico = models.ForeignKey(SeguroMedico, models.DO_NOTHING, blank=False, null=False)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, blank=False, null=False) #relacion con el paciente


    def __str__(self):
        return self.seguro_medico

    class Meta:
        ordering = ["seguro_medico"]
        verbose_name = "Paciente Seguro Médico"
        verbose_name_plural = "Paciente Seguro Médico"


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


class Desague(models.Model):
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
    desagua = models.ForeignKey(Desague, models.DO_NOTHING, blank=False, null=False)

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

