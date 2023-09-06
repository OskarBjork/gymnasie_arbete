import pygame


class ViewModel:
    def __init__(self, screen) -> None:
        self.screen = screen

    def place_pixel(self, x: int, y: int, color: tuple) -> None:
        pygame.draw.rect(self.screen, color, (x, y, 10, 10))

    def render_objects(self, objects: list) -> None:
        for obj in objects:
            self.place_pixel(obj.position.x, obj.position.y, obj.color)
