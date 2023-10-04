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
        self.force += force

    def update_velocity(self, delta_time: float):
        self.velocity = self.velocity + (self.force / self.mass) * delta_time

    def update_position(self, delta_time: float):
        self.position = self.position + self.velocity * delta_time

    def render(self, view_model):
        view_model.render_polygon(self)


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


class Square(PhysObj):
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        width: int,
        height: int,
        position=Vector2D(*ORIGIN),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
    ):
        super().__init__(mass, color, position, velocity, force)
        self.width = width
        self.height = height
        self.update_points()

    def update_points(self):
        self.points = [
            (self.position.x - self.width // 2, self.position.y - self.height // 2),
            (self.position.x + self.width // 2, self.position.y - self.height // 2),
            (self.position.x + self.width // 2, self.position.y + self.height // 2),
            (self.position.x - self.width // 2, self.position.y + self.height // 2),
        ]

    def is_inside_of(self, other_object) -> bool:
        return (
            self.position.x == other_object.position.x
            and self.position.y == other_object.position.y
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
    ):
        super().__init__(mass, color, position, velocity, force)
        self.radius = radius

    def render(self, view_model):
        view_model.render_circle(self)

    def is_inside_of(self, other) -> bool:
        return self.position.distance_to(other.position) < self.radius + other.radius
