from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import Vector2D
from pyng.config import ORIGIN, RED, GRAVITY_CONSTANT
from pyng.space.phys_obj import PhysObj, Circle, Rectangle
import time
import math


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

    def find_collisions(self):
        points = [
            (obj.position.x, obj.position.y)
            if isinstance(obj, Circle)
            else (obj.position.x + obj.width / 2, obj.position.y + obj.height / 2)
            for obj in self.objects
        ]
        kd_tree = self.build_kd_tree(points)
        collisions = self.find_all_leaves_with_two_points(kd_tree)
        print(len(collisions))

    def build_kd_tree(self, points, depth=0, k=2):
        n = len(points)
        if n <= 0:
            return None
        axis = depth % k
        sorted_points = sorted(points, key=lambda point: point[axis])
        median = n // 2

        return {
            "point": sorted_points[median],
            "left": self.build_kd_tree(points=sorted_points[:median], depth=depth + 1),
            "right": self.build_kd_tree(
                points=sorted_points[median + 1 :], depth=depth + 1
            ),
        }

    def find_all_leaves_with_two_points(self, root):
        if root is None:
            return []
        elif root["left"] is None and root["right"] is None:
            return [root]
        else:
            return self.find_all_leaves_with_two_points(
                root["left"]
            ) + self.find_all_leaves_with_two_points(root["right"])

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def closer_distance(self, pivot, p1, p2):
        if p1 is None:
            return p2
        if p2 is None:
            return p1

        d1 = self.distance(pivot, p1)
        d2 = self.distance(pivot, p2)

        if d1 < d2:
            return p1
        else:
            return p2

    def kd_tree_closest_point(self, root, point, depth=0, k=2):
        if root is None:
            return None

        axis = depth % k
        next_branch = None
        opposite_branch = None

        if point[axis] < root["point"][axis]:
            next_branch = root["left"]
            opposite_branch = root["right"]
        else:
            next_branch = root["right"]
            opposite_branch = root["left"]

        best = self.closer_distance(
            point,
            self.kd_tree_closest_point(next_branch, point, depth + 1),
            root["point"],
        )

        if self.distance(point, best) > abs(point[axis] - root["point"][axis]):
            best = self.closer_distance(
                point,
                self.kd_tree_closest_point(opposite_branch, point, depth + 1),
                best,
            )

        return best

    def check_collisions(self):
        for obj in self.objects:
            for other_obj in self.objects:
                if obj == other_obj:
                    continue
                if obj.is_inside_of(other_obj):
                    self.resolve_collision(obj, other_obj)

    def resolve_collision(self, obj: PhysObj, other_obj: PhysObj):
        if isinstance(obj, Circle) and isinstance(obj, Circle):
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
