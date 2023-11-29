import pymongo


def categories(productos_collection):
    categorias_unicas = productos_collection.distinct('categoría')

    return categorias_unicas


def get_category_image(productos_collection, category):
    resultado = productos_collection.aggregate([
        {"$match": {"categoría": category}},
        {"$sample": {"size": 1}},
        {"$project": {"_id": 0, "imágen": 1}}
    ])

    producto_aleatorio = next(resultado, None)

    return producto_aleatorio["imágen"] if producto_aleatorio else None


def image_of_product(productos_collection, nombre):
    product = productos_collection.find_one({'nombre': nombre})

    return product.get('imágen')


def get_maximum_product_id(productos_collection):
    max_product_id = productos_collection.find_one(
        {},
        sort=[("producto_id", pymongo.DESCENDING)],
    )["producto_id"]

    return max_product_id