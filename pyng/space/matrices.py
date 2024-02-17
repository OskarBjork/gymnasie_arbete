from pyng.space.vectors import Vector2D

class Matrix2x2:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def mult(self, other):
        return Matrix2x2(self.a * other.a + self.b * other.c,
                         self.a * other.b + self.b * other.d,
                         self.c * other.a + self.d * other.c,
                         self.c * other.b + self.d * other.d)

    def mult_vector2d(self, vector: Vector2D) -> Vector2D:
        return Vector2D(self.a * vector.x + self.b * vector.y,
                        self.c * vector.x + self.d * vector.y)
