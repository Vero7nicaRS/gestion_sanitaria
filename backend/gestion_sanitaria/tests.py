from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User as DjangoUser
from django.db.models.deletion import ProtectedError


from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from gestion_sanitaria.models import Animal, HistorialSanitario, ProductoSanitario


# ------------------------------------------------------------------------------------------------------
# Observaciones:
#  - Se va a utilizar los nombres de las rutas para hacer las peticiones en cada uno de los test.
#
# -------------------------------------------------------------------------------------------------------

class GestionSanitariaTestCase(APITestCase):

# Se definen los datos iniciales de los test
    def setUp(self):
        # Se crean...
        # --------------- Grupos: Administradores y Veterinarios ---------------
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.grupo_vet = Group.objects.create(name = "Veterinarios")

        # --------------- Usuarios ---------------------------------------------
        self.admin = User.objects.create_user(username="admin_test", password="admin1234")
        self.admin.groups.add(self.grupo_admin)

        self.vet = User.objects.create_user(username="veterinario_test", password="vet1234")
        self.vet.groups.add(self.grupo_vet)

        # --------------- Permisos ---------------------------------------------
        ct_animal = ContentType.objects.get_for_model(Animal)
        ct_producto = ContentType.objects.get_for_model(ProductoSanitario)
        ct_historial = ContentType.objects.get_for_model(HistorialSanitario)

        # Veterinarios: solo pueden visualizar los datos
        perms_vet = Permission.objects.filter(
            content_type__in=[ct_animal, ct_producto, ct_historial],
            codename__startswith="view_"
        )
        self.grupo_vet.permissions.set(perms_vet)

        # Administradores: pueden hacer CRUD completo (Crear, Leer, Modificar y Eliminar)
        perms_admin = Permission.objects.filter(
            content_type__in=[ct_animal, ct_producto, ct_historial],
        )
        self.grupo_admin.permissions.set(perms_admin)


        # --------------- Animales ---------------------------------------------
        self.animal_activo = Animal.objects.create(
            nombre="Max", 
            tipo_animal="Cobaya", 
            estado="ACTIVO"
        )
        self.animal_baja = Animal.objects.create(
            nombre="Kira", 
            tipo_animal="Gato", 
            estado="BAJA"
        )

        # --------------- Productos Sanitarios----------------------------------
        self.producto_sanitario_con_unidades = ProductoSanitario.objects.create(
            nombre="Vacuna prueba", 
            tipo="VACUNA", 
            unidades_disponibles=4
        )
        self.producto_sanitario_sin_unidades = ProductoSanitario.objects.create(
            nombre="Tratamiento prueba", 
            tipo="TRATAMIENTO", 
            unidades_disponibles=0
        )

        # --------------- Historial Sanitario----------------------------------
        self.historial_sanitario_01 = HistorialSanitario.objects.create(
            animal = self.animal_activo, 
            producto= self.producto_sanitario_con_unidades,
            fecha_suministro= "2026-01-14",
            observaciones= "Todo bien",
        )



# ------------------------------------------------------------------------------------#
#                                       LISTAR 
# ----------------------------------------------------------------------------------- #

    # Obtiene la lista de todos los animales siendo usuario veterinario.
    def test_get_lista_animales(self):
        self.client.force_authenticate(user=self.vet) # Usuario veterinario.
        url = reverse('animal_list_api')
        response = self.client.get(url) 
        self.assertEqual(response.status_code,200) # 200.
        self.assertTrue(len(response.data)>=2) # Hay 2 animales en el listado.

    # Obtiene la lista de todos los productos sanitarios siendo usuario veterinario.
    def test_get_lista_productos_sanitarios(self):
        self.client.force_authenticate(user=self.vet) # Usuario veterinario.
        url = reverse('producto_sanitario_list_api')
        response = self.client.get(url) 
        self.assertEqual(response.status_code,200) # 200.
        self.assertTrue(len(response.data)>=2) # Hay 2 productos en el listado.

    # Obtiene la lista de todos los historiales sanitarios siendo usuario administrador.
    def test_get_lista_historiales_sanitarios(self):
        self.client.force_authenticate(user=self.admin) # Usuario administrador.
        url = reverse('historial_sanitario_list_api')
        response = self.client.get(url) 
        self.assertEqual(response.status_code,200) # 200.
        self.assertTrue(len(response.data)>=1) # Hay 1 historial en el listado.

# ------------------------------------------------------------------------------------#
#                                       CREAR 
# ----------------------------------------------------------------------------------- #

###########################
#         ANIMAL          #
###########################

    # Crear a un animal siendo usuario administrador
    def test_post_animal_admin(self):
        self.client.force_authenticate(user=self.admin) # Usuario administrador.
        url = reverse('animal_create_api')
        data = {
            "nombre": "Coco",
            "tipo_animal": "Perro",
            "fecha_nacimiento": "2018-12-09",
            "estado": "ACTIVO"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201) # 201 

    # Crear a un animal siendo usuario veterinario
    # (NO puede crear al animal por no tener la autorización necesario).
    def test_post_animal_veterinario(self):
        self.client.force_authenticate(user=self.vet) # Usuario veterinario.
        url = reverse('animal_create_api')
        data = {
            "nombre": "Nala", 
            "tipo_animal": "Perro", 
            "estado": "ACTIVO"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403) # 403.

    # Crear un animal con nombre vacio siendo usuario administrador.
    # (NO puede crear al animal).
    def test_post_animal_nombre_vacio_admin(self):
        self.client.force_authenticate(user=self.admin) # Usuario administrador.
        url = reverse('animal_create_api')
        data = {
            "nombre": "   ", # Nombre vacío.
            "tipo_animal": "Agoporni",
            "estado": "ACTIVO"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400) # 400.
        self.assertIn("nombre", response.data) # Se devuelve un error asociado al campo "nombre"
            

###########################
#   PRODUCTO SANITARIO    #
###########################
    # Crear un producto sanitario siendo usuario administrador 
    def test_post_producto_sanitario_admin(self):
        self.client.force_authenticate(user=self.admin) # Usuario administrador.
        url = reverse('productos_sanitario_create_api')
        data = {
            "nombre": "Tratamiento prueba 01",
            "tipo": "TRATAMIENTO",
            "descripcion": "",
            "unidades_disponibles": 50, 
            "volver_a_suministrar_dias": None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201) # 201

    # Crear un producto sanitario con unidades negativas siendo usuario administrador.
    # (NO puede crear el producto sanitario porque debe introducirse unidades superiores a cero).
    def test_post_producto_sanitario_unidades_negativas_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('productos_sanitario_create_api')
        data = {
            "nombre": "Vacuna prueba 01",
            "tipo": "VACUNA",
            "descripcion": "",
            "unidades_disponibles": -4,  # Unidades negativas.
            "volver_a_suministrar_dias":""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400) # 400

    # Crear un producto sanitario siendo usuario veterinario.
    # (NO puede crear un producto sanitario porque no tiene la autorización necesaria).
    def test_post_producto_sanitario_veterinario(self):
        self.client.force_authenticate(user=self.vet) # Usuario veterinario.
        url = reverse('productos_sanitario_create_api')
        data = {
            "nombre": "Vacuna prueba 01",
            "tipo": "VACUNA",
            "unidades_disponibles": 28
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403) # 403.


    # Crear un producto sanitario siendo usuario veterinario.
    # (NO puede crear un producto sanitario).
    def test_post_producto_sanitario_nombre_vacio_admin(self):
        self.client.force_authenticate(user=self.admin) # Usuario administrador.
        url = reverse('productos_sanitario_create_api')
        data = {
            "nombre": "  ", # Nombre vacío.
            "tipo": "VACUNA", 
            "unidades_disponibles": 2
            }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400) # 400.
        self.assertIn("nombre", response.data) # Se devuelve un error asociado al campo "nombre".

# ------------------------------------------------------------------------------------#
#                                       ELIMINAR 
# ----------------------------------------------------------------------------------- #
    # Se realizan estos test para verificar las relaciones de los productos y animales
    # con el historial, ya que tienen la eliminación "PROTECTED".

    # No se puede eliminar a un animal que esté en un historial.
    def test_delete_no_se_puede_borrar_animal_con_historial(self):
        with self.assertRaises(ProtectedError):
            self.animal_activo.delete()

    # No se puede eliminar un producto que esté en un historial.
    def test_delete_no_se_puede_borrar_producto_con_historial(self):
        with self.assertRaises(ProtectedError):
            self.producto_sanitario_con_unidades.delete()


# ------------------------------------------------------------------------------------#
#                           SUMINISTRAR PRODUCTO 
#                       ----------------------------
# Cualquier usuario que esté autenticado puede suministrar un producto a un animal.
# Por tanto, se añadirá un nuevo historial al listado.
# ----------------------------------------------------------------------------------- #

    # Suministrar producto siendo un usuario administrador
    def test_suministrar_producto_autenticado(self):
        self.client.force_authenticate(user=self.admin) # Usuario administrador.

        url = reverse("suministrar_producto")
        data = {
            "animal_id": self.animal_activo.id,
            "producto_id": self.producto_sanitario_con_unidades.id,
            "fecha_suministro": "2026-02-02",
            "observaciones": "Sin incidencias"
        } # Datos que se van a utilizasr para realizar un suministro de un producto a un animal.

        # Se almacena el número de unidades para comprobar después si se ha restado una unidad.
        unidades_anteriores = self.producto_sanitario_con_unidades.unidades_disponibles
        
        historiales_anteriores = HistorialSanitario.objects.count()

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

        # Se comprueba el mensaje que se recibe.
        self.assertIn("message", response.data)
        self.assertIn("Se añade", response.data["message"])
        self.assertIn(self.producto_sanitario_con_unidades.nombre, response.data["message"])
        self.assertIn(self.animal_activo.nombre, response.data["message"])

        # Se comprueba que se ha creado un nuevo historial y que se ha restado una unidad.
        self.assertEqual(HistorialSanitario.objects.count(), historiales_anteriores + 1)

        self.producto_sanitario_con_unidades.refresh_from_db()
        # Tras añadir un nuevo historial al listado, se resta una unidad del producto sanitario que se ha empleado.
        self.assertEqual(self.producto_sanitario_con_unidades.unidades_disponibles, unidades_anteriores - 1)

    
    # Sumininistrar un producto sin autenticar.
    # (No puede suministrar un producto a un animal si no está autenticado).
    def test_suministrar_producto_no_autenticado(self):
        url = reverse("suministrar_producto")
        data = {
            "animal_id": self.animal_activo.id,
            "producto_id": self.producto_sanitario_con_unidades.id,
            "fecha_suministro": "2026-02-01",
            "observaciones": ""
        }

        response = self.client.post(url, data, format="json")
        self.assertIn(response.status_code, [401, 403])
        self.assertIn("detail", response.data)

    # Sumininistrar un producto a un animal con el estado "BAJA" siendo usuario administrador.
    # (No suministra porque el estado del animal es "BAJA").
    def test_suministrar_producto_animal_baja_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("suministrar_producto")
        data = {
            "animal_id": self.animal_baja.id,
            "producto_id": self.producto_sanitario_con_unidades.id,
            "fecha_suministro": "2026-02-03",
            "observaciones": ""
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.data) # Se devuelve un error asociado al campo "message"

    # Sumininistrar un producto sin unidades a un animal siendo usuario administrador.
    # (No suministra porque no tiene unidades suficientes).
    def test_suministrar_producto_sin_unidades_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("suministrar_producto")

        historiales_anteriores = HistorialSanitario.objects.count()

        data = {
            "animal_id": self.animal_activo.id,
            "producto_id": self.producto_sanitario_sin_unidades.id,
            "fecha_suministro": "2026-01-04",
            "observaciones": ""
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400) # 400
        self.assertEqual(HistorialSanitario.objects.count(), historiales_anteriores) # Se comprueba que haya el mismo número de historiales existentes.

    # Sumininistrar un producto a un animal que no existe siendo usuario administrador.
    # (No suministra porque no existe el animal en el sistema).
    def test_suministrar_producto_animal_inexistente_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("suministrar_producto")
        data = {
            "animal_id": 435345, # No existe el animal con este identificador.
            "producto_id": self.producto_sanitario_con_unidades.id, 
            "fecha_suministro": "2026-02-04"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 404)  # 404
    
    
    # Sumininistrar un producto que no existe a un animal siendo usuario administrador.
    # (No suministra porque no existe el producto sanitario en el sistema).
    def test_suministrar_producto_no_existe_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("suministrar_producto")
        data = {
            "animal_id": self.animal_activo.id, # No existe el animal con este identificador.
            "producto_id": 1234, 
            "fecha_suministro": "2026-02-04"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 404)

    
    # Suministrar un producto siendo un usuario administrador.
    # Se comprueba que se reciben todos los parámetros necesarios para
    # añadir un nuevo historial.
    def test_suministrar_producto_campos_obligatorios(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("suministrar_producto")
        data = {

        } # No se introduce ningún campo en el body.
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400) # 400
        self.assertIn("animal_id", response.data)  # Se devuelve un error asociado al campo "animal_id".
        self.assertIn("producto_id", response.data) # Se devuelve un error asociado al campo "producto_id".
        self.assertIn("fecha_suministro", response.data)  # Se devuelve un error asociado al campo "fecha_suministro".

    