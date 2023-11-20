from . import Queries
from . import db_connection

client = db_connection.get_client()
def run_query_one():
    return list(Queries.query1(client.tienda.productos))

def run_query_two():
    return list(Queries.query2(client.tienda.productos))

def run_query_three():
    return list(Queries.query3(client.tienda.productos))

def run_query_four():
    return list(Queries.query4(client.tienda.productos))

def run_query_five():
    return Queries.query5(client.tienda.productos, client.tienda.compras)

def run_query_six():
    return Queries.query6(client.tienda.productos, client.tienda.compras)

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