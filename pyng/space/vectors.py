class TwoDimensionalVector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

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

    def __mul__(self, other):
        return TwoDimensionalVector(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        pass

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __imul__(self, other):
        self.x *= other.x
        self.y *= other.y

    def __idiv__(self, other):
        self.x /= other.x
        self.y /= other.y
