# etienda/urls.py
from django.urls import path, include
from . import views
from .api import api
app_name = 'etienda'

urlpatterns = [

    # Rutas normales
    path("", views.home, name="home"),
    path('search_category/<str:category>/', views.categoryproducts, name='category_products'),
    path('search/', views.search_results, name='search_results'),
    path('add-product', views.get_product_form, name='add-product'),
    path('thanks', views.thanks, name='thanks'),
    path("", include("django.contrib.auth.urls")),
]
