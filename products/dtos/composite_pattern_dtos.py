from abc import ABC
from typing import List

from products.models import ProfitType


class IProductDTO(ABC):
    """The Component interface sets the common method for all components."""

    def __init__(self, id_request, name_request, description_request="", cost_price_request=0.0,
                 profit_value_request=0.0,
                 profit_type_request=ProfitType.BY_PERCENTAGE,
                 current_quantity_in_stock_request=0, children_request=None):
        self.id = id_request
        self.name = name_request
        self.description = description_request
        self.cost_price = cost_price_request
        self.profit_value = profit_value_request
        self.profit_type = profit_type_request
        self.current_quantity_in_stock = current_quantity_in_stock_request
        self.children = children_request

    @property
    def id(self) -> str:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def description(self) -> str:
        raise NotImplementedError

    @property
    def cost_price(self) -> float:
        raise NotImplementedError

    @property
    def selling_price(self) -> float:
        raise NotImplementedError

    @property
    def profit_value(self) -> float:
        raise NotImplementedError

    @property
    def profit_type(self) -> ProfitType:
        raise NotImplementedError

    @property
    def current_quantity_in_stock(self) -> int:
        raise NotImplementedError

    @id.setter
    def id(self, value):
        raise NotImplementedError

    # @property
    # def children(self) -> int:
    #     raise NotImplementedError
    #
    # @children.setter
    # def children(self, value):
    #     raise NotImplementedError

    @name.setter
    def name(self, value):
        raise NotImplementedError

    @description.setter
    def description(self, value):
        raise NotImplementedError

    @cost_price.setter
    def cost_price(self, value):
        raise NotImplementedError

    @profit_value.setter
    def profit_value(self, value):
        raise NotImplementedError

    @profit_type.setter
    def profit_type(self, value: ProfitType):
        raise NotImplementedError

    @current_quantity_in_stock.setter
    def current_quantity_in_stock(self, value):
        raise NotImplementedError


class LeafProductDTO(IProductDTO):
    """Leaf represents individual objects that don’t contain other elements."""

    ## validações aqui??

    def __init__(self, id_request, name, description, cost_price, profit_value,
                 profit_type,
                 current_quantity_in_stock):
        super().__init__(id_request, name, description, cost_price, profit_value,
                         profit_type,
                         current_quantity_in_stock)

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def cost_price(self) -> float:
        return round(self._cost_price, 2)

    @property
    def selling_price(self) -> float:
        if self._profit_type == ProfitType.BY_PERCENTAGE:
            gain = self._cost_price * self._profit_value
        else:
            gain = self._cost_price + self._profit_value

        return round((self._cost_price + gain), 2)

    @property
    def profit_value(self) -> float:
        return self._profit_value

    @property
    def profit_type(self) -> ProfitType:
        return self._profit_type

    @property
    def current_quantity_in_stock(self) -> int:
        return self._current_quantity_in_stock

    @id.setter
    def id(self, value):
        self._id = value

    @name.setter
    def name(self, value):
        self._name = value

    @description.setter
    def description(self, value):
        self._description = value

    @cost_price.setter
    def cost_price(self, value):
        self._cost_price = value

    @profit_value.setter
    def profit_value(self, value):
        self._profit_value = value

    @profit_type.setter
    def profit_type(self, value):
        self._profit_type = value

    @current_quantity_in_stock.setter
    def current_quantity_in_stock(self, value):
        self._current_quantity_in_stock = value


class ChildDTO(IProductDTO):
    requested_quantity: int
    product: IProductDTO


class CompositeProductWithChildrenDTO(IProductDTO):
    """Composite acts as a container that can hold both Leaf and other Composite instances."""
    _children: List[ChildDTO]
    _base_props: LeafProductDTO

    def __init__(self, id_request, name, description, cost_price, profit_value,
                 profit_type,
                 current_quantity_in_stock, children_request=None):

        leaf = LeafProductDTO(
            id_request, name, description, cost_price, profit_value,
            profit_type, current_quantity_in_stock
        )

        self._base_props = leaf

        if children_request is not None:
            self._children = children_request
        else:
            self._children = []

        super().__init__(id_request, name, description, cost_price, profit_value,
                         profit_type,
                         current_quantity_in_stock)

        self.base_props = LeafProductDTO(id_request, name, description, cost_price, profit_value,
                                         profit_type,
                                         current_quantity_in_stock)

    def add(self, component: ChildDTO):
        self.children.append(component)

    def remove(self, component: ChildDTO):
        self.children.remove(component)

    @property
    def id(self) -> str:
        return self.base_props.id

    @property
    def name(self) -> str:
        return self.base_props.name

    @property
    def description(self) -> str:
        return self.base_props.description

    @property
    def cost_price(self) -> float:
        total_cost = 0.0
        for child in self._children:
            total_cost += child.product.cost_price * child.requested_quantity

        return total_cost + self.base_props.cost_price

    @property
    def selling_price(self) -> float:
        self_cost_price = self.cost_price
        if self.base_props.profit_type == ProfitType.BY_PERCENTAGE:
            gain = self_cost_price * self.profit_value
        else:
            gain = self_cost_price + self.profit_value

        return round((self_cost_price + gain), 2)

    @property
    def profit_value(self) -> float:
        return self.base_props.profit_value

    @property
    def profit_type(self) -> ProfitType:
        return self.base_props.profit_type

    @property
    def current_quantity_in_stock(self) -> int:
        return self.base_props.current_quantity_in_stock

    @id.setter
    def id(self, value):
        self.base_props.id = value

    @property
    def base_props(self) -> LeafProductDTO:
        return self._base_props

    @base_props.setter
    def base_props(self, value: LeafProductDTO):
        self._base_props = value

    @property
    def children(self) -> [ChildDTO]:
        return self._children

    @children.setter
    def children(self, value: [ChildDTO]):
        if value is None:
            value = []
        self._children = value

    @name.setter
    def name(self, value):
        self.base_props.name = value

    @description.setter
    def description(self, value):
        self.base_props.description = value

    @cost_price.setter
    def cost_price(self, value):
        self.base_props.cost_price = value

    @profit_value.setter
    def profit_value(self, value):
        self.base_props.profit_value = value

    @profit_type.setter
    def profit_type(self, value):
        self.base_props.profit_type = value

    @current_quantity_in_stock.setter
    def current_quantity_in_stock(self, value):
        self.base_props.current_quantity_in_stock = value
