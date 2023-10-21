# TODO: Ta bort all third-part dependencies förutom pygame
# TODO: Gör så att mindre upplösning ger samma information
# TODO: Ta bort allt klotter härifrån och sätt det in i andra klasser
# TODO: TYPE ANNOTATIONS!

import time

import pygame

from pyng.space.phys_obj import Circle, Point
from pyng.space.vectors import Vector2D
from pyng.space.interface.view_model import ViewModel
from pyng.state.state import State
from pyng.config import FPS, RED, BLACK, TEST_COORDINATE, BLUE, ORIGIN, GREEN
from simulation.event_handler import handle_events


def main():
    pygame.init()

    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    state = State()

    view_model = ViewModel(screen)

    view_model.set_caption("Pyng")

    screen.fill(BLACK)
    running = True
    prev_time = time.time()

    obj1 = Circle(mass=10, radius=10, color=BLUE)

    while running:
        clock.tick(FPS)
        # TODO: Omstrukturera tid in i egen funktion/klass
        now = time.time()
        dt = now - prev_time
        prev_time = now

        view_model.clear()

        if handle_events(pygame.event.get()) == "mouse 1":
            state.parse_mouse_click(
                Vector2D(*(view_model.convert_coordinates(*pygame.mouse.get_pos())))
            )

        state.check_collisions()

        state.step(dt)

        view_model.render_objects(state.objects)

        view_model.show_grid()

        view_model.update()

    pygame.quit()


if __name__ == "__main__":
    main()
