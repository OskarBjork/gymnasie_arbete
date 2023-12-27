from pyng.space.vectors import Vector2D
from pyng.config import ORIGIN, RED, GRAVITY_CONSTANT, COLORS, OBJECT_CREATION_COOLDOWN
from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon, Rectangle
from pyng.state.physics_evaluator import PhysicsEvaluator
from pyng.state.phys_world import PhysWorld

import math
import time
import pprint
import random

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
        self.player_chosen_tool = "force"
        self.player_chosen_radius = 10
        self.player_chosen_color = RED
        self.player_chosen_x = 0
        self.player_chosen_y = 0
        pass

    def parse_mouse_click(self, mouse_pos: Vector2D, view_model):
        if mouse_pos.x > ORIGIN[0] and mouse_pos.y > ORIGIN[1]:
            if view_model.ui_mode == True:  # om man är i "spawn" läge
                self.create_object(mouse_pos)
            # if view_model.ui_mode == True: #om man är i "spawn" läge, måste få tillgång till ui_mode på nåt sätt
            self.create_object(position=mouse_pos)

    def step(self, delta_time: float):
        self.update_all_vertices()
        for obj in self.objects:
            # TODO: Fixa +=
            obj.update_velocity(delta_time)
            obj.update_position(delta_time)
            if not obj.is_static:
                obj.force = Vector2D(0, GRAVITY_CONSTANT * obj.mass)
                pass
            if (
                obj.position.y > 2000
                or obj.position.x > 2000
                or obj.position.y < ORIGIN[1]
                or obj.position.x < ORIGIN[0]
            ):
                # self.del_object(obj)
                pass

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

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)

    def del_all_objects(self):
        self.objects = []
   
  
    def create_object(self, position=None, obj_type="circle", with_gravity=False):
        if (
            not self.object_creation_available()
        ):  # Kollar om det gått 0.1 sekunder sedan senaste objektet skapades
            return
        obj = None

        match obj_type:
            case "circle":
                obj = Circle(
                    color=RED,
                    mass=10,
                    position=position,
                    radius=self.player_chosen_radius,
                )

        self.add_objects([obj])
        self.time_since_last_object_creation = time.time()
        if with_gravity:
            self.physics_evaluator.impose_gravity(obj)

    def handle_collisions(self):
        collisions = self.phys_world.find_collisions(self.objects)
        for collision in collisions:
            self.physics_evaluator.analyze_and_handle_collision(
                collision[0], collision[1]
            )

    def object_creation_available(self):
        return (
            time.time() - self.time_since_last_object_creation
            > OBJECT_CREATION_COOLDOWN
        )

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
            self.add_objects(
                [
                    Circle(
                        color=random.choice(COLORS),
                        mass=random.randint(1, 100),
                        radius=random.randint(1, 100),
                        # velocity=Vector2D(
                        #     random.randint(-300, 300), random.randint(-300, 300)
                        # ),
                        position=Vector2D(
                            random.randint(100, 1000), random.randint(100, 1000)
                        )
                        + Vector2D(*ORIGIN),  # NOTE: Galen indentation
                    ),
                ]
            )
        elif type_of_object == "polygon":
            self.add_objects(
                [
                    ConvexPolygon(
                        color=random.choice(COLORS),
                        mass=random.randint(1, 100),
                        num_of_sides=random.randint(3, 10),
                        side_length=random.randint(1, 100),
                        # velocity=Vector2D(
                        #     random.randint(-300, 300), random.randint(-300, 300)
                        # ),
                        position=Vector2D(
                            random.randint(100, 1000), random.randint(100, 1000)
                        )
                        + Vector2D(*ORIGIN),  # NOTE: Galen indentation
                    )
                ],
            )

    def generate_test_data(self):
        for _ in range(20):
            type_of_object = random.choice(["circle", "polygon"])
            self.generate_random_object(type_of_object)
