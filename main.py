# TODO: Ta bort all third-part dependencies förutom pygame
# TODO: Gör så att mindre upplösning ger samma information
# TODO: Ta bort allt klotter härifrån och sätt det in i andra klasser
# TODO: TYPE ANNOTATIONS!


# TODO: Collision detection
# Broad phase: bounding volume hierarchies
# Narrow phase: Separating axis theorem

import time
import sys
import math
import random

import pygame
import pygame_gui
from rich.traceback import install

install(show_locals=True)

from pyng.space.phys_obj import Circle, Point, ConvexPolygon, Rectangle
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
    COLORS,
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

    ui_manager = pygame_gui.UIManager((screen_width, screen_height), "theme.json")
    view_model = ViewModel(screen, ui_manager)

    view_model.set_caption("Pyng")

    screen.fill(BLACK)

    view_model.show_mode_buttons()
    view_model.show_spawn_editor()

    obj1 = ConvexPolygon(
        mass=30,
        color=GREEN,
        position=Vector2D(1000, 670),
        velocity=Vector2D(-200, 0),
        num_of_sides=4,
        side_length=100,
        angle=math.pi / 4,
        id="green",
    )

    obj2 = ConvexPolygon(
        mass=30,
        color=RED,
        position=Vector2D(400, 670),
        velocity=Vector2D(200, 0),
        num_of_sides=4,
        side_length=100,
        angle=math.pi / 4,
        id="red",
    )

    # state.generate_test_data()

    # obj3 = ConvexPolygon(
    #     mass=30,
    #     color=BLUE,
    #     position=Vector2D(200, 500),
    #     # velocity=Vector2D(0, 10),
    #     num_of_sides=4,
    #     side_length=100,
    #     angle=math.pi / 4 + math.pi / 2,
    #     id="blue",
    # )

    # obj4 = ConvexPolygon(
    #     mass=30,
    #     color=ORANGE,
    #     position=Vector2D(600, 550),
    #     # velocity=Vector2D(100, 0),
    #     num_of_sides=4,
    #     side_length=100,
    #     angle=math.pi / 4,
    #     id="orange",
    # )
    # obj5 = ConvexPolygon(
    #     mass=30,
    #     color=PINK,
    #     position=Vector2D(1000, 500),
    #     velocity=Vector2D(0, 0),
    #     num_of_sides=4,
    #     side_length=100,
    #     angle=math.pi / 6,
    #     id="pink",
    # )

    # obj6 = ConvexPolygon(
    #     mass=30,
    #     color=PURPLE,
    #     position=Vector2D(1500, 500),
    #     velocity=Vector2D(0, 0),
    #     num_of_sides=4,
    #     side_length=100,
    #     angle=math.pi / 4,
    #     id="purple",
    # )

    static_box = ConvexPolygon(
        mass=100,
        color=BLUE,
        position=Vector2D(700, 600),
        velocity=Vector2D(0, 0),
        num_of_sides=4,
        side_length=500,
        angle=math.pi / 4,
        is_static=True,
    )

    static_box2 = ConvexPolygon(
        mass=100,
        color=GREEN,
        position=Vector2D(700, 1000),
        velocity=Vector2D(0, 0),
        num_of_sides=1000,
        side_length=50,
        angle=math.pi / 4,
        is_static=True,
    )

    moving_box = ConvexPolygon(
        mass=100,
        color=PURPLE,
        position=Vector2D(1200, 600),
        velocity=Vector2D(100, 0),
        num_of_sides=4,
        side_length=100,
        angle=math.pi / 4,
    )

    moving_circle = Circle(
        mass=100,
        color=RED,
        position=Vector2D(1200, 300),
        velocity=Vector2D(50, 0),
        radius=50,
    )

    static_circle = Circle(
        mass=100,
        color=YELLOW,
        position=Vector2D(1380, 300),
        velocity=Vector2D(0, 0),
        radius=50,
        is_static=True,
    )

    rect = Rectangle(
        mass=10,
        color=PURPLE,
        position=Vector2D(1000, 30),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
        angle=math.pi / 4,
        height=50,
        width=1300,
        is_static=True,
        id=None,
        restitution=0,
    )

    state.add_object(rect)
    # state.add_objects([static_box2, moving_box, moving_circle, static_circle])
    # state.add_objects([obj1, obj2, obj3, obj4, obj5, obj6])
    # state.add_objects([obj1, obj2])

    running = True
    prev_time = time.time()
    frame_limit = 1 / 60
    while running:
        ui_refresh_rate = clock.tick(FPS) / 1000
        # TODO: Omstrukturera tid in i egen funktion/klass
        now = time.time()
        dt = now - prev_time
        prev_time = now

        view_model.clear()

        event = handle_events(pygame.event.get(), ui_manager)

        delegate_event(event, state, view_model, ui_manager)

        state.step(dt)

        state.handle_collisions()

        view_model.render_objects(state.objects)

        view_model.render_ui(ui_manager)

        view_model.update(ui_refresh_rate)

        # state.create_object(position=Vector2D(550,1000), with_gravity=True)

    pygame.quit()


if __name__ == "__main__":
    main()
