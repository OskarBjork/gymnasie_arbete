from pyng.space.phys_obj import PhysObj, Point
from pyng.space.vectors import TwoDimensionalVector
from pyng.space.grid import Grid


class PhysWorld:
    def __init__(
        self,
        width,
        height,
        gravity=TwoDimensionalVector(0, -9.82),
        objects: [PhysObj] =[],
    ):
        self.objects = objects
        self.gravity = gravity
        self.width = width
        self.height = height

    def step(self, delta_time: float):
        self.resolve_collision()
        for obj in self.objects:
            # TODO: Fixa +=
            # Lägger till gravitationskraften
            obj.force = obj.force + (self.gravity * obj.mass)
            # TODO: Kommentera
            obj.velocity = obj.velocity + (obj.force / obj.mass) * delta_time
            obj.position = obj.position + (obj.velocity * delta_time)
            obj.force = TwoDimensionalVector(0, 0)

    def resolve_collision(self):
        pass

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)
