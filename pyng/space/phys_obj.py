from pyng.space.vectors import TwoDimensionalVector
from pyng.config import RED


class PhysObj:
    def __init__(
        self,
        mass: float,
        position: TwoDimensionalVector,  # koordinater
        velocity: TwoDimensionalVector,
        force: TwoDimensionalVector,
        color: tuple,
    ):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.force = force
        self.color = color


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
