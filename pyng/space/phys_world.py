from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import TwoDimensionalVector
from pyng.space.grid import Grid


class PhysWorld:
    def __init__(self, objects=None):
        if objects is None:
            objects = []
        self.objects = objects
        self.gravity = TwoDimensionalVector(0, -9.82)

    def step(self, delta_time: float):
        for obj in self.objects:
            pass

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)
