import sys

import pygame
import pygame_gui
from pygame.event import Event
from pyng.space.vectors import Vector2D
from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon


def handle_events(events: list[Event], UI_manager):
    for event in events:
        UI_manager.process_events(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if (
            event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED
        ):  # kan ändras till UI_TEXT_ENTRY_CHANGED när inmatningssäker
            if event.ui_object_id == "#radius_input":
                return {"input_type": "radius", "text": event.text}

            if event.ui_object_id == "#x_coordinate_input":
                return {"input_type": "x_val", "text": event.text}

            if event.ui_object_id == "#y_coordinate_input":
                return {"input_type": "y_val", "text": event.text}

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id == "#manipulate_view_changer_button":
                return "manipulate_mode"

            if event.ui_object_id == "#spawner_view_changer_button":
                return "spawner_mode"

            if event.ui_object_id == "#spawn_button":
                return "spawn"

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.text == "Rectangle":
                return "rect"

            if event.text == "Circle":
                return "circle"

        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if pygame.mouse.get_pressed()[0] == True:  # Kollar ifall mouse1 är nedtryckt
        return "mouse 1"


def delegate_event(event, state, view_model, ui_manager):
    if event is None:
        return

    if event == "mouse 1":
        state.parse_mouse_click(
            Vector2D(*(view_model.convert_coordinates(*pygame.mouse.get_pos())))
        )
        return

    if isinstance(event, dict):
        if event["input_type"] == "radius":
            state.player_chosen_radius = int(event["text"])

        if event["input_type"] == "x_val":
            state.player_chosen_x = int(event["text"])
            return

        if event["input_type"] == "y_val":
            state.player_chosen_y = int(event["text"])
            return

    if event == "manipulate_mode":
        view_model.ui_mode = False
        ui_manager.clear_and_reset()
        view_model.show_manipulate_editor()
        view_model.show_mode_buttons()
        return

    if event == "spawner_mode":
        view_model.ui_mode = True
        ui_manager.clear_and_reset()
        view_model.show_spawn_editor()
        view_model.show_mode_buttons()
        return

    if event == "rect":
        view_model.shape = "rect"
        # state.player_chosen_shape = Lägg till när det finns metod för rektanglar
        ui_manager.clear_and_reset()
        view_model.show_spawn_editor()
        view_model.show_mode_buttons()
        return

    if event == "circle":
        view_model.shape = "circle"
        state.player_chosen_shape = Circle
        ui_manager.clear_and_reset()
        view_model.show_spawn_editor()
        view_model.show_mode_buttons()
        return

    if event == "spawn":
        state.create_object()
        return
