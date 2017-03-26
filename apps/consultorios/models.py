from django.db import models

# Create your models here.
class Consultorio(models.Model):
    descripcion = models.CharField(max_length=100, blank=False)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ["id"]
        verbose_name = "Consultorio"
        verbose_name_plural = "Consultorios"

