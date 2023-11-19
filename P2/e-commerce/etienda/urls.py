from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'etienda'

urlpatterns = [
    path("2-1", views.index_2_1, name="index_2_1"),
    path("electronica", views.query_one, name="query_one"),
    path("pocket", views.query_two, name="query_two"),
    path("productos-puntuacion", views.query_three, name="query_three"),
    path("hombre-puntuacion", views.query_four, name="query_four"),
    path("facturacion-total", views.query_five, name="query_five"),
    path("facturacion-categoria", views.query_six, name="query_six"),
    path("", views.home, name="home"),
    path('search_category/<str:category>/', views.categoryproducts, name='category_products'),
    path('search/', views.search_results, name='search_results'),
]