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


class Producto(models.Model):
    cod_material = models.IntegerField()
    nom_producto = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    cant_existencia = models.IntegerField()
    descripcion = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    stock_minimo = models.IntegerField()
    stock_maximo = models.IntegerField()
    categoria_id = models.IntegerField()

    def __str__(self):
        return self.cod_

    class Meta:
        managed = False
        db_table = 'Producto'
        verbose_name='Producto'
        verbose_name_plural='Productos'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
