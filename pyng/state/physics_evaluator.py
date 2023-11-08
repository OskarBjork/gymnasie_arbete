from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon
from pyng.space.vectors import Vector2D
from pyng.helper import projection, overlaps, find_arithmetic_mean, dot_product
from pyng.config import GRAVITY_CONSTANT
import math


class PhysicsEvaluator:
    def __init__(self) -> None:
        pass

    def analyze_and_handle_collision(self, obj: PhysObj, other_obj: PhysObj):
        if isinstance(obj, Circle) and isinstance(other_obj, Circle):
            collision_analysis = self.check_circle_collision(obj, other_obj)
            collision_happened, overlap_length = collision_analysis
            if not collision_happened:
                return
            self.resolve_circle_collision(obj, other_obj, overlap_length)

        elif isinstance(obj, ConvexPolygon) and isinstance(other_obj, ConvexPolygon):
            collision_analysis = self.check_polygon_collision(obj, other_obj)
            collision_happened, mtv = collision_analysis
            if not collision_happened:
                return
            self.resolve_polygon_collision(obj, other_obj, mtv)

        elif isinstance(obj, ConvexPolygon) and isinstance(other_obj, Circle):
            collision_analysis = self.check_polygon_circle_collision(obj, other_obj)
            collision_happened, mtv = collision_analysis
            if not collision_happened:
                return
            self.resolve_polygon_circle_collision(other_obj, obj, mtv)

        elif isinstance(obj, Circle) and isinstance(other_obj, ConvexPolygon):
            collision_analysis = self.check_polygon_circle_collision(obj, other_obj)
            collision_happened, mtv = collision_analysis
            if not collision_happened:
                return
            self.resolve_polygon_circle_collision(obj, other_obj, mtv)

    def resolve_polygon_collision(
        self, obj: ConvexPolygon, other_obj: ConvexPolygon, mtv
    ):
        obj.position = obj.position - (mtv / 2)
        other_obj.position = other_obj.position + (mtv / 2)
        self.collision_response(obj, other_obj, mtv)

    def resolve_circle_collision(self, obj: Circle, other_obj: Circle, overlap_length):
        direction = obj.position - other_obj.position

        direction = direction.normalize()

        magnitude = overlap_length / 2

        direction = direction * magnitude

        obj.position = obj.position + direction

        other_obj.position = other_obj.position - direction
        self.collision_response(obj, other_obj, direction)

    def resolve_polygon_circle_collision(self, circle, polygon, mtv):
        circle.position = circle.position + (mtv / 2)
        polygon.position = polygon.position - (mtv / 2)
        self.collision_response(circle, polygon, mtv)

    def check_circle_collision(self, circle1: Circle, circle2: Circle):
        distance = circle1.position.distance_to(circle2.position)
        return (
            distance < circle1.radius + circle2.radius,
            circle1.radius + circle2.radius - distance,
        )

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

    def check_polygon_collision(self, polygon1, polygon2):
        """Går igenom alla normaler till båda polygonerna och projicerar alla vertexer på dessa, och kollar sedan om de överlappar varandra"""
        normals1 = self.get_normals(polygon1)
        normals2 = self.get_normals(polygon2)

        all_normals = normals1 + normals2

        min_overlap = float("inf")
        smallest_axis = None

        for i, normal in enumerate(all_normals):
            projection1 = projection(polygon1, normal)
            projection2 = projection(polygon2, normal)

            overlap = overlaps(projection1, projection2)

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
        center_1 = polygon1.position
        center_2 = polygon2.position
        direction = center_2 - center_1

        if smallest_axis.dot(direction) < 0:
            smallest_axis = Vector2D(-smallest_axis.x, -smallest_axis.y)
        mtv = smallest_axis * min_overlap
        return True, mtv  # No separating axis found, polygons overlap

    def check_polygon_circle_collision(self, polygon, circle):
        if isinstance(circle, ConvexPolygon) and isinstance(polygon, Circle):
            return self.check_polygon_circle_collision(circle, polygon)
        normals = self.get_normals(polygon)
        min_overlap = float("inf")

        for normal in normals:
            projection1 = polygon.project(normal)
            projection2 = circle.project(normal)

            overlap = overlaps(projection1, projection2)

            min1 = projection1[0]
            max1 = projection1[1]
            min2 = projection2[0]
            max2 = projection2[1]

            axis_depth = min(max2 - min1, max1 - min2)

            if axis_depth < min_overlap:
                min_overlap = axis_depth
                smallest_axis = normal

            if not overlap:
                return False, None

        min_overlap = min_overlap / (normal.magnitude())
        smallest_axis = smallest_axis.normalize()
        center_1 = polygon.position
        center_2 = circle.position
        direction = center_2 - center_1

        if smallest_axis.dot(direction) < 0:
            smallest_axis = Vector2D(-smallest_axis.x, -smallest_axis.y)

        return True, smallest_axis * min_overlap

    def find_closest_point_on_polygon(self, polygon, circle):
        result = -1
        min_dist = float("inf")
        for i, v in enumerate(polygon.vertices):
            dist = v.distance_to(circle.position)
            if dist < min_dist:
                min_dist = dist
                result = i
        return result

    def resolve_momentum(self, obj1, obj2):
        obj1_momentum = obj1.velocity * obj1.mass
        obj2_momentum = obj2.velocity * obj2.mass

        obj1.velocity = obj2_momentum / obj1.mass

        obj2.velocity = obj1_momentum / obj2.mass

    def collision_response(self, obj1, obj2, mtv):
        if mtv.magnitude() == 0:
            return
        mtv = mtv.normalize()
        relative_velocity = obj1.velocity - obj2.velocity
        e = min(obj1.restitution, obj2.restitution)
        j = (
            -(1 + e)
            * relative_velocity.dot(mtv)
            / (mtv.magnitude() ** 2 * (1 / obj1.mass + 1 / obj2.mass))
        )
        obj1.velocity = obj1.velocity + (mtv * (j / obj1.mass))
        obj2.velocity = obj2.velocity - (mtv * (j / obj2.mass))

    def impose_gravity(self, obj: PhysObj):
        obj.add_force(Vector2D(0, GRAVITY_CONSTANT) * obj.mass)
