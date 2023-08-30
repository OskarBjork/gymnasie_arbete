from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import TwoDimensionalVector
from pyng.space.grid import Grid


class PhysWorld:
    def __init__(self, grid: Grid, objects: [PhysObj] = None):
        if objects is None:
            objects = []
        self.objects = objects
        self.grid = grid
        self.gravity = TwoDimensionalVector(0, -9.82)

    def step(self, delta_time: float):
        for obj in self.objects:
            obj.force += obj.mass * self.gravity
            obj.position += obj.velocity * delta_time

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)
