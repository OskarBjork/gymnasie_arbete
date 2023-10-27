from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import Vector2D
from pyng.config import ORIGIN, RED, GRAVITY_CONSTANT
from pyng.space.phys_obj import PhysObj, Circle, Rectangle
import time


class State:
    def __init__(
        self,
        objects: [PhysObj] = [],
    ) -> None:
        self.objects = objects
        self.time_since_last_object_creation = time.time()

        self.default_object = Circle(color=RED, mass=10, radius=10)
        self.player_chosen_mass = 10
        self.player_chosen_shape = Circle
        self.player_chosen_radius = 10
        self.player_chosen_color = RED
        pass

    def parse_mouse_click(self, mouse_pos: Vector2D):
        if mouse_pos.x > ORIGIN[0] and mouse_pos.y > ORIGIN[1]:
            self.create_object(mouse_pos)

    def step(self, delta_time: float):
        for obj in self.objects:
            # TODO: Fixa +=
            obj.update_velocity(delta_time)
            obj.update_position(delta_time)

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)

    def create_object(
        self, position: Vector2D, obj: PhysObj = None, with_gravity=False
    ):
        if not (
            time.time() - self.time_since_last_object_creation > 0.1
        ):  # Kollar om det gått 0.1 sekunder sedan senaste objektet skapades
            return
        if obj is None:
            obj = Circle(
                mass=self.player_chosen_mass,
                radius=self.player_chosen_radius,
                color=self.player_chosen_color,
                position=position,
            )
        self.add_object(obj)
        self.time_since_last_object_creation = time.time()
        if with_gravity:
            self.impose_gravity(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)

    # TODO Möjligtvis flytta fysikfunktioner till egen klass

    def impose_gravity(self, obj: PhysObj):
        obj.add_force(Vector2D(0, GRAVITY_CONSTANT) * obj.mass)

    def check_collisions(self):
        for obj in self.objects:
            for other_obj in self.objects:
                if obj == other_obj:
                    continue
                if obj.is_inside_of(other_obj):
                    self.resolve_collision(obj, other_obj)

    def resolve_collision(self, obj: PhysObj, other_obj: PhysObj):
        if obj.isinstance(Circle) and other_obj.isinstance(Circle):
            d = obj.position.distance_to(other_obj.position)

            overlap_length = obj.radius + other_obj.radius - d

            direction = obj.position - other_obj.position

            direction = direction.normalize()

            magnitude = overlap_length / 2

            direction = direction * magnitude

            obj.position = obj.position + direction

            other_obj.position = other_obj.position - direction

        elif obj.isinstance(Circle) and other_obj.isinstance(Rectangle):
            obj.position.x = obj.position.x - obj.velocity.x
            obj.position.y = obj.position.y - obj.velocity.y
            other_obj.position.x = other_obj.position.x - other_obj.velocity.x
            other_obj.position.y = other_obj.position.y - other_obj.velocity.y

        self.resolve_momentum(obj, other_obj)

    def resolve_momentum(self, obj1, obj2):
        obj1_momentum = obj1.velocity * obj1.mass
        obj2_momentum = obj2.velocity * obj2.mass

        obj1.velocity = obj2_momentum / obj1.mass

        obj2.velocity = obj1_momentum / obj2.mass
