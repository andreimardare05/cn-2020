class Element:
    value = 0
    position = 0

    def __init__(self, value, position):
        self.value = float(value)
        self.position = int(position)

    def __repr__(self):
        return "(" + str(self.value) + "," + str(self.position) + ")"

    def __copy__(self):
        return Element(self.value, self.position)