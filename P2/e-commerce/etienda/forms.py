# forms.py
import logging
logger = logging.getLogger(__name__)

from django import forms
from django.core.validators import MinValueValidator, MinLengthValidator
from pydantic import ValidationError

from . import controller


class ProductForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    price = forms.DecimalField(label='Price', validators=[MinValueValidator(0)])
    description = forms.CharField(
        label='Description',
        max_length=1000,
        validators=[MinLengthValidator(100)],
        widget=forms.Textarea(attrs={'rows': 5})
    )
    category = forms.ChoiceField(label='Category', choices=[], widget=forms.Select)
    image = forms.ImageField(label='Image')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        categories = controller.categories()
        #Imprimo todas las categorías existentes en la BD
        self.fields['category'].choices = [(category, category) for category in categories]

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if not name or not name[0].isupper():
            raise ValidationError("The first letter of the name of the product must be uppercase.")
        return name
