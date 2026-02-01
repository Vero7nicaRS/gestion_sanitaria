from rest_framework.routers import DefaultRouter

from gestion_sanitaria.views.generic_views import AnimalCreateAPIView, AnimalListAPIView, AnimalRetrieveAPIView, AnimalUpdateAPIView, HistorialSanitarioCreateAPIView, HistorialSanitarioListAPIView, HistorialSanitarioRetrieveAPIView, HistorialSanitarioUpdateAPIView, ProductoSanitarioCreateAPIView, ProductoSanitarioListAPIView, ProductoSanitarioRetrieveAPIView, ProductoSanitarioUpdateAPIView

from .views.views import AnimalViewSet, suministrar_producto
from django.urls import path, include


# ROUTER VIEWSET
router = DefaultRouter() 
router.register(r'animales', AnimalViewSet, basename='animal') # Registrar en el router los endpoints que queremos

#urlpatterns = router.urls

urlpatterns = [
    
    path('', include(router.urls)),

    # API_VIEW PROPIA
    path('suministrar_producto/', suministrar_producto, name='suministrar_producto'),

    # ANIMAL (genérica)
    path("generics/animales/", AnimalListAPIView.as_view(), name="animal_list_api"),
    path("generics/animales/create/", AnimalCreateAPIView.as_view(), name="animal_create_api"),
    path("generics/animales/<int:pk>/", AnimalRetrieveAPIView.as_view(), name="animal_retrieve_api"),
    path("generics/animales/<int:pk>/update/", AnimalUpdateAPIView.as_view(), name="animal_update_api"),

    # PRODUCTO SANITARIO (genérica)
    path("generics/productos_sanitarios/", ProductoSanitarioListAPIView.as_view(), name="producto_sanitario_list_api"),
    path("generics/productos_sanitarios/create/",  ProductoSanitarioCreateAPIView.as_view(), name="productos_sanitario_create_api"),
    path("generics/productos_sanitarios/<int:pk>/",  ProductoSanitarioRetrieveAPIView.as_view(), name="productos_sanitario_retrieve_api"),
    path("generics/productos_sanitarios/<int:pk>/update/", ProductoSanitarioUpdateAPIView.as_view(), name="productos_sanitario_update_api"),

    # HISTORIAL SANITARIO (genérica)
    path("generics/historial_sanitario/", HistorialSanitarioListAPIView.as_view(), name="historial_sanitario_list_api"),
    path("generics/historial_sanitario/create/", HistorialSanitarioCreateAPIView.as_view(), name="historial_sanitario_create_api"),
    path("generics/historial_sanitario/<int:pk>/", HistorialSanitarioRetrieveAPIView.as_view(), name="historial_sanitario_retrieve_api"),
    path("generics/historial_sanitario/<int:pk>/update/", HistorialSanitarioUpdateAPIView.as_view(), name="historial_sanitario_update_api"),

]