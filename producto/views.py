from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Producto, Categoria, Tipoproducto
from .serializers import ProductoSerializer, CategoriaSerializer, TipoproductoSerializer
from rest_framework import status, viewsets, generics



# Create your views here.

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


