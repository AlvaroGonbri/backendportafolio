from django.urls import path, include
from views import *


urlPatters = [
    path('rest/list/', vistaproducto.as_view())

]



-------------------------------------------------------------------------

class Producto(models.Model):
    cod_material = models.IntegerField()
    nom_producto = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    cant_existencia = models.IntegerField()
    descripcion = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    stock_minimo = models.IntegerField()
    stock_maximo = models.IntegerField()
    categoria_id = models.IntegerField()
    tipo = models.ForeignKey('Tipoproducto', models.DO_NOTHING)