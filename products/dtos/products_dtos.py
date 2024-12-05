import uuid

from django import forms
from django.core.validators import MinValueValidator

from products.models import ProfitType


class BasicProductFormDTO(forms.Form):
    id = forms.UUIDField(default=uuid.uuid4)
    name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=256, required=False)

    current_quantity_in_stock = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(0)],
        help_text="Current available (produced/in stock) quantity"
    )
    reserved_quantity_in_stock = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(0)],
        help_text="Quantity reserved to produce another parent product"
    )
    raw_material_cost = forms.FloatField(
        required=True,
        validators=[MinValueValidator(0)],
        help_text="Cost of raw materials"
    )

    profit_value = forms.FloatField(
        required=True,
        validators=[MinValueValidator(0)],
        help_text="Profit value applied to the cost price"
    )
    profit_type = forms.ChoiceField(
        choices=ProfitType.choices,
        required=True,
        help_text="How will profit value be calculated"
    )


class ComponentFormDTO(forms.Form):
    id = forms.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )

    child_product: BasicProductFormDTO
    quantity = forms.IntegerField(null=False,
                                  blank=False,
                                  validators=[MinValueValidator(0)],
                                  default=0,
                                  help_text="The quantity of the child product required to produce the parent product.")


class ProductAndComponentsFormDTO(forms.Form):
    id = forms.UUIDField(default=uuid.uuid4)
    name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=256, required=False)

    current_quantity_in_stock = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(0)],
        help_text="Current available (produced/in stock) quantity"
    )
    reserved_quantity_in_stock = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(0)],
        help_text="Quantity reserved to produce another parent product"
    )
    raw_material_cost = forms.FloatField(
        required=True,
        validators=[MinValueValidator(0)],
        help_text="Cost of raw materials"
    )

    profit_value = forms.FloatField(
        required=True,
        validators=[MinValueValidator(0)],
        help_text="Profit value applied to the cost price"
    )
    profit_type = forms.ChoiceField(
        choices=ProfitType.choices,
        required=True,
        help_text="How will profit value be calculated"
    )

    def save(self):
        """
        Custom save method to return data as a dictionary or create objects manually.
        """
        data = self.cleaned_data
        # Você pode criar o objeto Product ou apenas retornar os dados
        return data
