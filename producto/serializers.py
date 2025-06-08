from rest_framework import serializers
from producto.models import Categoria, Producto, Tipoproducto
from .models import AuditoriaProducto

class TipoproductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoproducto
        fields = ['id', 'nombre']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id_categoria', 'nom_categoria']

tipo = TipoproductoSerializer(read_only=True) 

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True,
        required=False  # Permite omitir en actualizaciones parciales (PATCH)
    )
    tipo = TipoproductoSerializer(read_only=True)
    tipo_nombre = serializers.SlugRelatedField(
        source='tipo',
        slug_field='nombre',
        read_only=True
    )
    
    tipo_id = serializers.PrimaryKeyRelatedField(
        queryset=Tipoproducto.objects.all(),
        source='tipo',
        write_only=True,
        required=False  # Permite omitir en actualizaciones parciales (PATCH)
    )

    class Meta:
        model = Producto
        fields = [
            'id',
            'cod_material',
            'nom_producto',
            'cant_existencia',
            'descripcion',
            'stock_minimo',
            'stock_maximo',
            'categoria_id',
            'categoria',
            'tipo',
            'tipo_id',
            'tipo_nombre'
        ]

#class MovimientoInventarioSerializer(serializers.ModelSerializer):
 #   producto_nombre = serializers.CharField(source='producto.nom_producto', read_only=True)
  #  tecnico_email = serializers.CharField(source='tecnico.email', read_only=True)

   # class Meta:
    #    model = MovimientoInventario
     #   fields = '__all__'


class AuditoriaProductoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    accion_display = serializers.CharField(source='get_accion_display', read_only=True)
    diferencia_stock = serializers.ReadOnlyField()
    tiempo_transcurrido = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditoriaProducto
        fields = [
            'id', 'producto_id', 'codigo_material', 'nombre_producto',
            'accion', 'accion_display', 'descripcion',
            'cantidad_anterior', 'cantidad_nueva', 'diferencia_stock',
            'datos_anteriores', 'datos_nuevos',
            'usuario', 'usuario_nombre', 'fecha_accion', 'tiempo_transcurrido',
            'ip_address', 'observaciones', 'categoria', 'tipo_producto'
        ]
        read_only_fields = ['fecha_accion', 'usuario']
    
    def get_tiempo_transcurrido(self, obj):
        """Devuelve tiempo transcurrido en formato legible"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.fecha_accion
        
        if diff.days > 0:
            return f"Hace {diff.days} días"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"Hace {hours} horas"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"Hace {minutes} minutos"
        else:
            return "Hace un momento"


