from rest_framework import serializers
from .models import Animal, ProductoSanitario, HistorialSanitario
from datetime import date

#                                   VALIDACIONES
# SERIALIZER: Se encarga de validar que los datos que se pasado por el JSON (body) ---> Postman
#             sean los correctos. Para que así, VIEW solamente tenga que implementar la funcionalidad
#             y no hacer comprobaciones.
#             Por tanto, el serializer se encarga de comprobar los datos de entrada (JSON - BODY)
# validate_<NOMBRE_DEL_CAMPO_A_VALIDAR>
# 
# Serializer: permite definir que información de nuestro modelo vamos a mover hacia delante o hacia atrás
# cuando el usuario interactue con nosotros. Y que limitaciones estamos imponiendo y validaciones adicionales.
# Después del serializer, hay que dirigirse a la vista.



# UsuarioSerializer: comprueba UN usuario
#   { 
#     "id": 34,
#     "nombre": "Pepe" 
#   }  
# 

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal  # Modelo
        fields = ["id", "nombre", "tipo_animal", "fecha_nacimiento", "estado", "created_at", "updated_at"] # A la hora de hacer peticiones, esta información es la que se va a mostrar.
        read_only_fields = ['id', 'created_at', 'updated_at'] # El usuario no puede modificarlas.

    def validate_nombre(self, value): # Se asegura que el campo "nombre" tenga valor
        if(not value or not value.strip()):
            raise serializers.ValidationError("El campo 'nombre' es obligatorio.")
        return value 
    
    def validate_tipo_animal(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El campo 'tipo_animal' es obligatorio.")
        return value.strip()

class ProductoSanitarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoSanitario # Modelo
        fields = ["id", "nombre", "tipo", "descripcion", "unidades_disponibles", "volver_a_suministrar_dias", "created_at", "updated_at"] # A la hora de hacer peticiones, esta información es la que se va a mostrar.
        read_only_fields = ['id', 'created_at', 'updated_at'] # El usuario no puede modificarlas.

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El campo 'nombre' es obligatorio.")
        return value.strip()

    def validate_unidades_disponibles(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Las unidades_disponibles no puede ser negativas.")
        return value

class HistorialSanitarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialSanitario # Modelo
        fields = [
            "id",
            "animal",
            "producto", 
            "fecha_suministro",
            "observaciones",
            "created_at",
            "updated_at",
        ]

class SuministrarProductoAnimalSerializer(serializers.Serializer):
    animal_id = serializers.IntegerField()
    producto_id = serializers.IntegerField()
    fecha_suministro = serializers.DateField() 
    observaciones = serializers.CharField(required = False, allow_blank =True)


    # También, permite en el SERIALIZER checkear que los campos sean los correctos.
    def validate_animal_id(self, value): # Se asegura que el campo "animal_id" tenga valor
        if(not value):
            raise serializers.ValidationError("El campo 'animal_id' es obligatorio.")
        return value 
    
    def validate_producto_id(self, value): # Se asegura que el campo "producto_id" tenga valor
        if(not value):
            raise serializers.ValidationError("El campo 'producto_id' es obligatorio.")
        return value 