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
    total_quantity = models.IntegerField(null=False,
                                         blank=False,
                                         validators=[MinValueValidator(0)],
                                         default=0)

    raw_material_cost = models.FloatField(null=False, blank=False,
                                          validators=[MinValueValidator(0)],
                                          default=0.0)
    profit_value = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0)],
        help_text="Profit value applied to the cost price"
    )
    profit_type = models.CharField(
        max_length=20,
        choices=ProfitType.choices,
        default=ProfitType.BY_PERCENTAGE,
        help_text="How will profit value be calculated from cost price: summing up a fixed value or by percentage"
    )

    def __str__(self):
        return f'Product ID [{self.id}] : {self.name} ({self.description})'

    @property
    def components_list(self):
        """
        Returns a list of all components (child products and their quantities)
        required to produce this product.
        """
        return [
            {
                "child_product": component.child_product,
                "quantity": component.quantity
            }
            for component in self.components.all()
        ]

    def is_composition(self):
        return len(self.components_list) > 0


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
        return f'ProductComponent: {self.quantity} x {self.child_product.name} for {self.parent_product.name}'
