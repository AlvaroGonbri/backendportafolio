from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse 
from .models import Producto
from .serializers import *

# Create your views here.

class vistaproducto(APIView):

    def get(self, request):
        data = Producto.objects.order_by('-cod_material').all()
        datos_json = ProductoSerializer(data, many=True)
        return Response(datos_json.data)

