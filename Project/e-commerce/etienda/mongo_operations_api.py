import os

from django.conf import settings

from . import db_connection
from . import Queries
import logging
import re

logger = logging.getLogger(__name__)

client = db_connection.get_client()
products_collection = client.tienda.productos


def list_products(start: int, end: int):
    products = list(products_collection.find().skip(start).limit(end - start))
    products_converted = []

    for product in products:
        product_dict = {
            "id": str(product.get('producto_id')),
            "title": product.get("nombre", ""),
            "price": product.get("precio", 0.0),
            "description": product.get("descripción", ""),
            "category": product.get("categoría", ""),
            "image": product.get("imágen", ""),
            "rating": {
                "rate": product["rating"]["puntuación"],
                "count": product["rating"]["cuenta"],
            }
        }

        # Verifies if '_id' exists before deleting it
        if '_id' in product_dict:
            del product_dict["_id"]

        products_converted.append(product_dict)

    return products_converted


def get_product(producto_id: str):
    product = products_collection.find_one({"producto_id": int(producto_id)})

    if product:
        product_dict = {
            "id": str(product.get('producto_id')),
            "title": product.get("nombre", ""),
            "price": product.get("precio", 0.0),
            "description": product.get("descripción", ""),
            "category": product.get("categoría", ""),
            "image": product.get("imágen", ""),
            "rating": {
                "rate": product["rating"]["puntuación"],
                "count": product["rating"]["cuenta"],
            }
        }

        return product_dict
    else:
        raise Exception("Product not found")


def create_product(payload):
    # Makes the insertion to the DB
    product_id = Queries.get_maximum_product_id(products_collection) + 1

    products_collection.insert_one({
        "producto_id": product_id,
        "nombre": payload.title,
        "precio": payload.price,
        "descripción": payload.description,
        "categoría": payload.category,
        "rating": {'puntuación': payload.rating.rate, 'cuenta': payload.rating.count}
    })

    # Retorna el producto recién creado
    return get_product(product_id)


def modify_product(product_id: str, payload):
    existing_product = products_collection.find_one({"producto_id": int(product_id)})

    if existing_product:
        # Makes the update to the DB
        products_collection.update_one(
            {"producto_id": int(product_id)},
            {"$set":
                {
                    "nombre": payload.title,
                    "precio": payload.price,
                    "descripción": payload.description,
                    "categoría": payload.category,
                    "rating": {'puntuación': payload.rating.rate, 'cuenta': payload.rating.count}
                }})

        return get_product(product_id)

    else:
        # If product not found, launches an exception
        raise Exception("Product not found")


def delete_product(product_id: str):
    # Get the product before deleting it
    product = products_collection.find_one({"producto_id": int(product_id)})

    if product:
        # Get the image path
        image_path = product.get("imágen", "")
        # Delete the product from the database
        result = products_collection.delete_one({"producto_id": int(product_id)})
        if result.deleted_count == 0:
            raise Exception("Product not found")
        # Delete the image file
        if image_path:
            absolute_image_path = os.path.join(settings.BASE_DIR, image_path)
            if os.path.exists(absolute_image_path):
                os.remove(absolute_image_path)
    else:
        raise Exception("Product not found")


def modify_rating(product_id, rate):
    existing_product = products_collection.find_one({"producto_id": int(product_id)})

    if existing_product:
        current_rating = existing_product["rating"]["puntuación"]
        current_count = existing_product["rating"]["cuenta"]

        # Calculate the new average rating
        new_rating = (current_rating * current_count + rate) / (current_count + 1)

        # Truncate the new rating to 3 decimal places
        new_rating = round(new_rating, 3)

        # Makes the update to the DB
        products_collection.update_one(
            {"producto_id": int(product_id)},
            {"$set":
                {
                    "rating": {'puntuación': new_rating, 'cuenta': current_count + 1}
                }})

        return get_product(product_id)

    else:
        # If product not found, launches an exception
        raise Exception("Product not found.")


def coincidences_by_name_or_description(search_query):
    # Crear un patrón de regex insensible a mayúsculas
    pattern = f".*{search_query}.*"
    regex = {"$regex": pattern, "$options": "i"}

    # Buscar en los campos 'nombre' y 'descripción'
    products = products_collection.find({"$or": [{"nombre": regex}, {"descripción": regex}]})
    lista_de_productos = []

    for product in products:
        rating = product.get("rating", {})

        product_dict = {
            "id": str(product.get('producto_id')),
            "title": product.get("nombre", ""),
            "price": product.get("precio", 0.0),
            "description": product.get("descripción", ""),
            "category": product.get("categoría", ""),
            "image": product.get("imágen", ""),  # Corregir el nombre del campo
            "rating": {
                "rate": rating.get("puntuación", 0),  # Manejar casos donde 'puntuación' puede faltar
                "count": rating.get("cuenta", 0),  # Manejar casos donde 'cuenta' puede faltar
            }
        }

        lista_de_productos.append(product_dict)

    return lista_de_productos


def get_products_by_category(category: str):
    products = products_collection.find({"categoría": category})
    products_converted = []

    for product in products:
        product_dict = {
            "id": str(product.get('producto_id')),
            "title": product.get("nombre", ""),
            "price": product.get("precio", 0.0),
            "description": product.get("descripción", ""),
            "category": product.get("categoría", ""),
            "image": product.get("imágen", ""),
            "rating": {
                "rate": product["rating"]["puntuación"],
                "count": product["rating"]["cuenta"],
            }
        }

        if '_id' in product_dict:
            del product_dict["_id"]

        products_converted.append(product_dict)

    return products_converted


def get_categories():
    categories_cursor = products_collection.distinct('categoría')
    categories_list = [category for category in categories_cursor]
    return categories_list
