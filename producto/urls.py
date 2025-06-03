from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, TipoproductoViewSet, vistaproducto, ProductoDetalle

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'tipos', TipoproductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('productos/', vistaproducto.as_view()),          # GET (listar), POST (crear)
    path('productos/<int:pk>/', ProductoDetalle.as_view()),  # GET (detalle), PUT (actualizar), PATCH (actualización parcial), DELETE
]
