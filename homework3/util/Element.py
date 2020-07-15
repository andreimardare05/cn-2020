class Element:
    value = 0
    position = 0

    def __init__(self, value, position):
        self.value = float(value)
        self.position = int(position)

    def __repr__(self):
        return "(" + str(self.value) + "," + str(self.position) + ")"

    def __eq__(self, element):
        return element.value == self.value and element.position == self.position

    def copy(self):
        return Element(self.value, self.position)
