OPEN = "{"
CLOSE = "}"
COLON = ": "
DELIMITER = ", "

class MessageStringGenerator:
    def __init__(self):
        self.data = []
        self.first = True

    def open(self, typ):
        self.data.append(typ)
        self.data.append(OPEN)

    def close(self):
        self.data.append(CLOSE)

    def add(self, key, value):
        if self.first:
            self.first = False
        else:
            self.data.append(DELIMITER)
        self.data.append(str(key))
        self.data.append(COLON)
        self.data.append(str(value))

    def to_string(self):
        return "".join(self.data)
