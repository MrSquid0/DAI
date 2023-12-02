from . import Queries
from . import db_connection
from bson.objectid import ObjectId

client = db_connection.get_client()
products_collection = client.tienda.productos

# buscar desde el string id
# resu = products.find_one({"_id": ObjectId(id)})

# Añadir "id" desde "_id"
# resu["id"] = str(resu.get('_id'))
# del resu["_id"]


def categories():
    return Queries.categories(products_collection)


def products():
    return list(products_collection.find())


def images_category(category):
    return Queries.get_category_image(products_collection, category)

def products_by_category(category):
    return list(products_collection.find({"categoría": category}))


def image_of_product(nombre):
    return Queries.image_of_product(products_collection, nombre)


def search_products(query):
    # Implementa la lógica para buscar productos según el término de búsqueda
    # Puedes utilizar consultas a la base de datos, índices de búsqueda, etc.
    products_search = products_collection.find({'nombre': {'$regex': query, '$options': 'i'}})
    return products_search


def get_maximum_product_id():
    return Queries.get_maximum_product_id(products_collection)


def get_tienda_db():
    return products_collection


def insert_product_to_db(product):
    products_collection.insert_one(product.dict())