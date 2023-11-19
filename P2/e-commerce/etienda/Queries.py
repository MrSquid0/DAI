def query1(productos_collection):
    print("===================================================")
    print("Electrónica entre 100 y 200€, ordenados por precio")
    print("===================================================")

    # Realiza la consulta en la base de datos MongoDB
    electronicos = productos_collection.find({
        "categoría": "electronics",
        "precio": {"$gt": 100, "$lt": 200}
    })

    return electronicos


def query2(productos_collection):
    print("===============================================================")
    print("Productos que contengan la palabra 'pocket' en la descripción")
    print("===============================================================")

    # Realiza la consulta en MongoDB para encontrar productos con 'pocket' en la descripción
    productos_con_pocket = productos_collection.find({
        'descripción': {'$regex': 'pocket', '$options': 'i'}
    })

    return productos_con_pocket


def query3(productos_collection):
    print("===================================================")
    print("Productos con puntuación mayor de 4")
    print("===================================================")

    # Realiza la consulta en MongoDB para encontrar productos con 'rate' mayor de 4
    productos_con_rate_mayor_de_4 = productos_collection.find({
        'rating.puntuación': {'$gt': 4}
    })

    return productos_con_rate_mayor_de_4


def query4(productos_collection):
    print("===================================================")
    print("Ropa de hombre, ordenada por puntuación")
    print("===================================================")

    # Realiza la consulta en MongoDB para encontrar productos de la categoría 'men's clothing' y ordenar por 'rate'
    productos_ropa_hombre = productos_collection.find({
        'categoría': "men's clothing"
    }).sort('rating.puntuación', 1)

    return productos_ropa_hombre


def query5(productos_collection, compras_collection):
    print("===================================================")
    print("Facturación total")
    print("===================================================")

    facturacion = 0 # Inicializamos la facturación a 0

    for compra in compras_collection.find():
        for producto in compra["productos"]:

            cantidad = producto["quantity"]

            # Localizamos el producto que estamos buscando con el ID
            p = productos_collection.find_one({"producto_id": producto["productId"]})

            precio = p["precio"]

            facturacion += precio * cantidad

    return round(facturacion, 2)


def query6(productos_collection, compras_collection):
    print("===================================================")
    print("Facturación por categoría de producto")
    print("===================================================")

    facturacion_cada_categoria = {}

    for compra in compras_collection.find():
        for producto in compra["productos"]:

            cantidad = producto["quantity"]

            # Localizamos el producto que estamos buscando con el ID
            p = productos_collection.find_one({"producto_id": producto["productId"]})

            # Guardamos el precio
            precio = p["precio"]

            # Guardamos la categoría
            categoria = p["categoría"]

            # Si la categoría no está, le añadimos un 0 para no sumar esa categoría
            if categoria not in facturacion_cada_categoria:
                facturacion_cada_categoria[categoria] = 0

            facturacion_cada_categoria[categoria] += precio * cantidad


    return facturacion_cada_categoria


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