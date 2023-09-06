from pyng.space.phys_obj import PhysObj, Point
from pyng.space.vectors import TwoDimensionalVector
from pyng.space.grid import Grid


class PhysWorld:
    def __init__(
        self,
        width,
        height,
        gravity=TwoDimensionalVector(0, -9.82),
        objects: [PhysObj] = [],
    ):
        self.objects = objects
        self.gravity = gravity
        self.width = width
        self.height = height

    def step(self, delta_time: float):
        for obj in self.objects:
            # TODO: Fixa +=
            # Lägger till gravitationskraften
            obj.update_velocity(delta_time)
            obj.update_position(delta_time)

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)
