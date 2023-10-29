from pyng.space.vectors import Vector2D
from pyng.config import RED, ORIGIN
from pyng.space.interface.view_model import ViewModel


class PhysObj:
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        position=Vector2D(*ORIGIN),  # Centrumet av formen
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
    ):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.force = force
        self.color = color

    def is_inside_of(self, other_object) -> bool:
        pass

    def add_force(self, force: Vector2D):
        self.force = self.force + force

    def update_velocity(self, delta_time: float):
        self.velocity = self.velocity + (self.force / self.mass) * delta_time

    def update_position(self, delta_time: float):
        self.position = self.position + self.velocity * delta_time

    def render(self, view_model):
        view_model.render_polygon(self)

    def __repr__(self) -> str:
        return f"PhysObj(mass={self.mass}, color={self.color}, position={self.position}, velocity={self.velocity}, force={self.force})"


class Point(PhysObj):
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        position=Vector2D(*ORIGIN),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
    ):
        super().__init__(mass, color, position, velocity, force)

    def render(self, view_model):
        view_model.place_pixel(self.position.x, self.position.y, self.color)

    def is_inside_of_other_object(self, other_object) -> bool:
        return (
            self.position.x == other_object.position.x
            and self.position.y == other_object.position.y
        )


class ConvexPolygon(PhysObj):
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        height: int,
        width: int,
        position=Vector2D(*ORIGIN),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
        vertices=[],
    ):
        self.mass = mass
        self.color = color
        self.velocity = velocity
        self.force = force
        self.position = position
        self.height = height
        self.width = width
        self.vertices = vertices
        self.bounding_box = self.calculate_polygon_bounding_box()

    def calculate_polygon_bounding_box(self):
        min_x = min(v.x for v in self.vertices)
        max_x = max(v.x for v in self.vertices)
        min_y = min(v.y for v in self.vertices)
        max_y = max(v.y for v in self.vertices)
        return [(min_x, min_y), (max_x, max_y)]

    def is_inside_of(self, other_rect):
        a1 = self.position
        a2 = Vector2D(self.position.x + self.width, self.position.y + self.height)
        b1 = other_rect.position
        b2 = Vector2D(
            other_rect.position.x + other_rect.width,
            other_rect.position.y + other_rect.height,
        )
        if b2.y > a1.y or a2.y > b1.y or a1.x > b2.x or b1.x > a2.x:
            return False
        return True

    def render(self, view_model):
        view_model.render_polygon(self)


class Circle(PhysObj):
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        position=Vector2D(*ORIGIN),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
        radius=1,
    ):
        super().__init__(mass, color, position, velocity, force)
        self.radius = radius

    def render(self, view_model):
        view_model.render_circle(self)

    def is_inside_of(self, other) -> bool:
        return self.position.distance_to(other.position) < self.radius + other.radius


class CollisionResult:
    def __init__(self, contact_point: Vector2D, normal: Vector2D):
        self.contact_point = contact_point
        self.normal = normal


# def RayVsRect(ray_origin: Vector2D, ray_direction: Vector2D, target: Rectangle) -> bool:
#     t_near = (target.position - ray_origin).element_division(ray_direction)
#     t_far = (
#         target.position + Vector2D(target.width, target.height) - ray_origin
#     ).element_division(ray_direction)
#     if t_near.x > t_far.x:
#         t_near.x, t_far.x = t_far.x, t_near.x

#     if t_near.y > t_far.y:
#         t_near.y, t_far.y = t_far.y, t_near.y

#     # Nx < Fy eller Ny < Fx
#     if t_near.x > t_far.y or t_near.y < t_far.x:
#         return False

#     t_hit_near = max(t_near.x, t_near.y)
#     t_hit_far = min(t_far.x, t_far.y)

#     if t_hit_far < 0:
#         return False

#     contact_point = ray_origin + (t_hit_near * ray_direction)

#     # Hitta vilken sida som träffas

#     if t_near.x > t_near.y:
#         if ray_direction.x < 0:
#             normal = Vector2D(1, 0)
#         else:
#             normal = Vector2D(-1, 0)

#     elif t_near.x < t_near.y:
#         if ray_direction.y < 0:
#             normal = Vector2D(0, 1)
#         else:
#             normal = Vector2D(0, -1)

#     return True, CollisionResult(contact_point, normal)

#     # TODO: FINISH ME


# RayVsRect(Vector2D(0, 0), Vector2D(1, 1), Rectangle(1, RED, 1, 1))
