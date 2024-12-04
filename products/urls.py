from django.urls import path

from . import views

urlpatterns = [
    path('', views.foo, name='foo'),

    path('products/', views.list_products, name='products'),
    path('products/<str:pk>/', views.get_product, name='get_product'),

    path('products/new', views.create_product, name='create_product'),

    path('foo/', views.foo, name='foo'),

]
