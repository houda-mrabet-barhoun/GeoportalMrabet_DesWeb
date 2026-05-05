from django.db import models
from django.contrib.gis.db import models as gis_models


class Barrio(models.Model):
    nombre = models.TextField()
    codigo = models.TextField()
    distrito = models.TextField()
    area = models.FloatField()
    numero_clientes = models.IntegerField()
    geom = gis_models.PolygonField(srid=25830, blank=True, null=True)

    class Meta:
        db_table = "d.barrios"


class Cliente(models.Model):
    nombre = models.TextField()
    direccion = models.TextField()
    telefono = models.TextField()
    tipo_cliente = models.TextField()
    barrio = models.TextField()
    geom = gis_models.PointField(srid=25830, blank=True, null=True)

    class Meta:
        db_table = "d.clientes"


class Ruta(models.Model):
    distancia = models.FloatField()
    tiempo = models.IntegerField()
    estado = models.TextField()
    barrio_destino = models.TextField()
    numero_paradas = models.IntegerField()
    geom = gis_models.LineStringField(srid=25830, blank=True, null=True)

    class Meta:
        db_table = "d.rutas"
