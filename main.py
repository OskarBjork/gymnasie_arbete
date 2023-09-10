# TODO: Ta bort all third-part dependencies
# TODO: Gör så att mindre upplösning ger samma information
# TODO Ta bort allt klotter härifrån och sätt det in i andra klasser

import time

import pygame

from pyng.space.phys_world import PhysWorld
from pyng.space.phys_obj import PhysObj, Point, Square, Circle
from pyng.space.vectors import TwoDimensionalVector
from pyng.space.interface.view_model import ViewModel
from pyng.config import FPS, RED, BLACK, TEST_COORDINATE
from pyng.time.events.event_handler import EventHandler


def main():
    pygame.init()

    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    world = PhysWorld(screen_width, screen_height)

    event_handler = EventHandler()

    view_model = ViewModel(screen)

    view_model.set_caption("Pyng")

    obj1 = Circle(
        mass=10,
        color=RED,
        position=TwoDimensionalVector(*TEST_COORDINATE),
        radius=100,
        force=TwoDimensionalVector(0, -982 * 10),
    )

    obj2 = Circle(
        mass=10,
        color=RED,
        position=TwoDimensionalVector(1000, 800),
        radius=100,
        no_gravity=True,
    )

    world.add_object(obj1)
    world.add_object(obj2)

    screen.fill(BLACK)
    running = True
    prev_time = time.time()

    while running:
        clock.tick(FPS)
        now = time.time()
        dt = now - prev_time
        prev_time = now

        view_model.clear()

        event_handler.handle_events(pygame.event.get())

        world.step(dt)

        view_model.render_objects(world.objects)

        view_model.show_grid()

        view_model.update()

    pygame.quit()


if __name__ == "__main__":
    main()
