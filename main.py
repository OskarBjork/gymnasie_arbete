import time
import sys
import math
import random
import os

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
    RESOLUTION_ITERATIONS,
)
from simulation.event_handler import handle_events, delegate_event


# TODO: Gör så att mindre upplösning ger samma information
# TODO: Ta bort allt klotter härifrån och sätt det in i andra klasser
# TODO: TYPE ANNOTATIONS!
# TODO: Skapa ett sätt för användaren att mäta tid
# TODO: Skapa ett sätt för användaren att mäta distans
# TODO: Skapa ett sätt för användaren att inspektera objekt och se deras egenskaper
# TODO: Skapa ett sätt för användaren att kontrollera objekt


os.environ[
    "SDL_VIDEO_WINDOW_POS"
] = "1920, 0"  # Kommentera bort ifall man inte vill att fönstret ska öppnas på en annan skärm


def main():
    pygame.init()

    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    ui_manager = pygame_gui.UIManager((screen_width, screen_height), "theme.json")
    view_model = ViewModel(screen, ui_manager)

    state = State(view_model=view_model)
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
        position=Vector2D(500, 600),
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
        mass=1000000000,
        color=BLUE,
        position=Vector2D(850, ORIGIN[1] + 100),
        velocity=Vector2D(0, 0),
        force=Vector2D(100, 50),
        angle=math.pi / 4,
        height=50,
        width=1100,
        is_static=True,
        id="blue",
    )

    polygon1 = ConvexPolygon(
        mass=10,
        color=BLUE,
        num_of_sides=6,
        side_length=50,
        position=Vector2D(300, 100),
        velocity=Vector2D(0, 0),
        force=Vector2D(1000, 500),
        angle=math.pi / 4,
        is_static=False,
        id="blue",
    )

    rect2 = Rectangle(
        mass=10,
        color=RED,
        position=Vector2D(300, 100),
        velocity=Vector2D(100, 50),
        force=Vector2D(0, 0),
        angle=math.pi / 4,
        height=50,
        width=50,
        is_static=False,
        id="red",
    )

    circle = Circle(
        mass=1.5,
        color=RED,
        position=Vector2D(750, 300),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
        radius=100,
        id="red",
    )

    circle2 = Circle(
        mass=0.5,
        color=BLUE,
        position=Vector2D(500, 300),
        velocity=Vector2D(0, 0),
        force=Vector2D(0, 0),
        radius=10,
        id="blue",
    )

    # state.add_object(rect)
    # state.add_objects([static_box2, moving_box, moving_circle, static_circle])
    # state.add_objects([obj1, obj2, obj3, obj4, obj5, obj6])
    # state.add_objects([circle, polygon1])

    running = True
    prev_time = time.time()
    frame_limit = 1 / 60
    state.generate_test_data(scale=5)
    while running:
        ui_refresh_rate = clock.tick(FPS) / 1000
        # TODO: Omstrukturera tid in i egen funktion/klass
        now = time.time()
        dt = now - prev_time
        prev_time = now

        view_model.clear()

        event = handle_events(pygame.event.get(), ui_manager)

        delegate_event(event, state, view_model, ui_manager)
        
        # Slutar beräkna fysiken ifall användaren har pausat simulationen
        if not state.is_paused: 
            state.step(delta_time=dt, iterations=RESOLUTION_ITERATIONS)
            state.handle_collisions()

        view_model.render_or_uptade_selected_object_related()

        view_model.render_objects(state.objects)

        view_model.render_ui(ui_manager)

        view_model.update(ui_refresh_rate)

        # state.create_object(position=Vector2D(550,1000), with_gravity=True)

    pygame.quit()


if __name__ == "__main__":
    main()
