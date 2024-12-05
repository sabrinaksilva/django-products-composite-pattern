import uuid

from products.dtos.composite_pattern_dtos import LeafProductDTO, IProductDTO, CompositeProductWithChildrenDTO
from products.models import ProfitType


def test_should_create_LeafProduct_with_correct_fields():
    id_request = str(uuid.UUID('12345678-1234-5678-1234-567812345678'))  # UUID estático
    name = "Test Product"
    description = "This is a test product"
    cost_price = 123.45
    profit_value = 0.2  # 20%
    profit_type = ProfitType.BY_PERCENTAGE
    current_quantity_in_stock = 10

    leaf_product = LeafProductDTO(
        id_request=id_request,
        name=name,
        description=description,
        cost_price=cost_price,
        profit_value=profit_value,
        profit_type=profit_type,
        current_quantity_in_stock=current_quantity_in_stock
    )

    assert isinstance(leaf_product, LeafProductDTO)
    assert isinstance(leaf_product, IProductDTO)

    assert leaf_product.id == id_request
    assert leaf_product.name == name
    assert leaf_product.description == description
    assert round(leaf_product.cost_price, 2) == round(cost_price, 2)
    assert leaf_product.profit_value == profit_value
    assert leaf_product.profit_type == profit_type
    assert leaf_product.current_quantity_in_stock == current_quantity_in_stock


def test_should_create_CompositeProduct_with_no_children():
    # Valores estáticos para os parâmetros
    id_request = str(uuid.UUID('87654321-4321-8765-4321-876543218765'))  # UUID estático
    name = "Composite Test Product"
    description = "This is a composite test product"
    cost_price = 200.50
    profit_value = 0.15  # 15%
    profit_type = ProfitType.FIXED
    current_quantity_in_stock = 5

    # Criação do CompositeProduct com children=None
    composite_product = CompositeProductWithChildrenDTO(
        id_request=id_request,
        name=name,
        description=description,
        cost_price=cost_price,
        profit_value=profit_value,
        profit_type=profit_type,
        current_quantity_in_stock=current_quantity_in_stock,
        children_request=None
    )

    # Assert: o objeto criado é uma instância de CompositeProduct e IProductDTO
    assert isinstance(composite_product, CompositeProductWithChildrenDTO)
    assert isinstance(composite_product, IProductDTO)

    # Assert: validação de cada parâmetro
    assert composite_product.id == id_request
    assert composite_product.name == name
    assert composite_product.description == description
    assert round(composite_product.cost_price, 2) == round(cost_price, 2)
    assert composite_product.profit_value == profit_value
    assert composite_product.profit_type == profit_type
    assert composite_product.current_quantity_in_stock == current_quantity_in_stock

    # Assert: a lista de children deve estar vazia
    assert composite_product.children == []
