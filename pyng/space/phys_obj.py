from pyng.space.vectors import TwoDimensionalVector
from pyng.config import RED


class PhysObj:
    def __init__(
            self,
            mass: float,
            color: (int, int, int),
            position: TwoDimensionalVector,
            velocity=TwoDimensionalVector(0, 0),
            force=TwoDimensionalVector(0, 0)
    ):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.force = force
        self.color = color

    def add_force(self, force: TwoDimensionalVector):
        self.force += force


class Point(PhysObj):
    def __init__(
            self,
            mass: float,
            position: TwoDimensionalVector,
            velocity: TwoDimensionalVector,
            force: TwoDimensionalVector,
            color: tuple,
    ):
        super().__init__(mass, position, velocity, force, color)

    def is_out_of_bounds(self, width: float, height: float) -> bool:
        if (self.position.x < 0 or self.position.x > width
                or self.position.y < 0 or self.position.y > height):
            return True
        return False
