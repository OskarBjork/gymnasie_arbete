from pyng.space.vectors import TwoDimensionalVector
from pyng.config import RED


class PhysObj:
    def __init__(
        self,
        mass: float,
        position: TwoDimensionalVector,  # koordinater
        velocity: TwoDimensionalVector,
        force: TwoDimensionalVector,
    ):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.force = force
        self.color = RED


class Point(PhysObj):
    def __init__(
        self,
        mass: float,
        position: TwoDimensionalVector,
        velocity: TwoDimensionalVector,
        force: TwoDimensionalVector,
    ):
        super().__init__(mass, position, velocity, force)
        self.color = RED
