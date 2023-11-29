import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse
from . import controller
from .forms import ProductForm
from .models import Producto
from django.contrib.admin.views.decorators import staff_member_required
import logging

logger = logging.getLogger(__name__)

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


@staff_member_required
def get_product_form(request):
    template = loader.get_template("add-product.html")
    categories = controller.categories()

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

            controller.insert_product_to_db(producto)
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
