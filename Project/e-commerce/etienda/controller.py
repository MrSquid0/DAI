from . import Queries
from . import db_connection
from bson.objectid import ObjectId

client = db_connection.get_client()

# buscar desde el string id
# resu = client.tienda.productos.find_one({"_id": ObjectId(id)})

# Añadir "id" desde "_id"
# resu["id"] = str(resu.get('_id'))
# del resu["_id"]

def categories():
    return Queries.categories(client.tienda.productos)

def products():
    return list(client.tienda.productos.find())

def images_category(category):
    return Queries.get_category_image(client.tienda.productos, category)

def products_by_category(category):
    return list(client.tienda.productos.find({"categoría": category}))

def image_of_product(nombre):
    return Queries.image_of_product(client.tienda.productos, nombre)

def search_products(query):
    # Implementa la lógica para buscar productos según el término de búsqueda
    # Puedes utilizar consultas a la base de datos, índices de búsqueda, etc.
    products = client.tienda.productos.find({'nombre': {'$regex': query, '$options': 'i'}})
    return products

def get_maximum_product_id():
    return Queries.get_maximum_product_id(client.tienda.productos)


def get_tienda_db():
    return client.tienda.productos


def insert_product_to_db(product):
    client.insert_one(product.model_dump())