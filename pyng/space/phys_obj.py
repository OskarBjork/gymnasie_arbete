from pyng.space.vectors import TwoDimensionalVector
from pyng.config import RED
from pyng.space.interface.view_model import convert_coordinates


class PhysObj:
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        position: TwoDimensionalVector,  # Centrumet av formen
        velocity=TwoDimensionalVector(0, 0),
        force=TwoDimensionalVector(0, 0),
    ):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.force = force
        self.color = color
        self.stop = False
        self.gravitational_force = TwoDimensionalVector(0, self.mass * -982)
        self.force.y += self.gravitational_force.y

    def is_inside_of_other_object(self, other_object) -> bool:
        return (
            self.position.x == other_object.position.x
            and self.position.y == other_object.position.y
        )

    def add_force(self, force: TwoDimensionalVector):
        self.force += force

    def update_velocity(self, delta_time: float):
        self.velocity.x = self.velocity.x + (self.force.x / self.mass) * delta_time
        self.velocity.y = self.velocity.y + (self.force.y / self.mass) * delta_time

    def update_position(self, delta_time: float):
        self.position.x = self.position.x + self.velocity.x * delta_time
        self.position.y = self.position.y + self.velocity.y * delta_time

    def render(self, view_model):
        view_model.render_polygon(self)


class Point(PhysObj):
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        position: TwoDimensionalVector,
        velocity=TwoDimensionalVector(0, 0),
        force=TwoDimensionalVector(0, 0),
    ):
        super().__init__(mass, color, position, velocity, force)

    def render(self, view_model):
        view_model.place_pixel(self.position.x, self.position.y, self.color)


class Square(PhysObj):
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        width: int,
        height: int,
        position: TwoDimensionalVector,
        velocity=TwoDimensionalVector(0, 0),
        force=TwoDimensionalVector(0, 0),
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


class Circle(PhysObj):
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        position: TwoDimensionalVector,
        velocity=TwoDimensionalVector(0, 0),
        force=TwoDimensionalVector(0, 0),
        radius=1,
    ):
        super().__init__(mass, color, position, velocity, force)
        self.radius = radius

    def render(self, view_model):
        view_model.render_circle(self)
