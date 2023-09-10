import math


class TwoDimensionalVector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        """
        Att normalisera en vektor innebär att man ändrar
        vektorns magnitud till 1 samtidigt som man behåller samma riktning
        """
        magnitude = self.magnitude()
        assert magnitude > 0
        return TwoDimensionalVector(self.x, self.y) / magnitude

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return self.x != other.x and self.y != other.y

    def __le__(self, other) -> bool:
        return self.x <= other.x and self.y <= other.y

    def __ge__(self, other) -> bool:
        return self.x >= other.x and self.y >= other.y

    def __lt__(self, other) -> bool:
        return self.x < other.x and self.y < other.y

    def __gt__(self, other) -> bool:
        return self.x > other.x and self.y > other.y

    def __add__(self, other):
        return TwoDimensionalVector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return TwoDimensionalVector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return TwoDimensionalVector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return TwoDimensionalVector(self.x / scalar, self.y / scalar)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def __itruediv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
