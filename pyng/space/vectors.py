import math


def vector_magnitude(vec):
    return math.sqrt(vec.x**2 + vec.y**2)


class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def tuple(self):
        return (self.x, self.y)

    def distance_to(self, other) -> float:
        return vector_magnitude(self - other)

    def magnitude(self) -> float:
        return vector_magnitude(self)

    def normalize(self):
        """
        Att normalisera en vektor innebär att man ändrar
        vektorns magnitud till 1 samtidigt som man behåller samma riktning
        """
        magnitude = self.magnitude()
        assert magnitude > 0
        return Vector2D(self.x, self.y) / magnitude

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
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    # Dividerar elementvis
    def element_division(self, vector):
        return Vector2D(self.x / vector.x, self.y / vector.y)

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

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def get_distance_to(self, other) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def dot(self, other):
        return self.x * other.x + self.y * other.y
