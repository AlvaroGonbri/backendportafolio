from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AsignacionViewSet, CategoriaViewSet, MovimientoViewSet, TecnicoViewSet, TipoproductoViewSet, vistaproducto, ProductoDetalle

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'tipos', TipoproductoViewSet)
router.register(r'tecnicos', TecnicoViewSet, basename='tecnicos')
router.register(r'asignaciones', AsignacionViewSet, basename='asignaciones')
router.register(r'movimientos', MovimientoViewSet, basename='movimientos')

urlpatterns = [
    path('', include(router.urls)),
    path('productos/', vistaproducto.as_view()),          # GET (listar), POST (crear)
    path('productos/<int:pk>/', ProductoDetalle.as_view()),  # GET (detalle), PUT (actualizar), PATCH (actualización parcial), DELETE


]
