import math

class Vector:
    #TODO Use operator overloading(http://blog.teamtreehouse.com/operator-overloading-python)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def to_unit():
        norm = math.sqrt(x ** 2 + y ** 2)
        return Vector(x * norm, y * norm)
