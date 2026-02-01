from rest_framework import generics

from gestion_sanitaria.models import Animal, HistorialSanitario, ProductoSanitario
from gestion_sanitaria.serializer import AnimalSerializer, HistorialSanitarioSerializer, ProductoSanitarioSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions



# ------------------------------------------------------------------------------------#
#           REQUISITOS
# - Objetivo 1: Implementar al menos 1 viewset.
# - Objetivo 2: Utilizar al menos 4 vistas genéricas distintos para cada modelo.
# - Objetivo 3: Al menos un api_view propia que enlace modelos (que no sean vistas genéricas).
# ----------------------------------------------------------------------------------- #


# ## OBJETIVO 2: Utilizar al menos 4 vistas genéricas distintos para cada modelo ## 
# ======== #
# Generic  #  
# ======== # 

# Aquí con que partes del CRUD necesito implementar.
# Nos encapsulan parte de la lógica pero nos dan más flexibilidad a la hroa de implementar los distintos métodos.
# Da funcionalidades concretas y agrupadas.
# Da más flexibilidad que los viewset, pero sin ser de bajo nivel como las apiviews.
# En definitiva, es un punto intermedio que ofrece una mayor flexibilidad.

# OBSERVACIÓN:
# NO hace falta poner: "permission_classes = [IsAuthenticated, DjangoModelPermissions]"
# en cada una de las vistas porque está incluido en "DEFAULT_PERMISSION_CLASSES: 'rest_framework.permissions.DjangoModelPermissions'"


# ##############################################################################################
#                                      ANIMAL
# ##############################################################################################
class AnimalListAPIView(generics.ListAPIView):  # GET de todos los objetos.
    queryset=Animal.objects.all() #Traigo la información y traigo el serialicer.
    serializer_class = AnimalSerializer
#   permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
class AnimalCreateAPIView(generics.CreateAPIView): # POST
    queryset=Animal.objects.all()
    serializer_class = AnimalSerializer

class AnimalUpdateAPIView(generics.UpdateAPIView): # PUT
    queryset=Animal.objects.all()
    serializer_class = AnimalSerializer

class AnimalRetrieveAPIView(generics.RetrieveAPIView): # Get de un único objeto 
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


# ##############################################################################################
#                                      PRODUCTOSANITARIO
# ##############################################################################################
class ProductoSanitarioListAPIView(generics.ListAPIView):  # GET de todos los objetos.
    queryset=ProductoSanitario.objects.all() #Traigo la información y traigo el serialicer.
    serializer_class = ProductoSanitarioSerializer

class ProductoSanitarioCreateAPIView(generics.CreateAPIView): # POST
    queryset=ProductoSanitario.objects.all()
    serializer_class = ProductoSanitarioSerializer

class ProductoSanitarioUpdateAPIView(generics.UpdateAPIView): # PUT
    queryset=ProductoSanitario.objects.all()
    serializer_class = ProductoSanitarioSerializer

class ProductoSanitarioRetrieveAPIView(generics.RetrieveAPIView): # Get de un único objeto 
    queryset = ProductoSanitario.objects.all()
    serializer_class = ProductoSanitarioSerializer


# ##############################################################################################
#                                      HISTORIALSANITARIO
# ##############################################################################################
class HistorialSanitarioListAPIView(generics.ListAPIView):  # GET de todos los objetos.
    queryset=HistorialSanitario.objects.all() #Traigo la información y traigo el serialicer.
    serializer_class = HistorialSanitarioSerializer

class HistorialSanitarioCreateAPIView(generics.CreateAPIView): # POST
    queryset=HistorialSanitario.objects.all()
    serializer_class = HistorialSanitarioSerializer

class HistorialSanitarioUpdateAPIView(generics.UpdateAPIView): # PUT
    queryset=HistorialSanitario.objects.all()
    serializer_class = HistorialSanitarioSerializer

class HistorialSanitarioRetrieveAPIView(generics.RetrieveAPIView): # Get de un único objeto 
    queryset = HistorialSanitario.objects.all()
    serializer_class = HistorialSanitarioSerializer
