from django.urls import path, include
from producto.views import *

urlpatterns = [
    path('listar/', vistaproducto.as_view())
]


