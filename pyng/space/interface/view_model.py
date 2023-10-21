from math import ceil

import pygame
import pygame_gui
from pygame import Surface

from pyng.config import RED, BLACK, WHITE, GRID_SCALE, PIXELS_PER_METER, ORIGIN


# TODO: Flytta


class ViewModel:
    def __init__(self, screen: Surface, UI_manager) -> None:
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.UI_manager = UI_manager
        self.font = pygame.font.Font(None, 36)

    def convert_coordinates(self, x, y) -> (float, float):
        return x, self.screen.get_height() - y

    def clear(self):
        self.screen.fill(WHITE)

    def update(self, UI_refresh_rate: float):
        pygame.display.update()
        self.UI_manager.update(UI_refresh_rate)

    def place_pixel(self, x: int, y: int, color: tuple) -> None:
        converted_x, converted_y = self.convert_coordinates(x, y)
        pygame.draw.rect(self.screen, color, (converted_x, converted_y, 1, 1))

    def show_grid(self):
        origin = ORIGIN

        num_of_lines_vertical = ceil(self.width / PIXELS_PER_METER)
        num_of_lines_horizontal = ceil(self.height / PIXELS_PER_METER)

        # Skapar rutorna
        for i in range(num_of_lines_vertical):
            x_offset = i * PIXELS_PER_METER

            pygame.draw.line(
                surface=self.screen,
                color=BLACK,
                start_pos=self.convert_coordinates(origin[0] + x_offset, origin[1]),
                end_pos=self.convert_coordinates(origin[0] + x_offset, self.height),
            )
            # Ritar siffrorna
            self.render_text(
                f"{i * 100}",
                BLACK,
                self.convert_coordinates(origin[0] + x_offset, origin[1]),
            )

        # Samma ordning som ovan
        for i in range(num_of_lines_horizontal):
            y_offset = i * PIXELS_PER_METER

            pygame.draw.line(
                surface=self.screen,
                color=BLACK,
                start_pos=self.convert_coordinates(origin[0], origin[1] + y_offset),
                end_pos=self.convert_coordinates(self.width, origin[1] + y_offset),
            )

            if i == 0:
                continue
            self.render_text(
                f"{i * 100}",
                BLACK,
                self.convert_coordinates(origin[0] - 50, origin[1] + y_offset),
            )
        self.render_text(
            "Radius:",
            BLACK,
            (0, 80),
        )

    def render_UI(self, UI_manager):
        self.show_grid()
        UI_manager.draw_ui(self.screen)

    def show_editor(self):
        text_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 100), (0.7 * ORIGIN[0], 50)),
            manager=self.UI_manager,
            object_id="#radius_input",
        )

        pass

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
            converted_points.append(self.convert_coordinates(point[0], point[1]))

        pygame.draw.polygon(
            surface=self.screen, color=polygon.color, points=converted_points
        )

    def render_circle(self, circle):
        pygame.draw.circle(
            surface=self.screen,
            color=circle.color,
            center=self.convert_coordinates(circle.position.x, circle.position.y),
            radius=circle.radius,
        )
