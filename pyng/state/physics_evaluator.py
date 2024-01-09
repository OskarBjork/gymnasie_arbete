from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon
from pyng.space.vectors import Vector2D
from pyng.helper import (
    projection,
    overlaps,
    find_arithmetic_mean,
    dot_product,
    length_squared,
    distance_squared,
    float_nearly_equal,
    vector_nearly_equal,
)
from pyng.config import GRAVITY_CONSTANT, PIXELS_PER_METER
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
        if collision_happened:
            normal = collision_analysis[2]
            displacement = collision_analysis[1]
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
        if object1.is_static and object2.is_static:
            return
        if isinstance(object1, Circle) and isinstance(object2, Circle):
            self.resolve_circle_collision(manifold)
        elif isinstance(object1, ConvexPolygon) and isinstance(object2, ConvexPolygon):
            self.resolve_polygon_collision(manifold)
        elif isinstance(object1, ConvexPolygon) and isinstance(object2, Circle):
            self.resolve_polygon_circle_collision(manifold)
        elif isinstance(object1, Circle) and isinstance(object2, ConvexPolygon):
            self.resolve_polygon_circle_collision(manifold)

    def resolve_polygon_collision(self, manifold: CollisionManifold):
        obj = manifold.body_A
        other_obj = manifold.body_B
        mtv = manifold.depth
        if obj.is_static:
            other_obj.position = other_obj.position + mtv
        elif other_obj.is_static:
            obj.position = obj.position - mtv
        else:
            obj.position = obj.position - (mtv / 2)
            other_obj.position = other_obj.position + (mtv / 2)
        self.collision_response_rotation(manifold)

    def resolve_circle_collision(self, manifold: CollisionManifold):
        body_A = manifold.body_A
        body_B = manifold.body_B

        direction = body_A.position - body_B.position

        if not direction.magnitude() > 0:
            return  # FIXME: Hantera situationen
        direction = direction.normalize()

        magnitude = manifold.depth / 2

        direction = direction * magnitude

        if body_B.is_static:
            body_A.position = body_A.position + direction
        elif body_A.is_static:
            body_B.position = body_B.position - direction
        else:
            body_A.position = body_A.position + direction
            body_B.position = body_B.position - direction
        self.collision_response_rotation(manifold)

    def resolve_polygon_circle_collision(self, manifold: CollisionManifold):
        polygon = (
            manifold.body_A
            if isinstance(manifold.body_A, ConvexPolygon)
            else manifold.body_B
        )
        circle = (
            manifold.body_B if isinstance(manifold.body_B, Circle) else manifold.body_A
        )
        mtv = manifold.depth
        if circle.is_static:
            polygon.position = polygon.position - mtv
        elif polygon.is_static:
            circle.position = circle.position + mtv
        else:
            circle.position = circle.position + (mtv / 2)
            polygon.position = polygon.position - (mtv / 2)
        self.collision_response_rotation(manifold)

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
        depth = float("inf")
        normal = None

        for polygon in [polygon1, polygon2]:
            for i in range(len(polygon.vertices)):
                va = polygon.vertices[i]
                vb = polygon.vertices[(i + 1) % len(polygon.vertices)]

                edge = vb - va
                axis = Vector2D(-edge.y, edge.x)
                axis = axis.normalize()

                minA, maxA = polygon1.project(axis)
                minB, maxB = polygon2.project(axis)

                if minA >= maxB or minB >= maxA:
                    return False, None, None

                axis_depth = min(maxB - minA, maxA - minB)

                if axis_depth < depth:
                    depth = axis_depth
                    normal = axis

        direction = polygon2.position - polygon1.position

        if direction.dot(normal) < 0:
            normal = Vector2D(-normal.x, -normal.y)

        mtv = normal * depth

        return True, mtv, normal
        # normals1 = self.get_normals(polygon1)
        # normals2 = self.get_normals(polygon2)

        # all_normals = normals1 + normals2

        # min_overlap = float("inf")
        # smallest_axis = None

        # for i, normal in enumerate(all_normals):
        #     projection1 = projection(polygon1, normal)
        #     projection2 = projection(polygon2, normal)

        #     overlap = overlaps(projection1, projection2)

        #     if not overlap:
        #         return False, None, None  # Separating axis found

        #     min1 = projection1[0]
        #     max1 = projection1[1]
        #     min2 = projection2[0]
        #     max2 = projection2[1]

        #     axis_depth = min(max2 - min1, max1 - min2)

        #     if axis_depth < min_overlap:
        #         min_overlap = axis_depth
        #         smallest_axis = normal
        # # min_overlap = min_overlap / (normal.magnitude())
        # smallest_axis = smallest_axis.normalize()
        # center_1 = polygon1.position
        # center_2 = polygon2.position
        # direction = center_2 - center_1

        # if smallest_axis.dot(direction) < 0:
        #     smallest_axis = Vector2D(-smallest_axis.x, -smallest_axis.y)
        # mtv = smallest_axis * min_overlap
        # return True, mtv, smallest_axis  # No separating axis found, polygons overlap

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

    def collision_response(self, manifold: CollisionManifold):
        obj1 = manifold.body_A
        obj2 = manifold.body_B
        if normal.magnitude() == 0:
            return
        normal = normal.normalize()
        relative_velocity = obj1.velocity - obj2.velocity
        if (
            isinstance(obj1, ConvexPolygon)
            and isinstance(obj2, ConvexPolygon)
            and relative_velocity.dot(normal) < 0
        ):
            return
        if (
            isinstance(obj1, Circle) and isinstance(obj2, ConvexPolygon)
        ) and relative_velocity.dot(normal) > 0:
            return
        if (
            isinstance(obj2, ConvexPolygon) and isinstance(obj1, Circle)
        ) and relative_velocity.dot(normal) > 0:
            return

        e = min(obj1.restitution, obj2.restitution)
        j = -(1 + e) * relative_velocity.dot(normal)
        j /= obj1.inverse_mass + obj2.inverse_mass

        impulse = normal * j
        # print("normal: ", normal)
        # print(
        #     f"{obj2.id} Velocity Change", (impulse * obj1.inverse_mass).vector_round()
        # )
        # print(
        #     f"{obj1.id} Velocity Change", (impulse * obj2.inverse_mass).vector_round()
        # )
        obj1.velocity = obj1.velocity + (impulse * obj1.inverse_mass)
        obj2.velocity = obj2.velocity - (impulse * obj2.inverse_mass)
        # print(obj1.velocity, obj1.id)
        # print(obj2.velocity, obj2.id)

    def collision_response_rotation(self, manifold):
        body_A = manifold.body_A
        # print(body_A)
        body_B = manifold.body_B
        normal = manifold.normal
        contact1 = manifold.contact1
        contact2 = manifold.contact2
        contact_count = manifold.contact_count

        e = min(body_A.restitution, body_B.restitution)

        contact_list = [contact1, contact2]

        ra_list = []
        rb_list = []

        impulse_list = []

        for i, contact in enumerate(contact_list):
            if contact is None:
                continue
            ra = contact - body_A.position
            rb = contact - body_B.position

            ra_list.append(ra)
            rb_list.append(rb)

            ra_perp = Vector2D(-ra.y, ra.x)
            rb_perp = Vector2D(-rb.y, rb.x)

            angular_linear_velocity_A = ra_perp * body_A.angular_velocity
            angular_linear_velocity_B = rb_perp * body_B.angular_velocity

            relative_velocity = (angular_linear_velocity_A + body_A.velocity) - (
                angular_linear_velocity_B + body_B.velocity
            )

            contact_velocity_magnitude = relative_velocity.dot(normal)

            # if contact_velocity_magnitude > 0:
            #     return

            ra_perp_dot_normal = ra_perp.dot(normal)
            rb_perp_dot_normal = rb_perp.dot(normal)

            denominator = (
                body_A.inverse_mass
                + body_B.inverse_mass
                + ra_perp_dot_normal**2 * body_A.inverse_rotational_inertia
                + rb_perp_dot_normal**2 * body_B.inverse_rotational_inertia
            )

            j = -(1 + e) * contact_velocity_magnitude
            j /= denominator
            j /= contact_count

            impulse = normal * j
            impulse_list.append(impulse)

        for i, impulse in enumerate(impulse_list):
            ra = ra_list[i]
            rb = rb_list[i]

            body_A.velocity = body_A.velocity + (impulse * body_A.inverse_mass)

            body_A.angular_velocity = (
                body_A.angular_velocity
                + ra.cross(impulse) * body_A.inverse_rotational_inertia
            )

            body_B.velocity = body_B.velocity - (impulse * body_B.inverse_mass)

            body_B.angular_velocity = (
                body_B.angular_velocity
                - rb.cross(impulse) * body_B.inverse_rotational_inertia
            )

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

        distance_squared = length_squared(point - contact)

        return (distance_squared, contact)

    def impose_gravity(self, obj: PhysObj):
        obj.add_force(Vector2D(0, GRAVITY_CONSTANT) * obj.mass)

    def find_circles_contact_point(self, circle1, circle2):
        ab = circle1.position - circle2.position
        dir = ab.normalize()
        return [
            circle1.position - (dir * circle1.radius)
        ]  # Detta kommer ge tillbaka en punkt på skärmen och inte i världen

    def find_polygon_polygon_contact_points(self, polygon1, polygon2):
        contact1 = None
        contact2 = None
        contact_count = 0

        min_dist_squared = float("inf")

        for p in polygon1.vertices:
            for j, va in enumerate(polygon2.vertices):
                vb = polygon2.vertices[(j + 1) % len(polygon2.vertices)]
                distance_squared, contact = self.point_segment_distance(p, va, vb)

                if distance_squared == min_dist_squared:
                    if (
                        not contact == contact1
                    ):  # Floating point jämförelse, kan vara farligt
                        contact2 = contact
                        contact_count = 2

                elif distance_squared < min_dist_squared:
                    min_dist_squared = distance_squared
                    contact_count = 1
                    contact1 = contact

        for p in polygon2.vertices:
            for j, va in enumerate(polygon1.vertices):
                vb = polygon1.vertices[(j + 1) % len(polygon1.vertices)]
                distance_squared, contact = self.point_segment_distance(p, va, vb)

                if distance_squared == min_dist_squared:
                    if (
                        not contact == contact1
                    ):  # Floating point jämförelse, kan vara farligt
                        contact2 = contact
                        contact_count = 2

                elif distance_squared < min_dist_squared:
                    min_dist_squared = distance_squared
                    contact_count = 1
                    contact1 = contact

        return [contact1, contact2, contact_count]

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
            return self.find_polygon_polygon_contact_points(body_A, body_B)
        elif isinstance(body_A, ConvexPolygon) and isinstance(body_B, Circle):
            return self.find_polygon_circle_contact_points(body_A, body_B)
        elif isinstance(body_A, Circle) and isinstance(body_B, ConvexPolygon):
            return self.find_polygon_circle_contact_points(body_B, body_A)
