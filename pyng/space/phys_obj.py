from pyng.space.vectors import TwoDimensionalVector


class PhysObj:
    def __init__(self,
                 mass: float,
                 position: TwoDimensionalVector,  # koordinater
                 velocity: TwoDimensionalVector,
                 force: TwoDimensionalVector):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.force = force
