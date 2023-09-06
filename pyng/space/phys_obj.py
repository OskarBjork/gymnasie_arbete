from pyng.space.vectors import TwoDimensionalVector
from pyng.config import RED


class PhysObj:
    def __init__(
        self,
        mass: float,
        color: (int, int, int),
        position: TwoDimensionalVector,
        velocity=TwoDimensionalVector(0, 0),
        force=TwoDimensionalVector(0, 0),
    ):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.force = force
        self.color = color
        self.stop = False
        self.gravitational_force = TwoDimensionalVector(0, mass * -9.82)
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

    def render(self, view_model):
        for pixel_x in range(1, self.width):
            for pixel_y in range(1, self.height):
                view_model.place_pixel(
                    self.position.x + pixel_x,
                    self.position.y + pixel_y,
                    self.color,
                )
