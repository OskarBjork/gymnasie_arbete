# TODO: Ta bort all third-part dependencies förutom pygame
# TODO: Gör så att mindre upplösning ger samma information
# TODO: Ta bort allt klotter härifrån och sätt det in i andra klasser
# TODO: TYPE ANNOTATIONS!

import time

import pygame

from pyng.state.phys_world import PhysWorld
from pyng.space.phys_obj import Circle
from pyng.space.vectors import Vector2D
from pyng.space.interface.view_model import ViewModel
from pyng.state.analyzer import check_collisions
from pyng.config import FPS, RED, BLACK, TEST_COORDINATE
from simulation.event_handler import handle_events


def main():
    pygame.init()

    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    world = PhysWorld(screen_width, screen_height)

    view_model = ViewModel(screen)

    view_model.set_caption("Pyng")

    obj1 = Circle(
        mass=10,
        color=RED,
        position=Vector2D(*TEST_COORDINATE),
        radius=100,
        force=Vector2D(0, -982 * 10),
    )

    obj2 = Circle(
        mass=10,
        color=RED,
        position=Vector2D(1000, 500),
        radius=100,
    )

    world.add_object(obj1)
    world.add_object(obj2)

    screen.fill(BLACK)
    running = True
    prev_time = time.time()

    while running:
        clock.tick(FPS)
        # TODO: Omstrukturera tid in i egen funktion/klass
        now = time.time()
        dt = now - prev_time
        prev_time = now

        view_model.clear()

        handle_events(pygame.event.get())

        check_collisions(world.objects)

        world.step(dt)

        view_model.render_objects(world.objects)

        view_model.show_grid()

        view_model.update()

    pygame.quit()


if __name__ == "__main__":
    main()
