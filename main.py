# TODO: Ta bort all third-part dependencies förutom pygame
# TODO: Gör så att mindre upplösning ger samma information
# TODO: Ta bort allt klotter härifrån och sätt det in i andra klasser
# TODO: TYPE ANNOTATIONS!

import time
import sys

import pygame
import pygame_gui

from pyng.space.phys_obj import Circle, Point, Rectangle
from pyng.space.vectors import Vector2D
from pyng.space.interface.view_model import ViewModel
from pyng.state.state import State
from pyng.config import FPS, RED, BLACK, TEST_COORDINATE, BLUE, ORIGIN, GREEN
from simulation.event_handler import handle_events, delegate_event


def main():
    pygame.init()

    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    state = State()

    ui_manager = pygame_gui.UIManager((screen_width, screen_height))
    view_model = ViewModel(screen, ui_manager)

    view_model.set_caption("Pyng")

    screen.fill(BLACK)
    running = True
    prev_time = time.time()

    view_model.show_editor()

    obj1 = Rectangle(
        mass=30,
        width=20,
        height=10,
        color=GREEN,
        position=Vector2D(700, 670),
        velocity=Vector2D(-100, 0),
    )

    obj2 = Rectangle(
        mass=30,
        width=10,
        height=10,
        color=RED,
        position=Vector2D(300, 670),
        velocity=Vector2D(100, 0),
    )

    state.add_object(obj1)
    state.add_object(obj2)

    while running:
        ui_refresh_rate = clock.tick(FPS) / 1000
        # TODO: Omstrukturera tid in i egen funktion/klass
        now = time.time()
        dt = now - prev_time
        prev_time = now

        view_model.clear()

        event = handle_events(pygame.event.get(), ui_manager)

        delegate_event(event, state, view_model, ui_manager)

        state.check_collisions()

        state.step(dt)

        view_model.render_objects(state.objects)

        view_model.render_ui(ui_manager)

        view_model.update(ui_refresh_rate)

    pygame.quit()


if __name__ == "__main__":
    main()
