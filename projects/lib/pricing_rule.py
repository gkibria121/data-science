# models/pricing_rule.py
class PricingRule:
    def __init__(self, attribute_name: str, attribute_value: str, percentage_change: float):
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.percentage_change = percentage_change
