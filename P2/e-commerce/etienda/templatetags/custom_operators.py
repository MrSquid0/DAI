from django import template

register = template.Library()


@register.filter
def get_image_route(product, field_name='imágen'):
    if isinstance(product, dict):
        image_path = product.get(field_name, '')
        if '/' in image_path:
            values = image_path.split('/')
            return 'images/' + values[-1]
    return 'images/default_image.png'
