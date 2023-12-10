from . import db_connection
from . import Queries

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


def search_product(producto_id: str):
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
    return search_product(product_id)


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

        return search_product(product_id)

    else:
        # If product not found, launches an exception
        raise Exception("Product not found")


def delete_product(product_id: str):
    result = products_collection.delete_one({"producto_id": int(product_id)})
    if result.deleted_count == 0:
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

        return search_product(product_id)

    else:
        # If product not found, launches an exception
        raise Exception("Product not found.")
