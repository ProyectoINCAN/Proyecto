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
    pais = models.ForeignKey(Pais,  models.SET_NULL, blank=True,null=True,)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Región"
        verbose_name_plural = "Regiones"


class Localidad(models.Model):
    nombre = models.CharField(max_length=60, blank=False)
    region = models.ForeignKey(Region,  models.SET_NULL, blank=True,null=True,)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"


class Barrio(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    localidad = models.ForeignKey(Localidad,  models.SET_NULL, blank=True,null=True,)
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
