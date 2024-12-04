from django import forms

from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'current_quantity_in_stock',
            'raw_material_cost',
            'profit_value',
            'profit_type'
        ]
