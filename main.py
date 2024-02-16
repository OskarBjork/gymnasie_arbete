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

# TODO: Skapa ett sätt för användaren att kontrollera objekt
# TODO: Skapa godtycklig polygon


# os.environ[
#     "SDL_VIDEO_WINDOW_POS"
# ] = "1920, 0"  # Kommentera bort ifall man inte vill att fönstret ska öppnas på en annan skärm


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

    rect1 = Rectangle(
        mass=1,
        color=PINK,
        width=1000,
        height=100,
        position=Vector2D(1000, 100),
        is_static=True,
    )
    rect2 = Rectangle(
        mass=1,
        color=RED,
        width=100,
        height=100,
        position=Vector2D(200, 400),
        force=Vector2D(50, 50),
    )
    
    # Experiment Objekt
    balanceBoardBase = ConvexPolygon(
        mass=1,
        color=YELLOW,
        position=Vector2D(200 + ORIGIN[0], 100 + ORIGIN[1]),
        num_of_sides=3,
        side_length=50,
        angle=math.pi / 2,
        is_static=True,
    )
    balanceBoard = ConvexPolygon(
        mass=1,
        color=RED,
        width=200,
        height=10,
        position=Vector2D(200 + ORIGIN[0], 128 + 5 + ORIGIN[1]),
    )

    state.add_objects([balanceBoard, balanceBoardBase])

    experiment_start_time = 0 # NOTE: gjord för experiment
    experiment_end_time = 0 # NOTE: gjord för experiment
    current_experiment_start_time = 0 # NOTE: gjord för experiment

    running = True
    prev_time = time.time()
    frame_limit = 1 / 60
    # state.generate_test_data(scale=5
    while running:
        ui_refresh_rate = clock.tick(FPS) / 1000
        # TODO: Omstrukturera tid in i egen funktion/klass
        now = time.time()
        dt = now - prev_time
        prev_time = now

        view_model.clear()

        # print(state.objects)

        event = handle_events(pygame.event.get(), ui_manager)

        delegate_event(event, state, view_model, ui_manager)
        
        # experiment_code(state) # NOTE: gjord för experiment
        if state.is_paused: # NOTE: gjord för experiment
            current_experiment_start_time = time.time() # NOTE: gjord för experiment
        
        # Slutar beräkna fysiken ifall användaren har pausat simulationen
        if not state.is_paused: 
            state.step(delta_time=dt, iterations=RESOLUTION_ITERATIONS)
            state.handle_collisions()
            experiment_end_time = time.time() # NOTE: gjord för experiment
            experiment_start_time = current_experiment_start_time
        
        stop_watch(view_model, experiment_start_time, experiment_end_time) # NOTE: gjord för experiment

        view_model.render_or_uptade_selected_object_related()

        view_model.render_objects(state.objects)

        view_model.render_ui(ui_manager)

        view_model.update(ui_refresh_rate)

        # state.create_object(position=Vector2D(550,1000), with_gravity=True)

    pygame.quit()


# NOTE: Allt under förutom main loopen är slarvig kod för att utföra experiment
def experiment_code(state):
    if len(state.objects) > 0:
        if state.objects[-1].position.y < 100 + ORIGIN[1]:
            state.is_paused = True

def stop_watch(view_model, experiment_start_time, experiment_end_time):
        view_model.render_text(
                    f"Stopwatch: {experiment_end_time - experiment_start_time}",
                    BLACK,
                    (10, 1000),
                    20,
                )

if __name__ == "__main__":
    main()


    