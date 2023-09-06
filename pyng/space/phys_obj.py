from pyng.space.vectors import TwoDimensionalVector


class PhysObj:
    def __init__(self,
                 mass: float,
                 position: TwoDimensionalVector,
                 velocity=TwoDimensionalVector(0, 0),
                 force=TwoDimensionalVector(0, 0)):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.force = force

    def add_force(self, force: TwoDimensionalVector):
        self.force += force
