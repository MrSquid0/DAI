import sys

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from . import controller


def index_2_1(request):
    res = ("<html>"
           "<h1>Lista de consultas</h1>"
           "<ul>"
           "    <li><a href='electronica'>Electrónica entre 100 y 200€, ordenados por precio</a></li>"
           "    <li><a href='pocket'>Productos que contengan la palabra 'pocket' en la descripción</a></li>"
           "    <li><a href='productos-puntuacion'>Productos con puntuación mayor de 4</a></li>"
           "    <li><a href='hombre-puntuacion'>Ropa de hombre, ordenada por puntuación</a></li>"
           "    <li><a href='facturacion-total'>Facturación total</a></li>"
           "    <li><a href='facturacion-categoria'>Facturación por categoría de producto</a></li>"
           "</ul>"
           "</html>")
    return HttpResponse(res)

def query_one(request):
    productos = controller.run_query_one()
    res = ("<html>"
           "<a href='../etienda/2-1'>Volver a la lista de consultas</a>"
           "<h1>Electrónica entre 100 y 200€, ordenados por precio</h1> <ul> "
           "</html>")
    for producto in productos:
        res += (f"\n<html><li></html>{producto['nombre']} <html> "
                f" <br> <b>===> Precio:</b> </html>{producto['precio']}<html></li><br></html>")
    res += "\n\n<html></ul></html>"
    return HttpResponse(res)

def query_two(request):
    productos = controller.run_query_two()
    res = ("<html>"
           "<a href='../etienda/2-1'>Volver a la lista de consultas</a>"
           "<h1>Productos que contengan la palabra 'pocket' en la descripción</h1> <ul> "
           "</html>")
    for producto in productos:
        res += (f"\n<html><li></html>{producto['nombre']} <html> "
                f" <br> <b>===> Descripción:</b> </html>{producto['descripción']}<html></li><br></html>")
    res += "\n\n<html></ul></html>"
    return HttpResponse(res)

def query_three(request):
    productos = controller.run_query_three()
    res = ("<html>"
           "<a href='../etienda/2-1'>Volver a la lista de consultas</a>"
           "<h1>Productos con puntuación mayor de 4</h1> <ul> "
           "</html>")
    for producto in productos:
        res += (f"\n<html><li></html>{producto['nombre']} <html> "
                f" <br> <b>===> Puntuación:</b> </html>{producto['rating']['puntuación']}<html></li><br></html>")
    res += "\n\n<html></ul></html>"
    return HttpResponse(res)

def query_four(request):
    productos = controller.run_query_four()
    res = ("<html>"
           "<a href='../etienda/2-1'>Volver a la lista de consultas</a>"
           "<h1>Ropa de hombre, ordenada por puntuación</h1> <ul> "
           "</html>")
    for producto in productos:
        res += (f"\n<html><li></html>{producto['nombre']} <html> "
                f" <br> <b>===> Puntuación:</b> </html>{producto['rating']['puntuación']}<html></li><br></html>")
    res += "\n\n<html></ul></html>"
    return HttpResponse(res)

def query_five(request):
    facturacion_total = controller.run_query_five()
    res = ("<html>"
           "<a href='../etienda/2-1'>Volver a la lista de consultas</a>"
           "<h1>Facturación total</h1> <ul> "
           "</html>")
    res += f"\n<html>La facturacion total es de {facturacion_total}.</html>"
    return HttpResponse(res)

def query_six(request):
    res = ("<html>"
           "<a href='../etienda/2-1'>Volver a la lista de consultas</a>"
           "<h1>Facturación por categoría de producto</h1> <ul> "
           "</html>")
    facturacion_cada_categoria = controller.run_query_six()
    for categoria, facturacion_categoria in facturacion_cada_categoria.items():
        res += (f"<html>"
                f"  <ul>"
                f"      <li>Categoría: {categoria} ===> {facturacion_categoria:.2f}</li><br>"
                f"  </ul>"
                f"</html>")
    return HttpResponse(res)


def home(request):
    template = loader.get_template("home.html")
    categories = controller.categories()
    products = controller.products()

    # Obtener images aleatorias para cada categoría
    category_images = {category: controller.images_category(category) for category in categories}

    context = {
        'products': products,
        'categories': categories,
        'category_images': category_images,
    }

    return HttpResponse(template.render(context, request))


def categoryproducts(request, category):
    template = loader.get_template("category_products.html")

    # Filtra los productos por la categoría proporcionada en la URL
    products = controller.products_by_category(category)
    categories = controller.categories()


    context = {
        'message': "Products in " + category,
        'products': products,
        'categories': categories,
    }

    return HttpResponse(template.render(context, request))


def search_results(request):
    query = request.GET.get('q', '')  # Obtén el término de búsqueda de la URL
    products = controller.search_products(query)  # Implementa esta función en tu lógica de controlador
    categories = controller.categories()

    context = {
        'query': query,
        'products': products,
        'categories': categories,
    }

    return render(request, 'search_results.html', context)