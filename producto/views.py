from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AuditoriaProducto, Producto, Categoria, Tipoproducto
from .serializers import AuditoriaProductoSerializer, ProductoSerializer, CategoriaSerializer, TipoproductoSerializer
from rest_framework import status, viewsets, generics
#from .serializers import MovimientoInventarioSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


# Create your views here.

class ProductoDetalle(APIView):

    def get_object(self, pk):
        try:
            return Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return None
        
    def patch(self, request, pk):
        producto = self.get_object(pk)
        if producto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        producto = self.get_object(pk)
        if producto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

    def put(self, request, pk):
        producto = self.get_object(pk)
        if producto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        producto = self.get_object(pk)
        if producto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class TipoproductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tipoproducto.objects.all()
    serializer_class = TipoproductoSerializer

class ProductoUpdateAPIView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'id'  # Campo para buscar el producto (puede ser 'pk', 'cod_material', etc.)

    def patch(self, request, *args, **kwargs):
        producto = self.get_object()
        serializer = self.get_serializer(producto, data=request.data, partial=True)  # partial=True permite actualización parcial
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

#class MovimientoInventarioViewSet(viewsets.ModelViewSet):
 #   queryset = MovimientoInventario.objects.select_related('producto', 'tecnico')
  #  serializer_class = MovimientoInventarioSerializer
   # filter_backends = [DjangoFilterBackend]
    #filterset_fields = {
     #   'producto': ['exact'],
      #  'tecnico': ['exact'],
       # 'fecha': ['gte', 'lte', 'exact'],
        #'tipo_movimiento': ['exact']
    #}
    #ordering_fields = ['fecha']

def get_client_ip(request):
    """Obtiene la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Vista para listar y crear productos
class vistaproducto(APIView):
    def get(self, request):
        data = Producto.objects.order_by('-cod_material').all()
        serializer = ProductoSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("🔍 DEBUG: Iniciando POST")
        print(f"🔍 Usuario autenticado: {request.user.is_authenticated}")
        print(f"🔍 Usuario: {request.user}")
        
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            print("🔍 Serializer válido, guardando...")
            
            # ✅ DESACTIVAR SIGNALS TEMPORALMENTE
            from django.db.models.signals import post_save
            post_save.disconnect(receiver=None, sender=Producto)
            
            # Primer save SIN signal
            producto = serializer.save()
            print(f"🔍 Producto guardado con ID: {producto.id}")
            
            # Asignar usuario
            if request.user.is_authenticated:
                producto._usuario_auditoria = request.user
                print(f"🔍 Usuario asignado: {request.user}")
            else:
                usuario_default = User.objects.first()
                producto._usuario_auditoria = usuario_default
                print(f"🔍 Usuario por defecto asignado: {usuario_default}")
            
            producto._ip_auditoria = get_client_ip(request)
            print(f"🔍 IP asignada: {producto._ip_auditoria}")
            
            # ✅ REACTIVAR SIGNALS
            from producto.signals import registrar_auditoria_producto
            post_save.connect(registrar_auditoria_producto, sender=Producto)
            
            # Segundo save CON signal y usuario
            print("🔍 Guardando segunda vez...")
            producto.save()
            print("🔍 Segunda guardada completada")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(f"🔍 Errores del serializer: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para detalle, actualización y borrado de productos
class ProductoDetalle(APIView):
    
    def get_object(self, pk):
        try:
            return Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return None
    
    def get(self, request, pk):
        producto = self.get_object(pk)
        if producto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        producto = self.get_object(pk)
        if producto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # ✅ AGREGAR INFORMACIÓN DE AUDITORÍA ANTES DE GUARDAR
        if request.user.is_authenticated:
            producto._usuario_auditoria = request.user
        else:
            producto._usuario_auditoria = User.objects.first()
        
        producto._ip_auditoria = get_client_ip(request)
        
        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        producto = self.get_object(pk)
        if producto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # ✅ AGREGAR INFORMACIÓN DE AUDITORÍA ANTES DE GUARDAR
        if request.user.is_authenticated:
            producto._usuario_auditoria = request.user
        else:
            producto._usuario_auditoria = User.objects.first()
        
        producto._ip_auditoria = get_client_ip(request)
        
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        producto = self.get_object(pk)
        if producto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # ✅ AGREGAR INFORMACIÓN DE AUDITORÍA ANTES DE ELIMINAR
        if request.user.is_authenticated:
            producto._usuario_auditoria = request.user
        else:
            producto._usuario_auditoria = User.objects.first()
        
        producto._ip_auditoria = get_client_ip(request)
        
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ViewSets
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class TipoproductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tipoproducto.objects.all()
    serializer_class = TipoproductoSerializer

class AuditoriaProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditoriaProducto.objects.all().select_related('usuario')
    serializer_class = AuditoriaProductoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = {
        'accion': ['exact'],
        'producto_id': ['exact'],
        'usuario': ['exact'],
        'fecha_accion': ['gte', 'lte', 'exact'],
        'categoria': ['icontains'],
        'tipo_producto': ['icontains'],
    }
    
    search_fields = ['codigo_material', 'nombre_producto', 'descripcion', 'observaciones', 'usuario__username']
    ordering_fields = ['fecha_accion', 'accion', 'codigo_material']
    ordering = ['-fecha_accion']