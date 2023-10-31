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

    def add_objects(self, objs: [PhysObj]):
        for obj in objs:
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
        # pp.pprint(root_node)
        potential_collision_nodes = self.find_leaf_nodes_with_two_objects(root_node)
        # print(len(potential_collision_nodes))
        for node in potential_collision_nodes:
            object1 = node["objects"][0]
            object2 = node["objects"][1]
            print([obj.id for obj in node["objects"]])
            # print(f"object1: {object1.id}")
            # print(f"object2: {object2.id}")
            if self.check_collision(object1, object2):
                print("COLLISION")

    def build_bvh(self, objects, depth=0, max_depth=20, k=2):
        if len(objects) == 0:
            return None

        if len(objects) == 1:
            return {
                "objects": objects,
                "bounding_box": self.calculate_bounding_box(objects),
                "left": None,
                "right": None,
            }

        if len(objects) == 2:
            return {
                "objects": objects,
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
            left_objects, right_objects, k = self.partition_objects(
                objects, bounding_box, k=k
            )

        left_child = self.build_bvh(left_objects, depth + 1, max_depth, k=k)
        right_child = self.build_bvh(right_objects, depth + 1, max_depth, k=k)

        # print("LEFT CHILD: ")
        # pp.pprint(left_child)
        # print("RIGHT CHILD: ")
        # pp.pprint(right_child)

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

    def partition_objects(self, objects, bounding_box, k=2):
        # print("new objects: ")
        axis = self.longest_axis(bounding_box)
        objects_sorted_along_axis = sorted(
            objects, key=lambda obj: obj.position.x if axis == 0 else obj.position.y
        )
        # print(
        #     [
        #         obj.position.x if axis == 0 else obj.position.y
        #         for obj in objects_sorted_along_axis
        #     ]
        # )
        median = objects_sorted_along_axis[len(objects_sorted_along_axis) // 2]
        median_position_in_axis = median.position.x if axis == 0 else median.position.y
        # print(f"median: {median.id}")
        # print("axis: ", axis)

        left_objects = []
        right_objects = []

        for obj in objects:
            obj.bounding_box = obj.calculate_polygon_bounding_box()
            obj_position_in_axis = obj.position.x if axis == 0 else obj.position.y
            if obj_position_in_axis < median_position_in_axis:
                # print(f"obj: {obj.id} is left of median")
                left_objects.append(obj)
            elif obj_position_in_axis > median_position_in_axis:
                # print(f"obj: {obj.id} is right of median")
                right_objects.append(obj)
            else:
                # print(f"obj: {obj.id} is on median")
                if len(objects) == 3:
                    d1 = self.distance(
                        (objects[0].position.x, objects[0].position.y),
                        (median.position.x, median.position.y),
                    )
                    d2 = self.distance(
                        (objects[2].position.x, objects[2].position.y),
                        (median.position.x, median.position.y),
                    )
                    if d1 < d2:
                        left_objects.append(obj)
                    elif d2 < d1:
                        right_objects.append(obj)
                    else:
                        left_objects.append(obj)
                        right_objects.append(obj)
                    pass
                left_objects.append(obj)

        # print(f"Right objects: {len(right_objects)}")
        # print(f"Left objects: {len(left_objects)}")

        if len(left_objects) == 0:
            left_objects = right_objects[: len(right_objects) // 2]
            right_objects = right_objects[len(right_objects) // 2 :]
        elif len(right_objects) == 0:
            right_objects = left_objects[: len(left_objects) // 2]
            left_objects = left_objects[len(left_objects) // 2 :]

        k += 1

        return left_objects, right_objects, k

    def longest_axis(self, bounding_box):
        x_length = bounding_box[0][1] - bounding_box[0][0]
        y_length = bounding_box[1][1] - bounding_box[1][0]

        if x_length > y_length:
            return 0
        else:
            return 1

    def projection(self, polygon, axis):
        """Går igenom alla vertices i ett objekt och projicerar dem på en axel, och returnerar sedan minsta och största värdena av dessa"""
        min_proj = float("inf")
        max_proj = float("-inf")
        for vertex in polygon.vertices:
            dot_product = vertex.x * axis.x + vertex.y * axis.y
            min_proj = min(min_proj, dot_product)
            max_proj = max(max_proj, dot_product)
        return min_proj, max_proj

    def overlaps(self, projection1, projection2):
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

    def get_normals(self, polygon):
        # Get the normals of the edges of a convex polygon
        normals = []
        for i in range(len(polygon.vertices)):
            v1 = polygon.vertices[i]
            v2 = polygon.vertices[
                (i + 1) % len(polygon.vertices)
            ]  # Ser till så att sista och första vertex jämförs
            edge = Vector2D(v2.x - v1.x, v2.y - v1.y)
            length = math.sqrt(edge.x**2 + edge.y**2)
            normal = Vector2D(edge.x / length, -edge.y / length)  # Perpendicular vector
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
