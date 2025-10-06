# models/product.py
from .pricing_rule import PricingRule
from .delivery_rule import DeliveryRule
from .quantity_pricing import QuantityPricing

class Product:
    def __init__(self, name: str, pricing_rules=None, delivery_rules=None, quantity_pricings=None, vat_rate: float = 0.0):
        self.name = name
        self.pricing_rules = pricing_rules or []
        self.delivery_rules = delivery_rules or []
        self.quantity_pricings = quantity_pricings or []
        self.vat_rate = vat_rate
