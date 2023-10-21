from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import Vector2D
from pyng.config import ORIGIN, RED
from pyng.space.phys_obj import PhysObj, Circle


class State:
    def __init__(
        self,
        objects: [PhysObj] = [],
    ) -> None:
        self.objects = objects

        self.default_object = Circle(color=RED, mass=10, radius=10)
        self.player_chosen_mass = 10
        self.player_chosen_shape = Circle
        self.player_chosen_radius = 10
        self.player_chosen_color = RED
        pass

    def step(self, delta_time: float):
        for obj in self.objects:
            # TODO: Fixa +=
            obj.update_velocity(delta_time)
            obj.update_position(delta_time)

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)

    def create_object(self, position: Vector2D, obj: PhysObj = None):
        if obj is None:
            obj = self.default_object
        obj.position = position
        self.objects.append(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)

    def check_collisions(self):
        for obj in self.objects:
            for other_obj in self.objects:
                if obj == other_obj:
                    continue
                if obj.is_inside_of(other_obj):
                    self.resolve_collision(obj, other_obj)

    def resolve_collision(self, obj: PhysObj, other_obj: PhysObj):
        d = obj.position.distance_to(other_obj.position)

        overlap_length = obj.radius + other_obj.radius - d

        direction = obj.position - other_obj.position

        direction = direction.normalize()

        magnitude = overlap_length / 2

        direction = direction * magnitude

        obj.position = obj.position + direction

        other_obj.position = other_obj.position - direction

        self.resolve_momentum(obj, other_obj)

    def resolve_momentum(obj1, obj2):
        obj1_momentum = obj1.velocity * obj1.mass
        obj2_momentum = obj2.velocity * obj2.mass

        obj1.velocity = obj2_momentum / obj1.mass

        obj2.velocity = obj1_momentum / obj2.mass
