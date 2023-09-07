import pygame
from math import ceil

from pyng.config import RED, BLACK, WHITE, GRID_SCALE, PIXELS_PER_METER


# TODO: Flytta
def convert_coordinates(x, y, screen) -> (float, float):
    return x, screen.get_height() - y


class ViewModel:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font = pygame.font.Font(None, 36)

    def clear(self):
        self.screen.fill(WHITE)

    def update(self):
        pygame.display.update()

    def place_pixel(self, x: int, y: int, color: tuple) -> None:
        converted_x, converted_y = convert_coordinates(x, y, self.screen)
        pygame.draw.rect(self.screen, color, (converted_x, converted_y, 1, 1))

    def show_grid(self):
        """Till för att visa rutnätet."""
        origo = self.width // GRID_SCALE, self.height // GRID_SCALE

        num_of_lines_vertical = ceil(self.width / PIXELS_PER_METER)
        num_of_lines_horizontal = ceil(self.height / PIXELS_PER_METER)

        # Skapar rutorna
        for i in range(num_of_lines_vertical):
            x_offset = i * PIXELS_PER_METER

            pygame.draw.line(
                surface=self.screen,
                color=BLACK,
                start_pos=convert_coordinates(
                    origo[0] + x_offset, origo[1], self.screen
                ),
                end_pos=convert_coordinates(
                    origo[0] + x_offset, self.height, self.screen
                ),
            )
            # Ritar siffrorna
            self.render_text(
                f"{i * 100}",
                BLACK,
                convert_coordinates(origo[0] + x_offset, origo[1], self.screen),
            )

        # Samma ordning som ovan
        for i in range(num_of_lines_horizontal):
            y_offset = i * PIXELS_PER_METER

            pygame.draw.line(
                surface=self.screen,
                color=BLACK,
                start_pos=convert_coordinates(
                    origo[0], origo[1] + y_offset, self.screen
                ),
                end_pos=convert_coordinates(
                    self.width, origo[1] + y_offset, self.screen
                ),
            )

            if i == 0:
                continue
            self.render_text(
                f"{i * 100}",
                BLACK,
                convert_coordinates(origo[0] - 50, origo[1] + y_offset, self.screen),
            )

    def set_caption(self, caption: str) -> None:
        pygame.display.set_caption(caption)

    def create_text(self, text: str, color: tuple, position: tuple) -> None:
        return self.font.render(text, True, color)

    def render_text(self, text: str, color: tuple, position: tuple) -> None:
        text_surface = self.create_text(text, color, position)
        self.screen.blit(text_surface, position)

    def render_objects(self, objects: list) -> None:
        for obj in objects:
            obj.render(self)

    def render_polygon(self, polygon):
        polygon.update_points()
        converted_points = []
        for point in polygon.points:
            converted_points.append(
                convert_coordinates(point[0], point[1], self.screen)
            )
        pygame.draw.polygon(
            surface=self.screen, color=polygon.color, points=converted_points
        )

    def render_circle(self, circle):
        pygame.draw.circle(
            surface=self.screen,
            color=circle.color,
            center=convert_coordinates(
                circle.position.x, circle.position.y, self.screen
            ),
            radius=circle.radius,
        )
