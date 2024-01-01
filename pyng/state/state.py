from pyng.space.interface.view_model import relative_to_origin
from pyng.space.vectors import Vector2D
from pyng.config import (
    ORIGIN,
    RED,
    GRAVITY_CONSTANT,
    COLORS,
    OBJECT_CREATION_COOLDOWN,
    ORANGE,
)
from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon, Rectangle, Point
from pyng.state.physics_evaluator import PhysicsEvaluator
from pyng.state.phys_world import PhysWorld
from pyng.space.interface.view_model import relative_to_origin

import math
import time
import pprint
import random

pp = pprint.PrettyPrinter(indent=2)


class State:
    def __init__(
        self,
        objects: [PhysObj] = [],
        view_model=None,
    ) -> None:
        self.objects = objects
        self.view_model = view_model
        self.time_since_last_object_creation = time.time()
        self.physics_evaluator = PhysicsEvaluator()
        self.phys_world = PhysWorld()

        self.default_object = Circle(color=RED, mass=10, radius=10)
        self.player_chosen_mass = 10
        self.player_chosen_shape = "circle"
        self.player_chosen_tool = "force"
        self.player_chosen_radius = 10
        self.player_chosen_color = RED
        self.player_chosen_x = 0
        self.player_chosen_y = 0
        self.is_paused = False
        pass

    def parse_mouse_click(self, mouse_pos: Vector2D, view_model):
        if mouse_pos.x > ORIGIN[0] and mouse_pos.y > ORIGIN[1]:
            if view_model.ui_mode == True:  # om man är i "spawn" läge
                self.create_object(position=mouse_pos)

    def step(self, delta_time: float):
        self.update_all_vertices()
        for obj in self.objects:
            # TODO: Fixa +=
            obj.update_velocity(delta_time)
            obj.update_position(delta_time)
            if not obj.is_static:
                # obj.force = Vector2D(0, GRAVITY_CONSTANT * obj.mass)
                pass

            if obj.position.y > 1000:
                obj.velocity.y = -obj.velocity.y
            if obj.position.x > 1500:
                obj.velocity.x = -obj.velocity.x
            if obj.position.y < ORIGIN[1]:
                obj.velocity.y = -obj.velocity.y
            if obj.position.x < ORIGIN[0]:
                obj.velocity.x = -obj.velocity.x
            # if (
            #     obj.position.y > 2000
            #     or obj.position.x > 2000
            #     or obj.position.y < ORIGIN[1]
            #     or obj.position.x < ORIGIN[0]
            # ):
            #     pass

    def update_all_vertices(self):
        for obj in self.objects:
            if isinstance(obj, Circle) or isinstance(obj, Point):
                continue
            obj.update_vertices()

    def add_object(self, obj: PhysObj):
        self.objects.append(obj)

    def add_objects(self, objs: [PhysObj]):
        for obj in objs:
            self.objects.append(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)

    def del_all_objects(self):
        self.objects = []

    def create_object(
        self, position=None, obj_type=None, with_gravity=False, manual_spawn=False
    ):
        if (
            not self.object_creation_available(position)
        ):  # Kollar om det gått 0.1 sekunder sedan senaste objektet skapades
            return

        if manual_spawn:
            position = relative_to_origin(
                Vector2D(self.player_chosen_x, self.player_chosen_y)
            )

        if obj_type is None:
            obj_type = self.player_chosen_shape

        obj = None

        match obj_type:
            case "circle":
                obj = Circle(
                    color=RED,
                    mass=self.player_chosen_mass,
                    position=position,
                    radius=self.player_chosen_radius,
                )
            case "rect":
                obj = Rectangle(
                    color=RED,
                    mass=self.player_chosen_mass,
                    position=position,
                    width=100,
                    height=100,
                )

        self.add_objects([obj])
        self.time_since_last_object_creation = time.time()
        if with_gravity:
            self.physics_evaluator.impose_gravity(obj)

    def handle_collisions(self):
        collisions = self.phys_world.find_collisions(self.objects)
        collision_manifolds = []
        for collision in collisions:
            result = self.physics_evaluator.create_collision_manifold(
                collision[0], collision[1]
            )

            if result is not None:
                collision_manifolds.append(result)

        contact_points = []

        for manifold in collision_manifolds:
            self.physics_evaluator.resolve_any_collision(manifold)
            if manifold.contact1 is not None:
                contact_points.append(manifold.contact1)
            if manifold.contact2 is not None:
                contact_points.append(manifold.contact2)

        for point in contact_points:
            circle = Circle(color=ORANGE, mass=10, position=point, radius=20)
            self.view_model.render_circle(circle)

    def object_creation_available(self, creation_request_position):
        if not ( # Kollar om tillräckligt med tid har gått sedan senaste objektet skapats.
            time.time() - self.time_since_last_object_creation
            > OBJECT_CREATION_COOLDOWN
        ):
            return False
        
        # Förhindrar att objektet skapas på samma koordinater som det tidigare, vilket annars skulle resultera i ett AssertionError.    
        if len(self.objects) > 0:
            if creation_request_position is None: # NOTE: Om input från UI   
                if (
                    self.objects[-1].position.x == self.player_chosen_x + ORIGIN[0]
                and self.objects[-1].position.y == self.player_chosen_y + ORIGIN[1]
                ):
                    return False
            else: # NOTE: Om input från mus
                if (
                    self.objects[-1].position.x == creation_request_position.x
                and self.objects[-1].position.y == creation_request_position.y
                ):
                    return False   

        # Om inget False returnas så returnas True istället
        return True

    def generate_random_position(self):
        while True:
            position = Vector2D(
                random.randint(100, 1000), random.randint(100, 1000)
            ) + Vector2D(*ORIGIN)
            circle = Circle(
                color=RED,
                mass=10,
                radius=100,
                position=position,
            )
            for obj in self.objects:
                if isinstance(obj, Circle):
                    if (
                        self.physics_evaluator.check_circle_collision(circle, obj)[0]
                        == True  # NOTE: Galen indentation
                    ):
                        break
                elif isinstance(obj, ConvexPolygon):
                    if (
                        self.physics_evaluator.check_polygon_circle_collision(
                            obj, circle
                        )[0]
                        == True  # NOTE: Galen indentation
                    ):
                        break
            else:
                return position

    def generate_random_object(self, type_of_object: str):
        if type_of_object == "circle":
            radius = random.randint(1, 100)
            self.add_objects(
                [
                    Circle(
                        color=random.choice(COLORS),
                        mass=radius,
                        # mass=10,
                        radius=radius,
                        # velocity=Vector2D(
                        #     random.randint(-300, 300), random.randint(-300, 300)
                        # ),
                        position=Vector2D(
                            random.randint(100, 1000), random.randint(100, 1000)
                        )
                        + Vector2D(*ORIGIN),  # NOTE: Galen indentation
                        velocity=Vector2D(
                            random.randint(-1000, 1000), random.randint(-1000, 1000)
                        ),
                    ),
                ]
            )
        elif type_of_object == "polygon":
            side_length = random.randint(1, 100)
            self.add_objects(
                [
                    ConvexPolygon(
                        color=random.choice(COLORS),
                        mass=side_length,
                        # mass=10,
                        num_of_sides=random.randint(3, 10),
                        side_length=side_length,
                        # velocity=Vector2D(
                        #     random.randint(-300, 300), random.randint(-300, 300)
                        # ),
                        position=Vector2D(
                            random.randint(100, 1000), random.randint(100, 1000)
                        )
                        + Vector2D(*ORIGIN),  # NOTE: Galen indentation
                        velocity=Vector2D(
                            random.randint(-1000, 1000), random.randint(-1000, 1000)
                        ),
                    )
                ],
            )

    def generate_test_data(self):
        for _ in range(20):
            type_of_object = random.choice(["circle", "polygon"])
            self.generate_random_object(type_of_object)
