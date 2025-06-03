from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Producto

@receiver(post_save, sender=Producto)
def alerta_stock_bajo(sender, instance, **kwargs):
    print("SEÑAL EJECUTADA - producto:", instance.id_producto.nombre)
    producto = instance.id_producto
    
    if producto.stock_minimo is None:
        return
    
    if not producto.alerta_activa:  # Verifica si la alerta está activa
        return

    stock_actual = instance.cantidad
    umbral = producto.stock_minimo

    if stock_actual < umbral:  # <-- Condición simplificada
        ubicacion = instance.id_ubicacion.nombre if instance.id_ubicacion else 'Sin ubicación'
        lote = instance.id_lote.numero_lote if instance.id_lote else 'N/A'
        
        subject = f"🚨 Alerta de stock bajo: {producto.nombre}"
        message = (
            f"Producto: {producto.nombre} ({producto.codigo_producto})\n"
            f"Stock actual: {stock_actual}\n"
            f"Umbral mínimo: {umbral}\n"
            f"Ubicación: {ubicacion}\n"
            f"Lote: {lote}\n\n"
            f"Acción requerida: Por favor reponer stock."
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ALERT_RECIPIENTS,
            fail_silently=False,
        )
