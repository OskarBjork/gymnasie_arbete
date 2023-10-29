# TODO: Ta bort all third-part dependencies förutom pygame
# TODO: Gör så att mindre upplösning ger samma information
# TODO: Ta bort allt klotter härifrån och sätt det in i andra klasser
# TODO: TYPE ANNOTATIONS!

# TODO: Collision detection
# Broad phase: bounding volume hierarchies
# Narrow phase: ?

import time
import sys
import math

import pygame
import pygame_gui
from rich.traceback import install

install(show_locals=True)

from pyng.space.phys_obj import Circle, Point, ConvexPolygon
from pyng.space.vectors import Vector2D
from pyng.space.interface.view_model import ViewModel
from pyng.state.state import State
from pyng.config import (
    FPS,
    RED,
    BLACK,
    TEST_COORDINATE,
    BLUE,
    ORIGIN,
    GREEN,
    ORANGE,
    YELLOW,
    PINK,
    PURPLE,
    GRAY,
    LIGHT_BLUE,
)
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

    obj1 = ConvexPolygon(
        mass=30,
        color=GREEN,
        position=Vector2D(1000, 670),
        velocity=Vector2D(-100, 0),
        num_of_sides=4,
        side_length=100,
        angle=math.pi / 4,
    )

    obj2 = ConvexPolygon(
        mass=30,
        color=RED,
        position=Vector2D(100, 670),
        velocity=Vector2D(100, 0),
        num_of_sides=4,
        side_length=100,
        angle=math.pi / 4,
    )

    obj3 = ConvexPolygon(
        mass=30,
        color=BLUE,
        position=Vector2D(500, 500),
        velocity=Vector2D(0, 10),
        num_of_sides=4,
        side_length=100,
        angle=math.pi / 4,
    )

    obj4 = ConvexPolygon(
        mass=30,
        color=ORANGE,
        position=Vector2D(1500, 500),
        velocity=Vector2D(0, 0),
        num_of_sides=4,
        side_length=100,
        angle=math.pi / 4,
    )

    obj5 = ConvexPolygon(
        mass=30,
        color=PINK,
        position=Vector2D(1500, 500),
        velocity=Vector2D(0, 0),
        num_of_sides=4,
        side_length=100,
        angle=math.pi / 4,
    )

    obj6 = ConvexPolygon(
        mass=30,
        color=PURPLE,
        position=Vector2D(1500, 500),
        velocity=Vector2D(0, 0),
        num_of_sides=4,
        side_length=100,
        angle=math.pi / 4,
    )

    state.add_objects([obj1, obj2, obj3, obj4, obj5, obj6])

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

        state.find_collisions()

        view_model.render_ui(ui_manager)

        view_model.update(ui_refresh_rate)

    pygame.quit()


if __name__ == "__main__":
    main()
