from rest_framework import serializers
from producto.models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        extra_kwargs = {
            'cod_material': {'read_only': True}  # Auto-incremental
        }