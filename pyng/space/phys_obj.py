from pyng.space.vectors import TwoDimensionalVector
from pyng.config import RED


class PhysObj:
    def __init__(self,
                 mass: float,
                 color: (int, int, int),
                 position: TwoDimensionalVector,
                 velocity=TwoDimensionalVector(0, 0),
                 force=TwoDimensionalVector(0, 0)):
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
