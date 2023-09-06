import pygame


# TODO: Flytta
def convert_coordinates(x, y, screen) -> (float, float):
    return x, screen.get_height() - y


class ViewModel:
    def __init__(self, screen) -> None:
        self.screen = screen

    def place_pixel(self, x: int, y: int, color: tuple) -> None:
        converted_x, converted_y = convert_coordinates(x, y, self.screen)
        pygame.draw.rect(self.screen, color, (converted_x, converted_y, 1, 1))

    def render_objects(self, objects: list) -> None:
        for obj in objects:
            obj.render(self)
