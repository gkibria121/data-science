# models/delivery_rule.py
class DeliveryRule:
    def __init__(self, delivery_nature: str, delivery_fee: float):
        self.delivery_nature = delivery_nature
        self.delivery_fee = delivery_fee
