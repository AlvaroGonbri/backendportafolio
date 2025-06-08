from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Producto, AuditoriaProducto
import json

# Variable global para almacenar datos anteriores
_productos_anteriores = {}

@receiver(pre_save, sender=Producto)
def guardar_valor_anterior(sender, instance, **kwargs):
    if instance.pk:  # Solo si ya existe en la DB
        try:
            old_instance = Producto.objects.get(pk=instance.pk)
            instance._old_cant = old_instance.cant_existencia
        except Producto.DoesNotExist:
            instance._old_cant = 0
    else:
        instance._old_cant = 0

@receiver(pre_save, sender=Producto)
def guardar_estado_anterior(sender, instance, **kwargs):
    """Guarda el estado anterior del producto antes de modificarlo"""
    if instance.pk:  # Solo si ya existe
        try:
            producto_anterior = Producto.objects.get(pk=instance.pk)
            _productos_anteriores[instance.pk] = {
                'cod_material': producto_anterior.cod_material,
                'nom_producto': producto_anterior.nom_producto,
                'cant_existencia': producto_anterior.cant_existencia,
                'descripcion': producto_anterior.descripcion,
                'stock_minimo': producto_anterior.stock_minimo,
                'stock_maximo': producto_anterior.stock_maximo,
                'categoria': producto_anterior.categoria.nom_categoria if producto_anterior.categoria else None,
                'tipo': producto_anterior.tipo.nombre if producto_anterior.tipo else None,  # ✅ CORREGIDO
            }
        except Producto.DoesNotExist:
            _productos_anteriores[instance.pk] = None

@receiver(post_save, sender=Producto)
def registrar_auditoria_producto(sender, instance, created, **kwargs):
    """Registra automáticamente todas las acciones sobre productos"""
    
    # Obtener usuario del contexto
    usuario = getattr(instance, '_usuario_auditoria', None)
    ip_address = getattr(instance, '_ip_auditoria', None)
    
    # ✅ FORZAR USUARIO SI ES NULL
    if not usuario:
        from django.contrib.auth.models import User
        try:
            usuario = User.objects.first()
            print(f"🔥 SIGNAL: Usuario forzado a {usuario}")
        except:
            print("🔥 SIGNAL: No hay usuarios en la base de datos")
            return  # No crear auditoría si no hay usuarios
    
    if created:
        # Producto creado
        AuditoriaProducto.objects.create(
            producto_id=instance.id,
            codigo_material=instance.cod_material,
            nombre_producto=instance.nom_producto,
            accion='crear',
            descripcion=f"Nuevo producto creado: {instance.nom_producto} ({instance.cod_material})",
            cantidad_nueva=instance.cant_existencia,
            datos_nuevos={
                'cod_material': instance.cod_material,
                'nom_producto': instance.nom_producto,
                'cant_existencia': instance.cant_existencia,
                'descripcion': instance.descripcion,
                'categoria': instance.categoria.nom_categoria if instance.categoria else None,
                'tipo': instance.tipo.nombre if instance.tipo else None,
            },
            usuario=usuario,  # ✅ Ya no será None
            ip_address=ip_address,
            categoria=instance.categoria.nom_categoria if instance.categoria else None,
            tipo_producto=instance.tipo.nombre if instance.tipo else None,
        )
    else:
        # Producto editado
        datos_anteriores = _productos_anteriores.get(instance.pk, {})
        
        cambios = []
        cantidad_anterior = None
        
        if datos_anteriores:
            # Detectar cambios específicos
            if datos_anteriores.get('cant_existencia') != instance.cant_existencia:
                cantidad_anterior = datos_anteriores.get('cant_existencia')
                diff = instance.cant_existencia - cantidad_anterior
                if diff > 0:
                    cambios.append(f"Stock aumentado en {diff} unidades")
                else:
                    cambios.append(f"Stock reducido en {abs(diff)} unidades")
            
            if datos_anteriores.get('nom_producto') != instance.nom_producto:
                cambios.append(f"Nombre cambiado de '{datos_anteriores.get('nom_producto')}' a '{instance.nom_producto}'")
            
            if datos_anteriores.get('descripcion') != instance.descripcion:
                cambios.append("Descripción actualizada")
                
            if datos_anteriores.get('stock_minimo') != instance.stock_minimo:
                cambios.append(f"Stock mínimo cambiado a {instance.stock_minimo}")
                
            if datos_anteriores.get('stock_maximo') != instance.stock_maximo:
                cambios.append(f"Stock máximo cambiado a {instance.stock_maximo}")
        
        descripcion = f"Producto editado: {'. '.join(cambios)}" if cambios else "Producto editado"
        
        # Determinar tipo de acción basado en cambio de stock
        accion = 'editar'
        if cantidad_anterior is not None and cantidad_anterior != instance.cant_existencia:
            if instance.cant_existencia > cantidad_anterior:
                accion = 'stock_entrada'
            else:
                accion = 'stock_salida'
        
        AuditoriaProducto.objects.create(
            producto_id=instance.id,
            codigo_material=instance.cod_material,
            nombre_producto=instance.nom_producto,
            accion=accion,
            descripcion=descripcion,
            cantidad_anterior=cantidad_anterior,
            cantidad_nueva=instance.cant_existencia,
            datos_anteriores=datos_anteriores,
            datos_nuevos={
                'cod_material': instance.cod_material,
                'nom_producto': instance.nom_producto,
                'cant_existencia': instance.cant_existencia,
                'descripcion': instance.descripcion,
                'categoria': instance.categoria.nom_categoria if instance.categoria else None,
                'tipo': instance.tipo.nombre if instance.tipo else None,
            },
            usuario=usuario,  # ✅ Ya no será None
            ip_address=ip_address,
            categoria=instance.categoria.nom_categoria if instance.categoria else None,
            tipo_producto=instance.tipo.nombre if instance.tipo else None,
        )
        
        # Limpiar datos anteriores
        if instance.pk in _productos_anteriores:
            del _productos_anteriores[instance.pk]