from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import TwoDimensionalVector
from pyng.space.grid import Grid


class PhysWorld:
    def __init__(self, objects: [PhysObj] = []):
        self.objects = objects
        self.gravity = TwoDimensionalVector(0, -9.82)

    def step(self, delta_time: float):
        for obj in self.objects:
            obj.force += obj.mass * self.gravity
            obj.velocity += (obj.force / obj.mass) * delta_time
            obj.position += obj.velocity * delta_time
            obj.force = TwoDimensionalVector(0, 0)

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)
