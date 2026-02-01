from django.contrib import admin

from gestion_sanitaria.models import Animal, HistorialSanitario, ProductoSanitario

# Para gestionar los datos de los Animales, Productos Sanitarios e Historial Sanitario
# desde la interfaz de Django.

# Register your models here.
admin.site.register(Animal)
admin.site.register(ProductoSanitario)
admin.site.register(HistorialSanitario)

