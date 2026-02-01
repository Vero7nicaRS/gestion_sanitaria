from django.db import models

# Create your models here.


class ModeloFecha(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Animales.
class Animal(ModeloFecha):

    class Estado(models.TextChoices):
        ACTIVO = "ACTIVO", "Activo"
        BAJA = "BAJA", "Baja"

    nombre = models.CharField(max_length=255)
    tipo_animal = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField(null=True, blank = True)
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ACTIVO
    )

    def __str__(self): # Printar los animales
        return f"{self.nombre} - {self.tipo_animal}"
    
    class Meta: # Crear una subclase para permitir añadir más información.
        # Podemos añadir subcomportamientos 
        # Cuando me devuelva la información el modelo, los últimos nombres añadidos, aparezcan al principio
        ordering = ['nombre']



# PRODUCTO SANITARIO: VACUNA O TRATAMIENTO
class ProductoSanitario(ModeloFecha):
    class Tipo(models.TextChoices):
        VACUNA = "VACUNA", "Vacuna"
        TRATAMIENTO = "TRATAMIENTO", "Tratamiento"

    nombre = models.CharField(max_length=255, unique=True)
    tipo = models.CharField(max_length=15, choices=Tipo.choices)
    descripcion = models.TextField(blank=True)
    unidades_disponibles = models.PositiveIntegerField(default=0)
    volver_a_suministrar_dias = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self): # Printar los tratamientos y/o vacunas
        return f"{self.nombre} [{self.tipo}]"
    

# HISTORIAL DEL ANIMAL
class HistorialSanitario(ModeloFecha):

    animal = models.ForeignKey(
        Animal,
        on_delete=models.PROTECT,
        related_name="historial_animal"   # Nombre de la Relacion: Animal --> HistorialSanitario
    )
    producto = models.ForeignKey(
        ProductoSanitario,
        on_delete=models.PROTECT,
        related_name="historial_suministros"   # Nombre de la Relación: ProductoSanitario --> HistorialSanitario
    )

    fecha_suministro = models.DateField()
    observaciones = models.TextField(blank=True)
    
   
    def __str__(self): # Printar el historial médico del animal
        return f"{self.animal} - {self.producto} ({self.fecha_suministro})"

    class Meta: # Crear una subclase para permitir añadir más información.
        # Podemos añadir subcomportamientos 
        # Cuando me devuelva la información el modelo, las últimas fechas añadidas, aparezcan al principio
        unique_together = ("animal", "producto", "fecha_suministro")
        ordering = ['-fecha_suministro']

        
#Serializers obtener información más sencilla del modelo.
