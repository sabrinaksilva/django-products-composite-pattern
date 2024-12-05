import json
import uuid

from django.core.validators import MinValueValidator
from django.db import models


class ProfitType(models.TextChoices):
    BY_PERCENTAGE = 'BY_PERCENTAGE', 'By Percentage'
    FIXED = 'FIXED', 'Fixed'


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=256, null=True, blank=True)

    # in creation, this value is set with max value setted going trought all components
    # does not decrease current quantity of children elements if removed
    current_quantity_in_stock = models.IntegerField(null=False,
                                                    validators=[MinValueValidator(0)],
                                                    default=0,
                                                    help_text="Current available (produced/in stock) quantity")

    reserved_quantity_in_stock = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)],
                                                     default=0,
                                                     help_text="Quantity reserved to produce another parent product")

    raw_material_cost = models.FloatField(null=False, blank=False,
                                          validators=[MinValueValidator(0)],
                                          default=0.0)
    profit_value = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0)],
        help_text="Profit value applied to the cost price"
    )
    profit_type = models.CharField(
        max_length=20,
        choices=ProfitType.choices,
        default=ProfitType.BY_PERCENTAGE,
        help_text="How will profit value be calculated from cost price: summing up a fixed value or by percentage"
    )

    def __str__(self):
        return json.dumps({
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "current_quantity_in_stock": self.current_quantity_in_stock,
            "reserved_quantity_in_stock": self.reserved_quantity_in_stock,
            "raw_material_cost": self.raw_material_cost,
            "profit_value": self.profit_value,
            "profit_type": self.profit_type,
            "cost_price": self.cost_price
        })

    @property
    def components_list(self):
        """
        Returns a list of all components (child products and their quantities)
        in a JSON-serializable format.
        """
        all_components = self.components.all()
        if not all_components:
            all_components = []

            return [
                {
                    "product_component_id": str(component.id),
                    "child_product_id": str(component.child_product.id),
                    "child_product_name": str(component.child_product.name),
                    "child_product_description": str(component.child_product.description),
                    "child_product_current_quantity_in_stock": int(component.child_product.current_quantity_in_stock),
                    "quantity": int(component.quantity)
                }
                for component in all_components
            ]
        # return [
        #     {
        #         "product_component_id": str(component.id),
        #         "child_product_id": str(component.child_product.id),
        #         "child_product_name": 'component.child_product.name',
        #         "child_product_description": 'component.child_product.description',
        #         "child_product_current_quantity_in_stock": 'component.child_product.current_quantity_in_stock',
        #         "quantity": component.quantity
        #     }
        #     for component in all_components
        # ]

    @property
    def cost_price(self):
        """
        Calculate the total cost price of the product:
        Sum of the cost prices of all child products multiplied by their quantities,
        plus this product's raw material cost.
        """
        # Base cost is the raw_material_cost of the current product
        base_cost = self.raw_material_cost

        # Add the cost of all components (child products)
        components_cost = sum(
            component.child_product.raw_material_cost * component.quantity
            for component in self.components.select_related('child_product')
        )

        return base_cost + components_cost


class ProductComponent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # TO-TO: VALIDATE BEST on_delete policy
    parent_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="components",
        help_text="The product that this component is used to produce."
    )

    # TO-TO: VALIDATE BEST on_delete policy
    child_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="used_in",
        help_text="The component product used to produce the parent product."
    )
    quantity = models.IntegerField(null=False,
                                   blank=False,
                                   validators=[MinValueValidator(0)],
                                   default=0,
                                   help_text="The quantity of the child product required to produce the parent product.")

    def __str__(self):
        return json.dumps({
            "id": str(self.id),
            "parent_product": {
                "id": str(self.parent_product.id),
                "name": self.parent_product.name
            },
            "child_product": {
                "id": str(self.child_product.id),
                "name": self.child_product.name
            },
            "quantity": self.quantity
        })
