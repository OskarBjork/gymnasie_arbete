from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import Vector2D
from pyng.config import ORIGIN, RED, GRAVITY_CONSTANT
from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon
import time
import math
import pprint

pp = pprint.PrettyPrinter(indent=4)


class BVHNode:
    def __init__(self, objects):
        self.left = None
        self.right = None
        self.objects = objects
        self.bounding_box = self.calculate_bounding_box(objects)

    def calculate_bounding_box(self, objects):
        if not objects:
            return None

        if len(objects) == 1:
            polygon = objects[0]
            min_x = min(v[0] for v in polygon.vertices)
            max_x = max(v[0] for v in polygon.vertices)
            min_y = min(v[1] for v in polygon.vertices)
            max_y = max(v[1] for v in polygon.vertices)
            return [(min_x, min_y), (max_x, max_y)]

        bounding_box = [(float("inf"), float("inf")), (float("-inf"), float("-inf"))]
        for polygon in objects:
            for vertex in polygon.vertices:
                bounding_box[0] = (
                    min(bounding_box[0][0], vertex[0]),
                    min(bounding_box[0][1], vertex[1]),
                )
                bounding_box[1] = (
                    max(bounding_box[1][0], vertex[0]),
                    max(bounding_box[1][1], vertex[1]),
                )

        return bounding_box


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
        self.update_all_vertices()
        for obj in self.objects:
            # TODO: Fixa +=
            obj.update_velocity(delta_time)
            obj.update_position(delta_time)

    def update_all_vertices(self):
        for obj in self.objects:
            obj.update_vertices()

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
        root_node = self.build_bvh(self.objects)
        potential_collision_nodes = self.find_leaf_nodes_with_two_objects(root_node)
        # print(potential_collision_nodes)
        for node in potential_collision_nodes:
            objects = potential_collision_nodes["objects"]
        pass

    def build_bvh(self, objects, depth=0, max_depth=20):
        if len(objects) == 0:
            return None

        if len(objects) == 1:
            return {
                "objects": [objects[0]],
                "bounding_box": self.calculate_bounding_box(objects),
                "left": None,
                "right": None,
            }

        if depth >= max_depth:
            return {
                "objects": objects,
                "bounding_box": self.calculate_bounding_box(objects),
                "left": None,
                "right": None,
            }

        bounding_box = self.calculate_bounding_box(objects)

        if len(objects) == 2:
            left_objects = [objects[0]]
            right_objects = [objects[1]]
        else:
            left_objects, right_objects = self.partition_objects(objects, bounding_box)

        left_child = self.build_bvh(left_objects, depth + 1, max_depth)
        right_child = self.build_bvh(right_objects, depth + 1, max_depth)

        return {
            "objects": objects,
            "bounding_box": bounding_box,
            "left": left_child,
            "right": right_child,
        }

    def calculate_bounding_box(self, objects):
        if not objects:
            return None

        if len(objects) == 1:
            polygon = objects[0]
            min_x = min(v.x for v in polygon.vertices)
            max_x = max(v.x for v in polygon.vertices)
            min_y = min(v.y for v in polygon.vertices)
            max_y = max(v.y for v in polygon.vertices)
            return [(min_x, min_y), (max_x, max_y)]

        bounding_box = [(float("inf"), float("inf")), (float("-inf"), float("-inf"))]
        for polygon in objects:
            for vertex in polygon.vertices:
                bounding_box[0] = (
                    min(bounding_box[0][0], vertex.x),
                    min(bounding_box[0][1], vertex.y),
                )
                bounding_box[1] = (
                    max(bounding_box[1][0], vertex.x),
                    max(bounding_box[1][1], vertex.y),
                )

        return bounding_box

    def partition_objects(self, objects, bounding_box):
        axis = self.longest_axis(bounding_box)
        midpoint = (bounding_box[axis][0] + bounding_box[axis][1]) / 2

        left_objects = []
        right_objects = []

        for obj in objects:
            if obj.bounding_box[axis][1] < midpoint:
                left_objects.append(obj)
            elif obj.bounding_box[axis][0] > midpoint:
                right_objects.append(obj)
            else:
                left_objects.append(obj)
                right_objects.append(obj)

        if len(left_objects) == 0:
            left_objects = right_objects[: len(right_objects) // 2]
            right_objects = right_objects[len(right_objects) // 2 :]
        elif len(right_objects) == 0:
            right_objects = left_objects[: len(left_objects) // 2]
            left_objects = left_objects[len(left_objects) // 2 :]

        return left_objects, right_objects

    def longest_axis(bounding_box):
        x_length = bounding_box[0][1] - bounding_box[0][0]
        y_length = bounding_box[1][1] - bounding_box[1][0]
        z_length = bounding_box[2][1] - bounding_box[2][0]

        if x_length > y_length and x_length > z_length:
            return 0
        elif y_length > z_length:
            return 1
        else:
            return 2

    def projection(polygon, axis):
        """Går igenom alla vertices i ett objekt och projicerar dem på en axel, och returnerar sedan minsta och största värdena av dessa"""
        min_proj = float("inf")
        max_proj = float("-inf")
        for vertex in polygon.vertices:
            dot_product = vertex[0] * axis[0] + vertex[1] * axis[1]
            min_proj = min(min_proj, dot_product)
            max_proj = max(max_proj, dot_product)
        return min_proj, max_proj

    def overlaps(projection1, projection2):
        """Kollar om två projektioner överlappar varandra, utifrån deras minsta och största värden"""
        return projection1[1] >= projection2[0] and projection1[0] <= projection2[1]

    def find_leaf_nodes_with_two_objects(self, root):
        leaf_nodes = []

        if root is None:
            return leaf_nodes
        if root["left"] is None and root["right"] is None and len(root["objects"]) == 2:
            leaf_nodes.append(root)
        else:
            left_leaf_nodes = self.find_leaf_nodes_with_two_objects(root["left"])
            right_leaf_nodes = self.find_leaf_nodes_with_two_objects(root["right"])
            leaf_nodes.extend(left_leaf_nodes)
            leaf_nodes.extend(right_leaf_nodes)

        return leaf_nodes

    def get_normals(polygon):
        # Get the normals of the edges of a convex polygon
        normals = []
        for i in range(len(polygon.vertices)):
            v1 = polygon.vertices[i]
            v2 = polygon.vertices[
                (i + 1) % len(polygon.vertices)
            ]  # Ser till så att sista och första vertex jämförs
            edge = (v2[0] - v1[0], v2[1] - v1[1])
            length = math.sqrt(edge[0] ** 2 + edge[1] ** 2)
            normal = (edge[1] / length, -edge[0] / length)  # Perpendicular vector
            normals.append(normal)
        return normals

    def check_collision(self, polygon1, polygon2):
        """Går igenom alla normaler till båda polygonerna och projicerar alla vertexer på dessa, och kollar sedan om de överlappar varandra"""
        normals1 = self.get_normals(polygon1)
        normals2 = self.get_normals(polygon2)

        for normal in normals1 + normals2:
            projection1 = self.projection(polygon1, normal)
            projection2 = self.projection(polygon2, normal)

            if not self.overlaps(projection1, projection2):
                return False  # Separating axis found

        return True  # No separating axis found, polygons overlap

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

        elif obj.isinstance(Circle) and other_obj.isinstance(ConvexPolygon):
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
