class CreatePrPayload:
    def __init__(self, title, head, base, body):
        self.title = title
        self.head = head
        self.base = base
        self.body = body

    def to_dict(self):
        return {
            "title": self.title,
            "head": self.head,
            "base": self.base,
            "body": self.body,
        }
