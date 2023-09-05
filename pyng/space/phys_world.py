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
        self.add_object(
            Point(
                1,
                TwoDimensionalVector(50, 100),
                TwoDimensionalVector(0, 0),
                TwoDimensionalVector(0, 0),
            )
        )

    def step(self, delta_time: float):
        for obj in self.objects:
            pass

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)
