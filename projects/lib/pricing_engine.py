# pricing_engine.py
from lib.exceptions import PriceEngineException
from lib.quadratic_curve_fitter import QuadraticCurveFitter

class PricingEngine:
    def __init__(self, product):
        self.curve_fitter = QuadraticCurveFitter()
        self.pricing_rules = product.pricing_rules
        self.delivery_rules = product.delivery_rules
        self.quantity_pricings = product.quantity_pricings
        self.curve_fitter.fit(product.quantity_pricings)
        self.vat_rate = product.vat_rate

    def calculate_price(self, request):
        if request.quantity <= 0:
            return self._incomplete_result("Invalid quantity")

        min_qty = min(p.quantity for p in self.quantity_pricings)
        max_qty = max(p.quantity for p in self.quantity_pricings)
        if request.quantity < min_qty or request.quantity > max_qty:
            raise PriceEngineException("Request quantity out of Quantity pricing range")

        base_price = self.curve_fitter.predict(request.quantity)
        total = base_price

        try:
            for attribute in request.selected_attributes:
                rule = next(
                    (r for r in self.pricing_rules
                     if r.attribute_name == attribute.name and r.attribute_value == attribute.value),
                    None
                )
                if rule:
                    total += total * (rule.percentage_change / 100)
                else:
                    raise ValueError(f'Attribute "{attribute.name}" with value "{attribute.value}" not found.')
        except Exception as e:
            return self._incomplete_result(str(e))

        attribute_cost = total - base_price

        delivery_rule = next(
            (r for r in self.delivery_rules
             if r.delivery_nature.lower() == request.delivery_method.lower()),
            None
        )
        if not delivery_rule:
            return self._incomplete_result("Invalid delivery nature")

        tax = total * (self.vat_rate / 100)
        total += tax + delivery_rule.delivery_fee

        return {
            "totalPrice": total,
            "status": "complete",
            "breakdown": {
                "basePrice": base_price,
                "attributeCost": attribute_cost,
                "deliveryCharge": delivery_rule.delivery_fee,
                "tax": tax
            }
        }

    def _incomplete_result(self, message: str):
        return {
            "totalPrice": 0,
            "status": "incomplete",
            "message": message,
            "breakdown": {
                "basePrice": 0,
                "attributeCost": 0,
                "deliveryCharge": 0,
                "tax": 0
            }
        }
