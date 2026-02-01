# API SPOTIFY - DJANGO AVANZADO
# ----------------------------------------

----------
OBJETIVOS
----------
Desarrollar una API que permita gestionar una clínica veterinaria (animales, productos sanitarios e historial sanitario),
los cuales están almacenados en una base de datos.

Además, dependiendo del tipo de usuario, se podrán realizar determinadas acciones: 
 - Administrador: CRUD de todos los modelos.
 - Veterinario: Lectura de todos los modelos.

Este proyecto se ha implementando utilizando Django y la base de datos SQLite y MySQL.

-----------
INSTALACIÓN
-----------

1. Crear un entorno virtual (recomendado)

python -m venv venv


2. Activarlo

venv\Scripts\activate


3. Instalar dependencias

pip install -r requirements.txt

4. Migraciones

cd backend (Dirigirse a la carpeta backend)

python manage.py makemigrations

python manage.py migrate


5. Ejecutarlo

python manage.py runserver

-----------
ENDPOINTS
-----------

ANIMALES
---------
- POST /gestion_sanitaria/generics/animales/create/
Crea un animal en el sistema.
Los usuarios pertenecientes al grupo de Administradores pueden llevar a cabo esta acción.

    Body:
        { 
            “nombre”: "Jupiter",
            “tipo_animal”: "Agoporni",
            “fecha_nacimiento”: “2025-05-12”,
            “estado”: “ACTIVO”
        }


- GET /gestion_sanitaria/generics/animales/

Obtiene la lista de todos los animales existentes.
Los usuarios pertenecientes al grupo de Administradores y Veterinarios pueden acceder.


- GET /gestion_sanitaria/generics/animales/{id}/

Obtiene información detallada de un determinado animal.
Los usuarios pertenecientes al grupo de Administradores y Veterinarios pueden acceder.


- PUT /gestion_sanitaria/generics/animales/{id}

Modifica los datos de un animal existente.
Los usuarios pertenecientes al grupo de Administradores pueden llevar a cabo esta acción.
    

- DELETE /gestion_sanitaria/animales/{id}

Elimina a un determinado animal en el sistema.
Los usuarios pertenecientes al grupo de Administradores pueden llevar a cabo esta acción.


PRODUCTOS SANITARIOS
-------

- POST /gestion_sanitaria/generics/productos_sanitarios/create/

Crea un producto sanitario en el sistema.
Los usuarios pertenecientes al grupo de Administradores pueden llevar a cabo esta acción.

  Body:
        {
            "nombre": "Vacuna B",
            "tipo": "VACUNA",
            "descripcion": "Vacuna descripción",
            "unidades_disponibles": 5,
            "volver_a_suministrar_dias": None
        }


- GET /gestion_sanitaria/generics/productos_sanitarios/

Obtiene la lista de todos los productos sanitarios existentes.
Los usuarios pertenecientes al grupo de Administradores y Veterinarios pueden acceder.


- GET /gestion_sanitaria/generics/productos_sanitarios/{id}/

Obtiene información detallada de un determinado producto sanitario.
Los usuarios pertenecientes al grupo de Administradores y Veterinarios pueden acceder.

- PUT /gestion_sanitaria/generics/productos_sanitarios/{id}/update/

Modifica los datos de un producto sanitario existente.
Los usuarios pertenecientes al grupo de Administradores pueden llevar a cabo esta acción.

    Body:
        {
            "nombre": "Tratamiento C",
            "tipo": "TRATAMIENTO",
            "descripcion": "Mastitis",
            "unidades_disponibles": 29,
            "volver_a_suministrar_dias": 30
        }



HISTORIAL SANITARIO
-------

- POST /gestion_sanitaria/generics/historial_sanitario/create/

Crea un historial sanitario en el sistema.
Los usuarios pertenecientes al grupo de Administradores pueden llevar a cabo esta acción.
    Body:
        {
            "animal_id": 2,
            "producto_id": 2,
            "fecha_suministro": "2026-02-10",
            "observaciones": ""
        }
- GET /gestion_sanitaria/generics/historial_sanitario/

Obtiene la lista de todos los historiales sanitarios existentes.
Los usuarios pertenecientes al grupo de Administradores y Veterinarios pueden acceder.

- GET /gestion_sanitaria/generics/historial_sanitario/{id}/

Obtiene información detallada de un determinado historial sanitario existente.
Los usuarios pertenecientes al grupo de Administradores y Veterinarios pueden acceder.

- PUT /gestion_sanitaria/generics/historial_sanitario/{id}/update/

Modifica los datos de un historial sanitario existente.
Los usuarios pertenecientes al grupo de Administradores pueden llevar a cabo esta acción.
    Body:
        { 
            "animal_id": 2,
            "producto_id": 1,
            "fecha_suministro": "2026-02-04",
            "observaciones": "Todo ha ido correcto."
        }


SUMINISTRAR PRODUCTO
-------

- POST /gestion_sanitaria/suministrar_producto/

Suministra un producto sanitario a un determinado animal, añadiendose al listado de historiales sanitario.
El animal debe tener el estado "ACTIVO" y el producto tener unidades disponibles.
    
    Body:
        { 
            "animal_id": 2,
            "producto_id": 1,
            "fecha_suministro": "2026-02-04",
            "observaciones": "Todo ha ido correcto."
        }
