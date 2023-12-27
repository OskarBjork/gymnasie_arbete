from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon
from pyng.space.vectors import Vector2D
from pyng.helper import (
    projection,
    overlaps,
    find_arithmetic_mean,
    dot_product,
    length_squared,
    distance_squared,
)
from pyng.config import GRAVITY_CONSTANT
from pyng.space.collision import CollisionManifold
import math


class PhysicsEvaluator:
    def __init__(self) -> None:
        pass

    def create_collision_manifold(self, obj: PhysObj, other_obj: PhysObj):
        if obj.is_static and other_obj.is_static:
            return
        collision_analysis = self.check_any_collision(obj, other_obj)
        collision_happened = collision_analysis[0]
        normal = collision_analysis[2]
        displacement = collision_analysis[1]
        if collision_happened:
            contact_points = self.find_contact_points(obj, other_obj)
            manifold = CollisionManifold(
                obj,
                other_obj,
                normal=normal,
                depth=displacement,
                contact1=None,
                contact2=None,
                contact_count=1,
            )
            try:
                manifold.contact1 = contact_points[0]
                manifold.contact_count += 1
            except:
                pass
            try:
                manifold.contact2 = contact_points[1]
                manifold.contact_count += 1
            except:
                pass

            return manifold

        return None

    def check_any_collision(self, obj: PhysObj, other_obj: PhysObj):
        if isinstance(obj, Circle) and isinstance(other_obj, Circle):
            return self.check_circle_collision(obj, other_obj)
        elif isinstance(obj, ConvexPolygon) and isinstance(other_obj, ConvexPolygon):
            return self.check_polygon_collision(obj, other_obj)
        elif isinstance(obj, ConvexPolygon) and isinstance(other_obj, Circle):
            return self.check_polygon_circle_collision(obj, other_obj)
        elif isinstance(obj, Circle) and isinstance(other_obj, ConvexPolygon):
            return self.check_polygon_circle_collision(obj, other_obj)

    def resolve_any_collision(self, manifold: CollisionManifold):
        object1 = manifold.body_A
        object2 = manifold.body_B
        if isinstance(object1, Circle) and isinstance(object2, Circle):
            self.resolve_circle_collision(object1, object2, manifold.depth)
        elif isinstance(object1, ConvexPolygon) and isinstance(object2, ConvexPolygon):
            self.resolve_polygon_collision(object1, object2, manifold.depth)
        elif isinstance(object1, ConvexPolygon) and isinstance(object2, Circle):
            self.resolve_polygon_circle_collision(object2, object1, manifold.depth)
        elif isinstance(object1, Circle) and isinstance(object2, ConvexPolygon):
            self.resolve_polygon_circle_collision(object1, object2, manifold.depth)

    def resolve_polygon_collision(
        self, obj: ConvexPolygon, other_obj: ConvexPolygon, mtv
    ):
        if obj.is_static:
            other_obj.position = other_obj.position + mtv
        elif other_obj.is_static:
            obj.position = obj.position - mtv
        else:
            obj.position = obj.position - (mtv / 2)
            other_obj.position = other_obj.position + (mtv / 2)
        self.collision_response(obj, other_obj, mtv)

    def resolve_circle_collision(self, obj: Circle, other_obj: Circle, overlap_length):
        direction = obj.position - other_obj.position

        if not direction.magnitude() > 0:
            return  # FIXME: Hantera situationen
        direction = direction.normalize()

        magnitude = overlap_length / 2

        direction = direction * magnitude

        if other_obj.is_static:
            obj.position = obj.position + direction
        elif obj.is_static:
            other_obj.position = other_obj.position - direction
        else:
            obj.position = obj.position + direction
            other_obj.position = other_obj.position - direction
        self.collision_response(obj, other_obj, direction)

    def resolve_polygon_circle_collision(self, circle, polygon, mtv):
        if circle.is_static:
            polygon.position = polygon.position - mtv
        elif polygon.is_static:
            circle.position = circle.position + mtv
        else:
            circle.position = circle.position + (mtv / 2)
            polygon.position = polygon.position - (mtv / 2)
        self.collision_response(circle, polygon, mtv)

    def check_circle_collision(self, circle1: Circle, circle2: Circle):
        distance = circle1.position.distance_to(circle2.position)
        return (
            distance < circle1.radius + circle2.radius,
            circle1.radius + circle2.radius - distance,
            (circle1.position - circle2.position).normalize(),
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
        return True, mtv, smallest_axis  # No separating axis found, polygons overlap

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

        return True, smallest_axis * min_overlap, smallest_axis

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

        obj1.velocity = obj2_momentum * obj1.inverse_mass

        obj2.velocity = obj1_momentum * obj2.inverse_mass

    def collision_response(self, obj1, obj2, mtv):
        if mtv.magnitude() == 0:
            return
        mtv = mtv.normalize()
        relative_velocity = obj1.velocity - obj2.velocity
        e = min(obj1.restitution, obj2.restitution)
        j = (
            -(1 + e)
            * relative_velocity.dot(mtv)
            / (mtv.magnitude() ** 2 * (obj1.inverse_mass + obj2.inverse_mass))
        )
        obj1.velocity = obj1.velocity + (mtv * (j * obj1.inverse_mass))
        obj2.velocity = obj2.velocity - (mtv * (j * obj2.inverse_mass))

    def point_segment_distance(self, point, a, b):
        ab = b - a
        ap = point - a

        proj = ap.dot(ab)
        ab_length_squared = length_squared(ab)
        d = proj / ab_length_squared

        if d < 0:
            contact = a
        elif d >= 1:
            contact = b
        else:
            contact = ab * d + a

        distance_squared = length_squared(ap - contact)

        return (distance_squared, contact)

    def impose_gravity(self, obj: PhysObj):
        obj.add_force(Vector2D(0, GRAVITY_CONSTANT) * obj.mass)

    def find_circles_contact_point(self, circle1, circle2):
        ab = circle1.position - circle2.position
        dir = ab.normalize()
        return [
            circle1.position - (dir * circle1.radius)
        ]  # Detta kommer ge tillbaka en punkt på skärmen och inte i världen

    def find_polygon_circle_contact_points(self, polygon, circle):
        min_dist_squared = float("inf")
        closest_contact = None
        for i, vertice in enumerate(polygon.vertices):
            va = vertice
            vb = polygon.vertices[(i + 1) % len(polygon.vertices)]
            distance_squared, contact = self.point_segment_distance(
                circle.position, vb, va
            )
            if distance_squared < min_dist_squared:
                min_dist_squared = distance_squared
                closest_contact = contact

        return [closest_contact]

    def find_contact_points(self, body_A, body_B):
        if isinstance(body_A, Circle) and isinstance(body_B, Circle):
            return self.find_circles_contact_point(body_A, body_B)
        elif isinstance(body_A, ConvexPolygon) and isinstance(body_B, ConvexPolygon):
            # return self.find_polygon_polygon_contact_points(body_A, body_B)
            return None
        elif isinstance(body_A, ConvexPolygon) and isinstance(body_B, Circle):
            return self.find_polygon_circle_contact_points(body_A, body_B)
        elif isinstance(body_A, Circle) and isinstance(body_B, ConvexPolygon):
            return self.find_polygon_circle_contact_points(body_B, body_A)
