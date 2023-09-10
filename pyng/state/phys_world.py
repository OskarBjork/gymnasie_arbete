from pyng.space.phys_obj import PhysObj, Point
from pyng.space.vectors import Vector2D
from pyng.space.grid import Grid


class PhysWorld:
    def __init__(
        self,
        width,
        height,
        gravity=Vector2D(0, -9.82),
        objects: [PhysObj] = [],
    ):
        self.objects = objects
        self.gravity = gravity
        self.width = width
        self.height = height

    def step(self, delta_time: float):
        self.resolve_collision()
        for obj in self.objects:
            # TODO: Fixa +=
            obj.update_velocity(delta_time)
            obj.update_position(delta_time)

    def resolve_collision(self):
        pass

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)
