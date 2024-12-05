from django import forms

from products.models import ProductComponent, Product


class ComponentForm(forms.ModelForm):
    class Meta:
        model = ProductComponent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the display of child_product
        self.fields['child_product'].queryset = Product.objects.all()
        self.fields['child_product'].to_field_name = 'id'  # Use ID for selection
        self.fields['child_product'].label_from_instance = lambda \
                obj: f"{obj.name} (Stock: {obj.current_quantity_in_stock})"

    def save(self, commit=True):
        component = super().save(commit=commit)

        components_data = self.cleaned_data
        print('ComponentForm components_data', components_data)
        return component


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'current_quantity_in_stock',
            'raw_material_cost',
            'profit_value',
            'profit_type',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        product = super().save(commit=commit)

        components_data = self.cleaned_data
        print('ProductForm components_data', components_data)
        return product
