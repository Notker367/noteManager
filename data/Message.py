class Message:
    def __init__(self, text, timestamp):
        self.text = text
        self.timestamp = timestamp

    @classmethod
    def from_json(cls, data):
        return cls(data["text"], data["timestamp"])

    def to_json(self):
        return {
            "text": self.text,
            "timestamp": self.timestamp
        }