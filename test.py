# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Asignacion(models.Model):
    asignacionid = models.AutoField(db_column='AsignacionID', primary_key=True)  # Field name made lowercase.
    tecnicoid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='TecnicoID')  # Field name made lowercase.
    productoid = models.ForeignKey('Producto', models.DO_NOTHING, db_column='ProductoID')  # Field name made lowercase.
    cantidadasignada = models.IntegerField(db_column='CantidadAsignada')  # Field name made lowercase.
    fechaasignacion = models.DateTimeField(db_column='FechaAsignacion')  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Asignacion'
