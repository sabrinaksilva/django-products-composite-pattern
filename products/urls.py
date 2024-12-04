from django.urls import path

from . import views

urlpatterns = [
    path('', views.foo, name='foo'),

    path('dashboard/', views.dashboard, name='home'),
    path('products/', views.products, name='products'),
    path('products/new', views.create_product, name='create_product'),

    path('foo/', views.foo, name='foo'),

]
