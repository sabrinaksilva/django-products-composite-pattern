from django.shortcuts import get_object_or_404

from products.models import Product, ProfitType


class ProductService:

    ## TO-DO: deal not found
    @staticmethod
    def get_product_by_id(product_id=None):
        product = get_object_or_404(Product, id=product_id)
        return product

    @staticmethod
    def get_products():
        products: list[Product] = Product.objects.all()
        return products

    @staticmethod
    def create_product(name: str, description: str, current_quantity_in_stock: int, raw_material_cost: float,
                       profit_value: float, profit_type: ProfitType):
        product = Product(name=name, description=description, current_quantity_in_stock=current_quantity_in_stock,
                          raw_material_cost=raw_material_cost,
                          profit_type=profit_type, profit_value=profit_value)
        savedProduct = Product.objects.create(product=product)
        return savedProduct
