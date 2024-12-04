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
        error_messages = {
            'name': {
                'required': 'Product name is required.',
                'max_length': 'Product name cannot exceed 100 characters.'
            },
            'current_quantity_in_stock': {
                'required': 'Please enter the quantity in stock.',
                'min_value': 'The stock quantity must be >= 0.'
            },
            'raw_material_cost': {
                'required': 'Please provide the price cost for raw materials.',
                'min_value': 'Raw materials cost price cannot be negative.'
            },
            'profit_value': {
                'required': 'Profit value is mandatory.',
                'min_value': 'Profit value must be >= 0'
            },
            'profit_type': {
                'required': 'You must select a profit calculation type.'
            }
        }
