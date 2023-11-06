from pyng.space.vectors import Vector2D
from pyng.config import ORIGIN, RED, GRAVITY_CONSTANT
from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon
from pyng.state.physics_evaluator import PhysicsEvaluator
from pyng.state.phys_world import PhysWorld
import time
import math
import pprint

pp = pprint.PrettyPrinter(indent=2)


class State:
    def __init__(
        self,
        objects: [PhysObj] = [],
    ) -> None:
        self.objects = objects
        self.time_since_last_object_creation = time.time()
        self.physics_evaluator = PhysicsEvaluator()
        self.phys_world = PhysWorld()

        self.default_object = Circle(color=RED, mass=10, radius=10)
        self.player_chosen_mass = 10
        self.player_chosen_shape = Circle
        self.player_chosen_radius = 10
        self.player_chosen_color = RED
        self.player_chosen_x = 0
        self.player_chosen_y = 0
        pass

    def parse_mouse_click(self, mouse_pos: Vector2D):
        if mouse_pos.x > ORIGIN[0] and mouse_pos.y > ORIGIN[1]:
            self.create_object(mouse_pos)

    def step(self, delta_time: float):
        self.update_all_vertices()
        for obj in self.objects:
            # TODO: Fixa +=
            obj.update_velocity(delta_time)
            obj.update_position(delta_time)

    def update_all_vertices(self):
        for obj in self.objects:
            if isinstance(obj, Circle):
                continue
            obj.update_vertices()

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)

    def add_objects(self, objs: [PhysObj]):
        for obj in objs:
            self.objects.append(obj)

    def create_object(
        self, position: Vector2D = None, obj: PhysObj = "circle", with_gravity=False
    ):
        if not (
            time.time() - self.time_since_last_object_creation > 0.1
        ):  # Kollar om det gått 0.1 sekunder sedan senaste objektet skapades
            return
        if obj == "circle":
            obj = Circle(
                mass=self.player_chosen_mass,
                radius=self.player_chosen_radius,
                color=self.player_chosen_color,
                position=position
                if position is not None
                else Vector2D(self.player_chosen_x, self.player_chosen_y)
                + Vector2D(*ORIGIN),
            )
        self.add_objects([obj])
        self.time_since_last_object_creation = time.time()
        if with_gravity:
            self.impose_gravity(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)

    # TODO Möjligtvis flytta fysikfunktioner till egen klass

    def handle_collisions(self):
        collisions = self.phys_world.find_collisions(self.objects)
        for collision in collisions:
            self.physics_evaluator.analyze_and_handle_collision(
                collision[0], collision[1]
            )

    def impose_gravity(self, obj: PhysObj):
        obj.add_force(Vector2D(0, GRAVITY_CONSTANT) * obj.mass)

    def longest_axis(self, bounding_box):
        x_length = bounding_box[1][0] - bounding_box[0][0]
        y_length = bounding_box[1][1] - bounding_box[0][1]  # BUGG: längden blir negativ

        if x_length > y_length:
            return 0
        else:
            return 1

    def dot_product(self, vector_a, vector_b):
        return vector_a.x * vector_b.x + vector_a.y * vector_b.y

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def check_collisions(self):
        for obj in self.objects:
            for other_obj in self.objects:
                if obj == other_obj:
                    continue
                if obj.is_inside_of(other_obj):
                    self.resolve_collision(obj, other_obj)
