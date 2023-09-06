from pyng.space.phys_obj import PhysObj, Point
from pyng.space.vectors import TwoDimensionalVector
from pyng.space.grid import Grid


class PhysWorld:
    def __init__(
        self,
        width,
        height,
        objects: [PhysObj] = [],
    ):
        self.objects = objects
        self.gravity = TwoDimensionalVector(0, -9.82)
        self.grid = Grid(width=width, height=height)
        self.width = width
        self.height = height

    def step(self, delta_time: float):
        for obj in self.objects:
            pass

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)
        self.grid.set_coordinate_value(obj.position.x, obj.position.y, obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)
