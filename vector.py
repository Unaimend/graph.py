import math


class Vector:
    # TODO Use operator overloading(http://blog.teamtreehouse.com/operator-overloading-python)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def to_unit(self):
        norm = math.sqrt(self.x ** 2 + self.y ** 2)
        a = Vector(self.x / norm, self.y / norm)
        return a

    def abs(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self):
        return "x:" + str(self.x) + "y:" + str(self.y)
