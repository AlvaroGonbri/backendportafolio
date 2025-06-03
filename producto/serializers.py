from rest_framework import serializers
from producto.models import Categoria, Producto, Tipoproducto

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


