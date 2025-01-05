class Finance:
    def __init__(self, amount, category, timestamp):
        self.amount = amount
        self.category = category
        self.timestamp = timestamp

    @classmethod
    def from_json(cls, data):
        return cls(data["amount"], data["category"], data["timestamp"])

    def to_json(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "timestamp": self.timestamp
        }