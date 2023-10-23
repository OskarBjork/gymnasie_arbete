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


class Rectangle(PhysObj):
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        height: int,
        width: int,
        position=Vector2D(*ORIGIN),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
    ):
        super().__init__(mass, color, velocity, force)
        self.middle_point = position
        self.height = height
        self.width = width

    def is_inside_of(self, other_rect):
        a1 = Vector2D(
            self.middle_point.x - self.width / 2, self.middle_point.y + self.height / 2
        )
        a2 = Vector2D(
            self.middle_point.x + self.width / 2, self.middle_point.y - self.height / 2
        )
        b1 = Vector2D(
            other_rect.middle_point.x - other_rect.width / 2,
            other_rect.middle_point.y + other_rect.height / 2,
        )
        b2 = Vector2D(
            Vector2D(
                other_rect.middle_point.x - other_rect.width / 2,
                other_rect.middle_point.y + other_rect.height / 2,
            )
        )
        if b2.y > a1.y or a2.y > b1.y or a1.x > b2.x or b1.x > a2.x:
            return False
        return True


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
