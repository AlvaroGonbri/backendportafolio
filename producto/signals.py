from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Producto

@receiver(post_save, sender=Producto)
def alerta_stock(sender, instance, **kwargs):
    producto = instance

    # No hacer nada si la alerta está desactivada o no hay límites definidos
    if not producto.alerta_activa or producto.stock_minimo is None or producto.stock_maximo is None:
        return

    stock_actual = producto.cant_existencia
    umbral_min = producto.stock_minimo
    umbral_max = producto.stock_maximo

    # Alerta de stock bajo
    if stock_actual < umbral_min:
        subject = f"🚨 Alerta de stock bajo: {producto.nom_producto}"
        message = (
            f"Producto: {producto.nom_producto} ({producto.cod_material})\n"
            f"Stock actual: {stock_actual}\n"
            f"Umbral mínimo: {umbral_min}\n\n"
            f"Acción requerida: Por favor reponer stock."
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ALERT_RECIPIENTS,
            fail_silently=False,
        )

    # Alerta de sobrestock
    if stock_actual > umbral_max:
        subject = f"⚠️ Alerta de sobrestock: {producto.nom_producto}"
        message = (
            f"Producto: {producto.nom_producto} ({producto.cod_material})\n"
            f"Stock actual: {stock_actual}\n"
            f"Umbral máximo: {umbral_max}\n\n"
            f"Acción requerida: Por favor revisar el inventario, hay sobrestock."
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ALERT_RECIPIENTS,
            fail_silently=False,
        )

# ✅ ARREGLADO: Usar pre_save para guardar el valor anterior
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

# ✅ ARREGLADO: Ahora _old_cant existe cuando se ejecuta este signal
#@receiver(post_save, sender=Producto)
#def crear_movimiento_actualizacion(sender, instance, created, **kwargs):
 #   if not created and hasattr(instance, '_old_cant'):  # Solo para actualizaciones
  #      old_cantidad = instance._old_cant
   #     nueva_cantidad = instance.cant_existencia
    #    
     #   # Solo crear movimiento si hay diferencia
      #  if old_cantidad != nueva_cantidad:
       #     diferencia = nueva_cantidad - old_cantidad
        #    tipo_movimiento = 'entrada' if diferencia > 0 else 'salida'
            
         #   # Verificar que el modelo MovimientoInventario tenga los campos correctos
          #  try:
           #     MovimientoInventario.objects.create(
            #        producto=instance,
             #       # usuario=getattr(instance, 'ultimo_usuario', None),  # Comentado si no tienes este campo
              #      tipo_movimiento=tipo_movimiento,  # Verificar nombre del campo
               #     cantidad=abs(diferencia),
                #    observacion=f"Ajuste automático de stock: {old_cantidad} → {nueva_cantidad}"  # Verificar nombre del campo
                #)
            #except Exception as e:
             #   print(f"Error creando movimiento: {e}")
              #  # No fallar si hay error en el movimiento
               # pass