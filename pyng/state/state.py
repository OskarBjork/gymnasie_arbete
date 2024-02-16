from pyng.space.interface.view_model import relative_to_origin
from pyng.space.vectors import Vector2D
from pyng.config import (
    ORIGIN,
    RED,
    LIGHT_BLUE,
    GRAVITY_CONSTANT,
    COLORS,
    OBJECT_CREATION_COOLDOWN,
    ORANGE,
    GLOBAL_ELASTICITY,
    OUTLINE_SIZE,
    OUTLINE_TEAL,
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
        self.player_chosen_radius = 10
        self.player_chosen_color = RED
        self.player_chosen_x = 0
        self.player_chosen_y = 0
        self.player_force = Vector2D(0, 0)
        self.player_velocity = Vector2D(0, 0)
        self.player_teleport_coordinates = Vector2D(0, 0)
        self.is_paused = False
        self.min_iterations = 1
        self.max_iterations = 128
        self.spawn_gravity = False #User toggleable, Motivering ifall otydligt: "spawn_gravity" pga att gravitationen hos nya objekt som spawnas påverkas av den 
        pass

    def parse_mouse_click(self, mouse_pos: Vector2D, view_model):
        if mouse_pos.x > ORIGIN[0] and mouse_pos.y > ORIGIN[1]:
            if view_model.ui_mode == True:  # om man är i "spawn" läge
                self.create_object(position=mouse_pos)

            else: # om man är i manipulate läge
                selected_object = self.find_object(position=mouse_pos)
                if not selected_object == False: # Om ett objekt hittades
                    view_model.selected_object = selected_object
                    view_model.update_object_info()

    def find_object(self, position):
        for object in self.objects:
            object.calculate_bounding_box
            if ( # AABB med musen
                object.aabb.min.x < position.x < object.aabb.max.x 
                and object.aabb.min.y < position.y < object.aabb.max.y
            ):
                return object
        return False # om inget objekt hittades

    def step(self, delta_time: float, iterations=1):
        iterations = max(self.min_iterations, iterations)

        for _ in range(iterations):
            self.update_all_vertices()
            for obj in self.objects:
                obj.calculate_bounding_box()
                # TODO: Fixa +=
                obj.step(delta_time, iterations)
                if not obj.is_static:
                    # obj.force = Vector2D(0, GRAVITY_CONSTANT * obj.mass)
                    pass
                

                # NOTE: Väggarna runt skärmen. Tog bort för experiment
                # if obj.position.y > 1000 + ORIGIN[1]:
                #     obj.velocity.y = -obj.velocity.y * GLOBAL_ELASTICITY
                #     obj.position.y = 1000 + ORIGIN[1]
                # if obj.position.x > 1500 + ORIGIN[0]:
                #     obj.velocity.x = -obj.velocity.x * GLOBAL_ELASTICITY
                #     obj.position.x = 1500 + ORIGIN[0]
                # if obj.position.y < ORIGIN[1]:
                #     obj.velocity.y = -obj.velocity.y * GLOBAL_ELASTICITY
                #     obj.position.y = ORIGIN[1]
                # if obj.position.x < ORIGIN[0]:
                #     obj.velocity.x = -obj.velocity.x * GLOBAL_ELASTICITY
                #     obj.position.x = ORIGIN[0]


            
                # if (
                #     obj.position.y > 2000
                #     or obj.position.x > 2000
                #     or obj.position.y < ORIGIN[1]
                #     or obj.position.x < ORIGIN[0]
                # ):
                #     pass

            self.handle_collisions()

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
                    width=50,
                    height=50,
                )

        self.add_objects([obj])
        self.time_since_last_object_creation = time.time()
        if with_gravity or self.spawn_gravity:
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
            circle = Circle(color=ORANGE, mass=10, position=point, radius=10)
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

    def generate_random_object(self, type_of_object: str, scale=1):
        if type_of_object == "circle":
            radius = random.randint(10, 100)
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
                            random.randint(-100, 100) * scale,
                            random.randint(-100, 100) * scale,
                        ),
                    ),
                ]
            )
        elif type_of_object == "polygon":
            side_length = random.randint(10, 100)
            self.add_objects(
                [
                    Rectangle(
                        color=random.choice(COLORS),
                        mass=side_length,
                        # mass=10,
                        width=side_length,
                        height=side_length,
                        # velocity=Vector2D(
                        #     random.randint(-300, 300), random.randint(-300, 300)
                        # ),
                        position=Vector2D(
                            random.randint(100, 1000), random.randint(100, 1000)
                        )
                        + Vector2D(*ORIGIN),  # NOTE: Galen indentation
                        velocity=Vector2D(
                            random.randint(-100, 100) * scale,
                            random.randint(-100, 100) * scale,
                        ),
                        angle=random.randint(0, 360) * (math.pi / 180),
                    )
                ],
            )

    def generate_test_data(self, scale=1):
        for _ in range(20):
            type_of_object = random.choice(["polygon", "circle"])
            self.generate_random_object(type_of_object, scale)

    def change_selected_object_attribute(self, type):
        # kollar först ifall ett objekt är valt
        if not self.view_model.selected_object is None:
            match type:
                case "set":
                    match self.view_model.tool:
                        #går inte att skriva self.view_model.selected_object.force = self.player_force för de är objekt
                        case "force":
                            self.view_model.selected_object.force.x = self.player_force.x
                            self.view_model.selected_object.force.y = self.player_force.y
                        case "velocity":
                            self.view_model.selected_object.velocity.x = self.player_velocity.x
                            self.view_model.selected_object.velocity.y = self.player_velocity.y
                case "add":
                    match self.view_model.tool:
                        case "force":
                            self.view_model.selected_object.force = self.view_model.selected_object.force + self.player_force
                        case "velocity":
                            self.view_model.selected_object.velocity = self.view_model.selected_object.velocity + self.player_velocity
                case "teleport":
                    self.view_model.selected_object.position.x = self.player_teleport_coordinates.x + ORIGIN[0]
                    self.view_model.selected_object.position.y = self.player_teleport_coordinates.y + ORIGIN[1]

    def reset_manipulate_data(self):
        self.player_force = Vector2D(0, 0)
        self.player_velocity = Vector2D(0, 0)
        self.player_teleport_coordinates = Vector2D(0, 0)