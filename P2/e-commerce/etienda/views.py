import json

import pymongo
import sys

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from . import controller
from .forms import ProductForm
from .models import Producto
from django.contrib.admin.views.decorators import staff_member_required
import logging

logger = logging.getLogger(__name__)


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
    template = loader.get_template("search_results.html")
    query = request.GET.get('q', '')  # Obtiene el término de búsqueda de la URL
    products = controller.search_products(query)
    categories = controller.categories()

    no_results = not bool(products)

    context = {
        'query': query,
        'products': products,
        'categories': categories,
        'no_results': no_results,
    }

    if not bool(products):
        logger.warning("The search bar was used with no results")

    return HttpResponse(template.render(context, request))


import os
from django.conf import settings


@staff_member_required
def get_product_form(request):
    template = loader.get_template("add-product.html")
    categories = controller.categories()
    tienda_productos = controller.get_tienda_db()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            # Obtener la ruta del directorio de medios estáticos
            static_images_dir = os.path.join(settings.BASE_DIR, 'static/images/')

            # Guardar la imagen en el sistema de archivos
            image_path = os.path.join(static_images_dir, form.cleaned_data['image'].name)
            with open(image_path, 'wb') as destination:
                for chunk in form.cleaned_data['image'].chunks():
                    destination.write(chunk)

            producto = Producto(
                producto_id=controller.get_maximum_product_id() + 1,
                nombre=form.cleaned_data['name'],
                precio=form.cleaned_data['price'],
                descripción=form.cleaned_data['description'],
                categoría=form.cleaned_data['category'],
                imágen=image_path,
                rating=None,
            )

            tienda_productos.insert_one(producto.model_dump())
            logger.info('A new product was added to the e-commerce.')
            # Redirige a la página de agradecimiento
            return HttpResponseRedirect("/etienda/thanks")
        else:
            logger.error('The submitted form was not valid.')
    else:
        form = ProductForm()

    context = {
        "form": form,
        "categories": categories,
    }
    return HttpResponse(template.render(context, request))

def thanks(request):
    template = loader.get_template("thanks.html")
    categories = controller.categories()

    context = {
        "categories": categories,
    }

    return HttpResponse(template.render(context, request))
