# price_calculation_request.py
from  lib.attribute import Attribute

class PriceCalculationRequest:
    def __init__(self, product_name: str, quantity: float, selected_attributes: list[Attribute], delivery_method: str):
        self.product_name = product_name
        self.quantity = quantity
        self.selected_attributes = selected_attributes
        self.delivery_method = delivery_method
