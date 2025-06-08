# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Asignacion(models.Model):
    asignacionid = models.AutoField(db_column='AsignacionID', primary_key=True)  # Field name made lowercase.
    tecnicoid = models.IntegerField(db_column='TecnicoID')  # Field name made lowercase.
    productoid = models.IntegerField(db_column='ProductoID')  # Field name made lowercase.
    cantidadasignada = models.DecimalField(db_column='CantidadAsignada', max_digits=10, decimal_places=2)  # Field name made lowercase.
    fechaasignacion = models.DateTimeField(db_column='FechaAsignacion')  # Field name made lowercase.
    fechadevolucionesperada = models.DateField(db_column='FechaDevolucionEsperada', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Asignacion'


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nom_categoria = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'Categoria'


class Configuracionmulta(models.Model):
    configuracionmultaid = models.AutoField(db_column='ConfiguracionMultaID', primary_key=True)  # Field name made lowercase.
    montopordia = models.DecimalField(db_column='MontoPorDia', max_digits=10, decimal_places=2)  # Field name made lowercase.
    maximodiassinmulta = models.IntegerField(db_column='MaximoDiasSinMulta')  # Field name made lowercase.
    activo = models.BooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ConfiguracionMulta'


class Historialmulta(models.Model):
    historialmultaid = models.AutoField(db_column='HistorialMultaID', primary_key=True)  # Field name made lowercase.
    multaid = models.ForeignKey('Multa', models.DO_NOTHING, db_column='MultaID')  # Field name made lowercase.
    estadoanterior = models.CharField(db_column='EstadoAnterior', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    estadonuevo = models.CharField(db_column='EstadoNuevo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fechacambio = models.DateTimeField(db_column='FechaCambio')  # Field name made lowercase.
    usuarioid = models.IntegerField(db_column='UsuarioID')  # Field name made lowercase.
    observacion = models.CharField(db_column='Observacion', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HistorialMulta'


class Multa(models.Model):
    multaid = models.AutoField(db_column='MultaID', primary_key=True)  # Field name made lowercase.
    asignacionid = models.ForeignKey(Asignacion, models.DO_NOTHING, db_column='AsignacionID')  # Field name made lowercase.
    diasretraso = models.IntegerField(db_column='DiasRetraso')  # Field name made lowercase.
    montopordia = models.DecimalField(db_column='MontoPorDia', max_digits=10, decimal_places=2)  # Field name made lowercase.
    montototal = models.DecimalField(db_column='MontoTotal', max_digits=10, decimal_places=2)  # Field name made lowercase.
    fechageneracion = models.DateTimeField(db_column='FechaGeneracion')  # Field name made lowercase.
    estadopago = models.CharField(db_column='EstadoPago', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fechapago = models.DateTimeField(db_column='FechaPago', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Multa'


class Notificacion(models.Model):
    notificacionid = models.AutoField(db_column='NotificacionID', primary_key=True)  # Field name made lowercase.
    usuarioid = models.IntegerField(db_column='UsuarioID')  # Field name made lowercase.
    mensaje = models.CharField(db_column='Mensaje', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha')  # Field name made lowercase.
    leida = models.BooleanField(db_column='Leida')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Notificacion'

class Tipoproducto(models.Model):
    nombre = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        db_table = 'TipoProducto'


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    cod_material = models.IntegerField()
    nom_producto = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    cant_existencia = models.IntegerField()
    descripcion = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    stock_minimo = models.IntegerField()
    stock_maximo = models.IntegerField()
    categoria = models.ForeignKey(
        'Categoria',
        on_delete=models.PROTECT,
        db_column='categoria_id'
    )
    
    tipo = models.ForeignKey(
        Tipoproducto, 
        on_delete=models.PROTECT,
        db_column='tipo_id'
    )
    alerta_activa = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.cod_material} - {self.nom_producto}"

    class Meta:
        db_table = 'Producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        

#class MovimientoInventario(models.Model):
 #   TIPO_MOVIMIENTO = [
  #      ('entrada', 'Entrada'),
   #     ('salida', 'Salida'),
    #    ('asignacion', 'Asignación a técnico')
    #]
    
#    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
#    tecnico = models.ForeignKey(
#        User, 
#        on_delete=models.PROTECT,
#        related_name='movimientos_tecnico'
#    )  # Usuario destinatario (técnico)
#    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
#    cantidad = models.IntegerField()
#    fecha = models.DateTimeField(auto_now_add=True)
#    observaciones = models.TextField(blank=True)
#    usuario = models.ForeignKey(
#        User, 
#        on_delete=models.PROTECT,
#        related_name='movimientos_registrados'
#    )  # Usuario que registra la transacción

 #   class Meta:
 #       db_table = 'MovimientoInventario'
 #       indexes = [
 #          models.Index(fields=['fecha']),
 #           models.Index(fields=['producto']),
 #           models.Index(fields=['tecnico']),
 #           models.Index(fields=['usuario']),
 #       ]


class AuditoriaProducto(models.Model):
    ACCIONES = [
        ('crear', 'Producto Creado'),
        ('editar', 'Producto Editado'),
        ('eliminar', 'Producto Eliminado'),
        ('stock_entrada', 'Entrada de Stock'),
        ('stock_salida', 'Salida de Stock'),
        ('asignacion', 'Producto Asignado'),
        ('devolucion', 'Producto Devuelto'),
    ]
    
    # Información del producto
    producto_id = models.IntegerField(help_text="ID del producto afectado")
    codigo_material = models.CharField(max_length=50, null=True, blank=True)
    nombre_producto = models.CharField(max_length=200, null=True, blank=True)
    
    # Información de la acción
    accion = models.CharField(max_length=20, choices=ACCIONES)
    descripcion = models.TextField(help_text="Descripción detallada de la acción")
    
    # Datos del cambio
    cantidad_anterior = models.IntegerField(null=True, blank=True)
    cantidad_nueva = models.IntegerField(null=True, blank=True)
    datos_anteriores = models.JSONField(null=True, blank=True, help_text="Estado anterior del producto")
    datos_nuevos = models.JSONField(null=True, blank=True, help_text="Estado nuevo del producto")
    
    # Información de auditoría
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario que realizó la acción")
    fecha_accion = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    # Información adicional
    observaciones = models.TextField(null=True, blank=True)
    categoria = models.CharField(max_length=100, null=True, blank=True)
    tipo_producto = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'auditoria_producto'
        ordering = ['-fecha_accion']
        indexes = [
            models.Index(fields=['producto_id']),
            models.Index(fields=['accion']),
            models.Index(fields=['fecha_accion']),
            models.Index(fields=['usuario']),
            models.Index(fields=['codigo_material']),
        ]
        
    def __str__(self):
        return f"{self.get_accion_display()} - {self.nombre_producto} por {self.usuario.username}"
    
    @property
    def diferencia_stock(self):
        """Calcula la diferencia de stock si aplica"""
        if self.cantidad_anterior is not None and self.cantidad_nueva is not None:
            return self.cantidad_nueva - self.cantidad_anterior
        return None