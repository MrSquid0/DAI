# Seed.py
from pydantic import BaseModel, Field, EmailStr, field_serializer
from pathlib import Path
import pathlib
from pymongo import MongoClient
from datetime import datetime
from typing import Any
import requests
import Queries
import os

# Para hacer una copia de seguridad, habría que ejecutar el siguiente comando:
# mongodump --host localhost --port 27017 --db tienda

# https://requests.readthedocs.io/en/latest/

def getElementos(api):
    response = requests.get(api)
    return response.json()


# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/
class Nota(BaseModel):
    puntuación: float = Field(ge=0., lt=5.)
    cuenta: int = Field(ge=1)


class Producto(BaseModel):
    _id: Any
    producto_id: int
    nombre: str
    precio: float
    descripción: str
    categoría: str
    imágen: str | None
    rating: Nota

    @field_serializer('imágen')
    def serializaPath(self, val) -> str:
        if type(val) is pathlib.PosixPath:
            return str(val)
        return val


class Compra(BaseModel):
    _id: Any
    usuario: EmailStr
    fecha: datetime
    productos: list


# Conexión con la BD
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('localhost', 27017)

tienda_db = client.tienda  # Base de Datos

# Obtenemos los productos de la API https://fakestoreapi.com/products
productos_collection = tienda_db.productos  # Colección de productos
productos = getElementos('https://fakestoreapi.com/products')
productos_collection.drop()  # Borramos toda la colección de productos para no duplicar elementos

# Obtenemos las compras de la API https://fakestoreapi.com/carts
compras_collection = tienda_db.compras  # Colección de compras
compras = getElementos('https://fakestoreapi.com/carts')

# Obtenemos los usuarios de la API https://fakestoreapi.com/users
usuarios = getElementos('https://fakestoreapi.com/users')

compras_collection.drop()  # Borramos toda la colección de compras para no duplicar elementos


# Elimina todas las imágenes antes de empezar a descargarlas
ruta_absoluta = os.path.abspath("e-commerce/imágenes")
for filename in os.listdir(ruta_absoluta):
    ruta_completa = os.path.join(ruta_absoluta, filename)

    # Verifica si el elemento en la ruta es un archivo
    if os.path.isfile(ruta_completa):
        # Elimina el archivo
        os.remove(ruta_completa)

# Insertamos los productos y las compras en la base de datos MongoDB
# y descargamos las imágenes de cada producto en el directorio

for producto in productos:
    url = producto.get("image")
    nombre_imagen_unico = pathlib.Path(url).name
    path = os.path.join(ruta_absoluta, nombre_imagen_unico)

    # Realizamos una solicitud HTTP GET a la URL especificada
    solicitud = requests.get(url)
    # Abrimos el archivo en modo binario en la ubicación especificada y
    # escribimos el contenido de la respuesta de la solicitud en el archivo
    with open(path, "wb") as archivo:
        archivo.write(solicitud.content)

    # Insertamos los elementos de cada columna
    nuevo_producto = {
        'producto_id': producto["id"],
        'nombre': producto["title"],
        'precio': producto["price"],
        'descripción': producto["description"],
        'categoría': producto["category"],
        'imágen': str(Path("e-commerce/imágenes/" + nombre_imagen_unico)),
        'rating': {'puntuación': producto["rating"]["rate"],
                   'cuenta': producto["rating"]["count"]}
    }

    # Creamos el objeto de la clase Producto
    producto = Producto(**nuevo_producto)

    # Comprobamos si la primera letra del nombre es mayúscula
    if producto.nombre[0].isupper():
        productos_collection.insert_one(producto.model_dump())
    else:
        print(f"La primera letra del nombre del producto "
              f"{producto['id']} no es mayúscula.\n")

# Hay más usuarios que compras, por lo que vamos asignando las compras
# que haya a los usuarios por orden a través de un índice
indice = 0
for compr in compras:
    # Insertamos los elementos de cada columna
    nueva_compra = {
        'usuario': usuarios[indice]["email"],
        'fecha': datetime.now(),
        'productos': compr["products"],
    }

    # Creamos el objeto de la clase Compra
    compra = Compra(**nueva_compra)
    compras_collection.insert_one(compra.model_dump())

    # Incrementamos el índice para la siguiente inserción
    indice += 1

# Consulta 1
query1 = Queries.query1(productos_collection)
for producto in query1:
    print(f"{str(producto)}+\n")
print("\n\n")

# Consulta 2
query2 = Queries.query2(productos_collection)
for producto in query2:
    print(f"{str(producto)}+\n")
print("\n\n")

# Consulta 3
query3 = Queries.query3(productos_collection)
for producto in query3:
    print(f"{str(producto)}+\n")
print("\n\n")

# Consulta 4
query4 = Queries.query4(productos_collection)
for producto in query4:
    print(f"{str(producto)}+\n")
print("\n\n")

# Consulta 5
query5 = Queries.query5(productos_collection, compras_collection)
print(f"La facturación total es {query5}.")
print("\n\n")

# Consulta 6
query6 = Queries.query6(productos_collection, compras_collection)
for categoria, facturacion_categoria in query6.items():
    print(f"\nCategoría: {categoria} --> {facturacion_categoria:.2f}\n")
