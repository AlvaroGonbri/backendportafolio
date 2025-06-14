from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Movimiento, Producto, Categoria, Tipoproducto, Asignacion
from .serializers import (
    MovimientoSerializer, ProductoSerializer, CategoriaSerializer, TipoproductoSerializer,
    AsignacionSerializer, UserSerializer
)
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from django.contrib.auth.models import User



# Vista para listar y crear productos
class vistaproducto(APIView):
    def get(self, request):
        data = Producto.objects.order_by('-cod_material').all()
        serializer = ProductoSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para detalle, actualización y borrado de productos
class ProductoDetalle(APIView):
    # ... (mantén tu código existente aquí) ...
    pass

# ViewSets para categorías, tipos y técnicos
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class TipoproductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tipoproducto.objects.all()
    serializer_class = TipoproductoSerializer

class TecnicoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(groups__name='Tecnico')
    
class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        producto_id = data.get('productoid')
        cantidad = int(data.get('cantidadasignada', 0))

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return Response(
                {'error': 'Producto no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        if producto.cant_existencia < cantidad:
            return Response(
                {'error': 'Stock insuficiente'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear la asignación
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Actualizar stock ANTES de crear el movimiento
        producto.cant_existencia -= cantidad
        producto.save()

        # Crear movimiento de salida DESPUÉS de actualizar stock
        Movimiento.objects.create(
            producto=producto,
            tipo='salida',
            cantidad=cantidad,
            usuario=request.user,
            observacion=f"Asignación a técnico ID: {data.get('tecnicoid')}"
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=['GET'], url_path=r'por-tecnico/(?P<tecnico_id>\d+)')
    def por_tecnico(self, request, tecnico_id=None):
        asignaciones = Asignacion.objects.filter(tecnicoid=tecnico_id)
        serializer = self.get_serializer(asignaciones, many=True)
        return Response(serializer.data)

# ... (resto de las vistas sin cambios)

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all().order_by('-fecha')
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated]