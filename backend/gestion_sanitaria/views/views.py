from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets
from ..models import Animal, ProductoSanitario, HistorialSanitario
from rest_framework.decorators import action
from ..serializer import AnimalSerializer, ProductoSanitarioSerializer, HistorialSanitarioSerializer, SuministrarProductoAnimalSerializer
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes



# ------------------------------------------------------------------------------------#
#           REQUISITOS
# - Objetivo 1: Implementar al menos 1 viewset.
# - Objetivo 2: Utilizar al menos 4 vistas genéricas distintos para cada modelo.
# - Objetivo 3: Al menos un api_view propia que enlace modelos (que no sean vistas genéricas).
# ----------------------------------------------------------------------------------- #

# Create your views here.
# No hace falta definir los permisos, ya que están definidos en settings.
# permission_classes = [IsAuthenticated, DjangoModelPermissions]

# ## OBJETIVO 1: Implementar al menos 1 viewset ## 
# VIEWSET 
class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all().order_by('nombre') #Obtener la informacion 
    serializer_class = AnimalSerializer 
    lookup_field = 'pk'




# ## OBJETIVO 2: Al menos un api_view propia que enlace modelos (que no sean vistas genéricas ## 
# Para suministrar una vacuna/tratamiento a un animal, se debe enviar en el body:
# - Identificador del animal (animal_id)
# - Identificador del producto (producto_id)
# - Fecha_suministro (fecha_suministro)
# {
#   "animal_id": 3,
#   "producto_id": 4,
#   "fecha_suministro": 12/03/2026,
#   "descripcion": "Tuvo reacción alérgica."
#}
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def suministrar_producto(request):


    serializer = SuministrarProductoAnimalSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    animal_id = serializer.validated_data["animal_id"]
    producto_id = serializer.validated_data["producto_id"]
    fecha_suministro = serializer.validated_data["fecha_suministro"]
    observaciones = serializer.validated_data.get("observaciones", "")



    # 1. Comprobar que el animal existe.
    try:
        animal = Animal.objects.get(pk=animal_id)
    except Animal.DoesNotExist:
        return Response(
                        {"message": f"Animal '{animal_id}' no encontrado"}, 
                            status=status.HTTP_404_NOT_FOUND
                        )

    # 2. Comprobar que el producto existe.
    try:
        producto_a_suministrar = ProductoSanitario.objects.get(pk=producto_id)
    except ProductoSanitario.DoesNotExist:
        return Response(
                        {"message": f"Producto '{producto_id}' no encontrado"}, 
                            status=status.HTTP_404_NOT_FOUND
                        )
    # 3. Comprobar el estado del animal: debe estar ACTIVO para suministrarle una vacuna o tratamiento.
    if animal.estado != "ACTIVO":
        return Response(
            {"message": "El animal debe estar en estado ACTIVO para suministrar un producto."},
            status=status.HTTP_400_BAD_REQUEST
        )
    # 4. Comprobar que hay unidades suficientes para suministrar.
    if producto_a_suministrar.unidades_disponibles > 0:
        
        # Añadir ese producto suministrado (vacuna o tratamiento) al historial del animal.
        nuevo_historial = HistorialSanitario.objects.create(
            animal = animal,
            producto = producto_a_suministrar,
            fecha_suministro = fecha_suministro,
            observaciones = observaciones
        )  # Añade el suministro al historial del animal.
        
        # Decrementar el número de unidades, ya que se ha utilizado una unidad para suministrársela al animal.
        producto_a_suministrar.unidades_disponibles = producto_a_suministrar.unidades_disponibles - 1
        producto_a_suministrar.save(update_fields=["unidades_disponibles"]) # Se actualiza en la base de datos.

        return Response(
            {
                "message": f"Se añade '{producto_a_suministrar.nombre}' (id: {producto_id}) al animal '{animal.nombre}' (id: {animal_id})",
            },
            status= status.HTTP_201_CREATED
        )

    else:
            return Response(
                            {
                                "message": (
                                f"No hay unidades disponibles del producto '{producto_a_suministrar.nombre}'. "
                                f"Unidades disponibles: {producto_a_suministrar.unidades_disponibles}."
                                )
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

 