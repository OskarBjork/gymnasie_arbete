from pyng.space.vectors import Vector2D
from pyng.config import RED, ORIGIN
from pyng.space.interface.view_model import ViewModel, relative_to_origin
import math


class PhysObj:
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        position=Vector2D(*ORIGIN),  # Centrumet av formen
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
        is_static=False,
        id: str = None,
        restitution=0,
    ):
        self.mass = mass
        if not is_static:
            self.inverse_mass = 1 / self.mass
        else:
            self.inverse_mass = 0
        self.position = position
        self.velocity = velocity
        self.force = force
        self.color = color
        self.is_static = is_static
        self.id = id
        self.restitution = restitution

    def is_inside_of(self, other_object) -> bool:
        pass

    def add_force(self, force: Vector2D):
        self.force = self.force + force

    def update_velocity(self, delta_time: float):
        # self.velocity = self.velocity + (self.force / self.mass) * delta_time
        self.velocity = self.velocity + (self.force * self.inverse_mass) * delta_time

    def update_position(self, delta_time: float):
        self.position = self.position + self.velocity * delta_time

    def render(self, view_model):
        view_model.render_polygon(self)

    def __repr__(self) -> str:
        return f"PhysObj(position={self.position} id = {self.id})"


class Point(PhysObj):
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        position=Vector2D(*ORIGIN),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
        is_static=False,
        id: str = None,
        restitution=0,
    ):
        super().__init__(
            mass, color, position, velocity, force, is_static, id, restitution
        )

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
        position=Vector2D(*ORIGIN),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
        num_of_sides=4,
        side_length=1,
        angle=0,
        is_static=False,
        id: str = None,
        restitution=0,
    ):
        super().__init__(
            mass, color, position, velocity, force, is_static, id, restitution
        )
        self.num_of_sides = num_of_sides
        self.side_length = side_length
        self.angle = angle
        self.vertices = self.update_vertices()
        self.bounding_box = self.calculate_polygon_bounding_box()
        self.potential_collision = 0

    def update_vertices(self):
        p = self.position
        k = self.num_of_sides
        s = self.side_length
        angle = self.angle
        vertices = []
        for i in range(k):
            rotated_angle = angle + 2 * math.pi * i / k
            x = p.x + s * math.cos(rotated_angle)
            y = p.y + s * math.sin(rotated_angle)
            vertices.append(Vector2D(x, y))
        self.vertices = vertices
        return vertices

    def calculate_polygon_bounding_box(self):
        min_x = min(v.x for v in self.vertices)
        max_x = max(v.x for v in self.vertices)
        min_y = min(v.y for v in self.vertices)
        max_y = max(v.y for v in self.vertices)
        return [(min_x, min_y), (max_x, max_y)]

    def is_axis_aligned_rectangle(self) -> bool:
        """Återvänder sant om objektet är en rektangel som inte har roterats"""
        # TODO: Kolla om bättre implementation finns när det kommer till
        #       om rektangeln roterats
        non_rotated_angles = [
            math.pi / 4,
            3 * math.pi / 4,
            5 * math.pi / 4,
            7 * math.pi / 4,
        ]
        return self.num_of_sides == 4 and self.angle in non_rotated_angles

    def check_axis_aligned_collision(self, other_rect) -> bool:
        # Utgår ifrån att self.position är mitten av rektangel vilket det inte är rent grafiskt
        side_len = self.side_length / 2
        other_side_len = other_rect.side_length / 2

        x_max = self.position.x + side_len
        x_min = self.position.x - side_len
        other_x_max = other_rect.position.x + other_side_len
        other_x_min = other_rect.position.x - other_side_len

        y_max = self.position.y + side_len
        y_min = self.position.y - side_len
        other_y_max = other_rect.position.y + other_side_len
        other_y_min = other_rect.position.y - other_side_len
        return (
            x_min < other_x_max
            and other_x_min < x_max
            and y_min < other_y_max
            and other_y_min < y_max
        )

    def is_inside_of(self, other_rect):
        if (
            self.is_axis_aligned_rectangle() and other_rect.is_axis_aligned_rectangle()
        ):  # Använd AABB
            return self.check_axis_aligned_collision(other_rect)

    def project(self, axis: Vector2D):
        """Går igenom alla vertices i ett objekt och projicerar dem på en axel, och returnerar sedan minsta och största värdena av dessa"""
        min_proj = float("inf")
        max_proj = float("-inf")
        for vertex in self.vertices:
            dot_product = vertex.x * axis.x + vertex.y * axis.y
            min_proj = min(min_proj, dot_product)
            max_proj = max(max_proj, dot_product)
        return min_proj, max_proj

    def render(self, view_model):
        view_model.render_polygon(self)


class Rectangle(ConvexPolygon):
    def __init__(
        self,
        mass: int,
        color: (int, int, int),
        position: (int, int),
        width: int,
        height: int,
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
        angle=math.pi/4,
        is_static=False,
        id=None,
        restitution=0  # vet inte om den är en int eller float
    ):
        self.width = width
        self.height = height
        super().__init__(
            mass=mass,
            color=color,
            position=position,
            velocity=velocity,
            force=force,
            num_of_sides=4,
            side_length=None,
            angle=angle,
            is_static=is_static,
            id=id,
            restitution=restitution,
        )

    def update_vertices(self):
        p = self.position
        k = self.num_of_sides
        w = self.width
        h = self.height
        angle = self.angle
        vertices = []
        for i in range(k):
            rotated_angle = angle + 2 * math.pi * i / k
            x = p.x + w * math.cos(rotated_angle)
            y = p.y + h * math.sin(rotated_angle)
            vertices.append(Vector2D(x, y))
        self.vertices = vertices
        return vertices

    def check_axis_aligned_collision(self, other_rect) -> bool:
        # Utgår ifrån att self.position är mitten av rektangel vilket det inte är rent grafiskt
        w = self.width / 2
        h = self.height / 2
        other_w = other_rect.width / 2
        other_h = other_rect.height / 2

        x_max = self.position.x + w
        x_min = self.position.x - w
        other_x_max = other_rect.position.x + other_w
        other_x_min = other_rect.position.x - other_w

        y_max = self.position.y + h
        y_min = self.position.y - h
        other_y_max = other_rect.position.y + h
        other_y_min = other_rect.position.y - h
        return (
            x_min < other_x_max
            and other_x_min < x_max
            and y_min < other_y_max
            and other_y_min < y_max
        )


class Circle(PhysObj):
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        position=Vector2D(*ORIGIN),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
        radius=1,
        is_static=False,
        id: str = None,
        restitution=0,
    ):
        super().__init__(
            mass, color, position, velocity, force, is_static, id, restitution
        )
        self.radius = radius

    def render(self, view_model):
        view_model.render_circle(self)

    def is_inside_of(self, other) -> bool:
        if isinstance(other, Circle):
            return (
                self.position.distance_to(other.position) < self.radius + other.radius
            )

    def project(self, axis: Vector2D):
        direction = axis.normalize()
        direction_and_radius = direction * self.radius
        p1 = self.position - direction_and_radius
        p2 = self.position + direction_and_radius

        min_proj = p1.dot(axis)
        max_proj = p2.dot(axis)
        if min_proj > max_proj:
            min_proj, max_proj = max_proj, min_proj
        return min_proj, max_proj


class CollisionResult:
    def __init__(self, contact_point: Vector2D, normal: Vector2D):
        self.contact_point = contact_point
        self.normal = normal
