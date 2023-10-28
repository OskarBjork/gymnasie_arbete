import sys

import pygame
import pygame_gui
from pygame.event import Event
from pyng.space.vectors import Vector2D


def handle_events(events: list[Event], UI_manager):
    for event in events:
        UI_manager.process_events(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if (
            event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED
            and event.ui_object_id == "#radius_input"
        ):
            print("Text entry finished. Text:", event.text)
            return event.text
        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if pygame.mouse.get_pressed()[0] == True:  # Kollar ifall mouse1 är nedtryckt
        return "mouse 1"


def delegate_event(event, state, view_model, UI_manager):
    if event is None:
        return

    if event == "mouse 1":
        state.parse_mouse_click(
            Vector2D(*(view_model.convert_coordinates(*pygame.mouse.get_pos())))
        )
        return

    elif isinstance(event, str):
        state.player_chosen_radius = int(event)
