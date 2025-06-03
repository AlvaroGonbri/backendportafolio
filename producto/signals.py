from django.db.models.signals import post_save
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
