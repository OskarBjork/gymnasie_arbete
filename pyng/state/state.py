from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import Vector2D
from pyng.config import ORIGIN, RED, GRAVITY_CONSTANT
from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon
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
            if isinstance(obj, Circle):
                continue
            obj.update_vertices()

    def add_object(self, obj: PhysObj):
        self.objects.append(obj

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
        self.add_objects([obj])
        self.time_since_last_object_creation = time.time()
        if with_gravity:
            self.impose_gravity(obj)

    def del_object(self, obj: PhysObj):
        self.objects.remove(obj)

    # TODO Möjligtvis flytta fysikfunktioner till egen klass

    def impose_gravity(self, obj: PhysObj):
        obj.add_force(Vector2D(0, GRAVITY_CONSTANT) * obj.mass)

    def find_collisions(self):
        print("\nNEW FRAME:\n")
        # root_node = self.build_bvh(self.objects)
        # print("ROOT NODE: ")
        # pp.pprint(root_node)
        # potential_collision_nodes = self.find_leaf_nodes_with_two_objects(root_node)
        potential_collisions = self.sweep_and_prune()

        for object1, object2 in potential_collisions:
            print([obj.id for obj in [object1, object2]])
            collision_result = self.check_collision(object1, object2)
            if collision_result[0]:
                print("COLLISION: ", [obj.id for obj in [object1, object2]])
                # self.resolve_collision(object1, object2)
                # print("COLLISION: ", [obj.id for obj in node["objects"]])
                object1.position = object1.position - collision_result[1] / 2
                object2.position = object2.position + collision_result[1] / 2
        # print(len(potential_collision_nodes))
        # print("POTENTIAL COLLISION NODES: ")
        # pp.pprint(potential_collision_nodes)
        # pp.pprint(self.objects)
        # print("POTENTIAL COLLISIONS: ")
        # for node in potential_collision_nodes:
        #     object1 = node["objects"][0]
        #     object2 = node["objects"][1]
        #     # if object1 == object2:
        #     #     continue
        #     # print("POSSIBLE COLLISION: ")
        #     print([obj.id for obj in node["objects"]])
        #     # print(f"object1: {object1.id}")
        #     # print(f"object2: {object2.id}")
        #     if self.check_collision(object1, object2):
        #         print("COLLISION: ", [obj.id for obj in node["objects"]])

    def sweep_and_prune(self):
        projections_x, projections_y = self.get_projections_in_x_and_y_plane()
        # print("PROJECTIONS X: ")
        # pp.pprint(projections_x)
        # print("PROJECTIONS Y: ")
        # pp.pprint(projections_y)
        potential_collisions = []
        for i, tup in enumerate(projections_x):
            points = tup[0], tup[1]
            for j, other_tup in enumerate(projections_x):
                if tup == other_tup:
                    continue
                other_points = other_tup[0], other_tup[1]
                if self.overlaps(points, other_points) and self.overlaps(
                    projections_y[i], projections_y[j]
                ):
                    potential_collisions.append((tup[2], other_tup[2]))

        return self.remove_duplicates(potential_collisions)

    def remove_duplicates(self, potential_collisions):
        unique_collisions = set(
            frozenset(collision) for collision in potential_collisions
        )
        return [tuple(collision) for collision in unique_collisions]

    def get_projections_in_x_and_y_plane(self):
        projections_x = []
        projections_y = []
        objects = [obj for obj in self.objects if not isinstance(obj, Circle)]
        for axis in (
            Vector2D(1, 0),
            Vector2D(0, 1),
        ):
            for obj in objects:
                min_proj, max_proj = self.projection(obj, axis)
                if axis.x == 1:
                    projections_x.append((min_proj, max_proj, obj))
                else:
                    projections_y.append((min_proj, max_proj, obj))

        return projections_x, projections_y

    def build_bvh(self, objects, depth=0, max_depth=20, k=2):
        objects = list(set(objects))

        print("NEW BUILD BVH")
        print([obj.id for obj in objects])

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
            if not isinstance(polygon, ConvexPolygon):
                continue
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
        print("new objects: ")
        axis = self.longest_axis(bounding_box)
        objects_sorted_along_axis = sorted(
            objects, key=lambda obj: obj.position.x if axis == 0 else obj.position.y
        )

        median = objects_sorted_along_axis[len(objects_sorted_along_axis) // 2]
        median_position_in_axis = median.position.x if axis == 0 else median.position.y
        print([obj.id for obj in objects_sorted_along_axis])
        print(
            [
                obj.position.x if axis == 0 else obj.position.y
                for obj in objects_sorted_along_axis
            ]
        )
        print(f"median: {median.id}")
        print("axis: ", axis)

        left_objects = []
        right_objects = []

        for index, obj in enumerate(objects_sorted_along_axis):
            obj.update_vertices()
            # if obj.id == "orange":
            #     print(obj.position)
            obj.bounding_box = obj.calculate_polygon_bounding_box()
            # if obj.id == "orange":
            #     print(obj.vertices)

            if len(objects) == 3:
                print("THREE OBJECTS")
                # print(objects_sorted_along_axis[0].id)
                # print(objects_sorted_along_axis[2].id)
                d1 = self.distance(
                    (
                        objects_sorted_along_axis[0].position.x,
                        objects_sorted_along_axis[0].position.y,
                    ),
                    (median.position.x, median.position.y),
                )
                d2 = self.distance(
                    (
                        objects_sorted_along_axis[2].position.x,
                        objects_sorted_along_axis[2].position.y,
                    ),
                    (median.position.x, median.position.y),
                )
                # print(f"d1: {d1}")
                # print(f"d2: {d2}")
                if d1 < d2:
                    left_objects.append(objects_sorted_along_axis[0])
                    left_objects.append(median)
                    print([obj.id for obj in left_objects])
                elif d1 > d2:
                    right_objects.append(objects_sorted_along_axis[2])
                    right_objects.append(median)
                    print([obj.id for obj in right_objects])
                else:
                    left_objects.append(obj)
                    right_objects.append(obj)
                break

            obj_position_in_axis = obj.position.x if axis == 0 else obj.position.y
            if obj_position_in_axis < median_position_in_axis:
                print(f"obj: {obj.id} is left of median")
                left_objects.append(obj)
            elif obj_position_in_axis > median_position_in_axis:
                print(f"obj: {obj.id} is right of median")
                right_objects.append(obj)
            else:
                print(f"obj: {obj.id} is on median")
                right_objects.append(obj)
                left_objects.append(obj)
                # if obj != median:
                #     left_objects.append(obj)

        # print(f"Right objects: {len(right_objects)}")
        # print(f"Left objects: {len(left_objects)}")

        if len(left_objects) == 0 and len(objects) > 3:
            left_objects = right_objects[: len(right_objects) // 2]
            right_objects = right_objects[len(right_objects) // 2 :]
        elif len(right_objects) == 0 and len(objects) > 3:
            right_objects = left_objects[: len(left_objects) // 2]
            left_objects = left_objects[len(left_objects) // 2 :]

        k += 1

        return left_objects, right_objects, k

    def longest_axis(self, bounding_box):
        x_length = bounding_box[1][0] - bounding_box[0][0]
        y_length = bounding_box[1][1] - bounding_box[0][1]  # BUGG: längden blir negativ

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
            # print("Vertex: ", vertex)
            # print("Axis: ", axis)
            # print("Projection: ", dot_product)
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
        normals = []
        for i in range(len(polygon.vertices)):
            v1 = polygon.vertices[i]
            v2 = polygon.vertices[(i + 1) % len(polygon.vertices)]
            edge = Vector2D(v2.x - v1.x, v2.y - v1.y)
            length = math.sqrt(edge.x**2 + edge.y**2)
            normal = Vector2D(
                round(-edge.y / length, 5), round(edge.x / length, 5)
            )  # Perpendicular vector
            normals.append(normal)
        return normals

    def check_collision(self, polygon1, polygon2):
        """Går igenom alla normaler till båda polygonerna och projicerar alla vertexer på dessa, och kollar sedan om de överlappar varandra"""
        normals1 = self.get_normals(polygon1)
        normals2 = self.get_normals(polygon2)

        all_normals = normals1 + normals2

        min_overlap = float("inf")
        smallest_axis = None
        # print(len(all_normals))

        for i, normal in enumerate(all_normals):
            # print("Polygon1: ", polygon1.id + "\n")
            projection1 = self.projection(polygon1, normal)
            # print(f"projection1: {projection1}")
            # print("Polygon2: ", polygon2.id + "\n")
            projection2 = self.projection(polygon2, normal)
            # print(f"projection2: {projection2}\n")

            overlap = self.overlaps(projection1, projection2)

            if not overlap:
                # print("Separating axis found")
                # print(f"normal: {normal}")
                # print(f"projection1: {projection1}")
                # print(f"projection2: {projection2}\n")
                return False, None  # Separating axis found

            overlap_amount = min(projection1[1], projection2[1]) - max(
                projection1[0], projection2[0]
            )

            if overlap_amount < min_overlap:
                min_overlap = overlap_amount
                smallest_axis = normal
        mtv = smallest_axis * min_overlap
        return True, mtv  # No separating axis found, polygons overlap

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def check_collisions(self):
        for obj in self.objects:
            for other_obj in self.objects:
                if obj == other_obj:
                    continue
                if obj.is_inside_of(other_obj):
                    self.resolve_collision(obj, other_obj)

    def resolve_collision(self, obj: PhysObj, other_obj: PhysObj):
        if isinstance(obj, Circle) and isinstance(other_obj, Circle):
            self.resolve_circle_collision(obj, other_obj)

        elif isinstance(obj, ConvexPolygon) and isinstance(other_obj, ConvexPolygon):
            # TODO: Hantera kollision på rätt sätt
            obj.position.x = obj.position.x - obj.velocity.x
            obj.position.y = obj.position.y - obj.velocity.y
            other_obj.position.x = other_obj.position.x - other_obj.velocity.x
            other_obj.position.y = other_obj.position.y - other_obj.velocity.y
        # elif obj.isinstance(Circle) and other_obj.isinstance(ConvexPolygon):
        elif isinstance(obj, Circle) and isinstance(other_obj, ConvexPolygon):
            obj.position.x = obj.position.x - obj.velocity.x
            obj.position.y = obj.position.y - obj.velocity.y
            other_obj.position.x = other_obj.position.x - other_obj.velocity.x
            other_obj.position.y = other_obj.position.y - other_obj.velocity.y

        self.resolve_momentum(obj, other_obj)

    @staticmethod
    def resolve_circle_collision(obj: Circle, other_obj: Circle):
        d = obj.position.distance_to(other_obj.position)

        overlap_length = obj.radius + other_obj.radius - d

        direction = obj.position - other_obj.position

        direction = direction.normalize()

        magnitude = overlap_length / 2

        direction = direction * magnitude

        obj.position = obj.position + direction

        other_obj.position = other_obj.position - direction

    def resolve_momentum(self, obj1, obj2):
        obj1_momentum = obj1.velocity * obj1.mass
        obj2_momentum = obj2.velocity * obj2.mass

        obj1.velocity = obj2_momentum / obj1.mass

        obj2.velocity = obj1_momentum / obj2.mass
