from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import Vector2D
from pyng.config import ORIGIN, RED, GRAVITY_CONSTANT
from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon
import time
import math
import pprint
from dataclasses import dataclass

pp = pprint.PrettyPrinter(indent=2)


@dataclass
class Interval:
    min: float
    max: float


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
        self.player_chosen_x = 0
        self.player_chosen_y = 0

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
                position=position if position is not None else Vector2D(self.player_chosen_x,
                                                                        self.player_chosen_y) + Vector2D(*ORIGIN),
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
        potential_collisions = self.sweep_and_prune()

        for object1, object2 in potential_collisions:
            collision_result = self.check_collision(object1, object2)
            if collision_result[0]:
                object1.position = object1.position - collision_result[1] / 2
                object2.position = object2.position + collision_result[1] / 2

    def sweep_and_prune(self):
        projections_x, projections_y = self.get_projections_in_x_and_y_plane()
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

    def get_normals(self, polygon):
        normals = []
        for i in range(len(polygon.vertices)):
            v1 = polygon.vertices[i]
            v2 = polygon.vertices[(i + 1) % len(polygon.vertices)]
            edge = Vector2D(v2.x - v1.x, v2.y - v1.y)
            length = math.sqrt(edge.x ** 2 + edge.y ** 2)
            normal = Vector2D(
                round(-edge.y / length, 5), round(edge.x / length, 5)
            )  # Perpendicular vector
            normals.append(normal)
        return normals

    # NOTE: axis är (1, 0) för x-axeln och (0, 1) för y-axeln, axis måste vara normaliserad
    @staticmethod
    def get_interval(polygon: ConvexPolygon, axis: Vector2D) -> Interval:
        [(min_x, min_y), (max_x, max_y)] = polygon.calculate_polygon_bounding_box()
        verticies = [Vector2D(min_x, min_y), Vector2D(min_x, max_y),
                     Vector2D(max_x, min_y), Vector2D(max_x, max_y)]

        interval = Interval(axis.dot(verticies[0]), axis.dot(verticies[0]))
        for vertex in verticies:
            projection = axis.dot(vertex)
            if projection < interval.min:
                interval.min = projection
            if projection > interval.max:
                interval.max = projection

        return interval

    # NOTE: axis är (1, 0) för x-axeln och (0, 1) för y-axeln, axis måste vara normaliserad
    @staticmethod
    def overlap_on_axis(polygon1: ConvexPolygon, polygon2: ConvexPolygon,
                        axis: Vector2D
                        ) -> bool:
        interval1 = State.get_interval(polygon1, axis)
        interval2 = State.get_interval(polygon2, axis)

        return interval2.min <= interval1.max and interval1.min <= interval2.max

    """
    def check_collision(self, polygon1, polygon2):
        x_axis = Vector2D(1, 0)
        y_axis = Vector2D(0, 1)
        #mtv = smallest_axis * min_overlap
        return (self.overlap_on_axis(polygon1, polygon2, x_axis)
                or self.overlap_on_axis(polygon1, polygon2, y_axis))

    """

    def check_collision(self, polygon1, polygon2):
        # Går igenom alla normaler till båda polygonerna och projicerar alla vertexer på dessa, och kollar sedan om de överlappar varandra
        normals1 = self.get_normals(polygon1)
        normals2 = self.get_normals(polygon2)

        all_normals = normals1 + normals2

        min_overlap = float("inf")
        smallest_axis = None

        for i, normal in enumerate(all_normals):
            projection1 = self.projection(polygon1, normal)
            projection2 = self.projection(polygon2, normal)

            overlap = self.overlaps(projection1, projection2)

            if not overlap:
                return False, None  # Separating axis found

            min1 = projection1[0]
            max1 = projection1[1]
            min2 = projection2[0]
            max2 = projection2[1]

            axis_depth = min(max2 - min1, max1 - min2)

            if axis_depth < min_overlap:
                min_overlap = axis_depth
                smallest_axis = normal
        min_overlap = min_overlap / (normal.magnitude())
        smallest_axis = smallest_axis.normalize()
        center_1 = self.find_arithmetic_mean(polygon1.vertices)
        center_2 = self.find_arithmetic_mean(polygon2.vertices)
        direction = center_2 - center_1

        if smallest_axis.dot(direction) < 0:
            smallest_axis = Vector2D(-smallest_axis.x, -smallest_axis.y)
        mtv = smallest_axis * min_overlap
        return True, mtv  # No separating axis found, polygons overlap

    def find_arithmetic_mean(self, vertices):
        sum_x = 0
        sum_y = 0
        for v in vertices:
            sum_x += v.x
            sum_y += v.y

        return Vector2D(sum_x / len(vertices), sum_y / len(vertices))

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
