from django.contrib import admin

from .models import Product, ProductComponent

admin.site.register(Product)
admin.site.register(ProductComponent)
