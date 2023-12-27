import sys

import pygame
import pygame_gui
from pygame.event import Event
from pyng.space.vectors import Vector2D
from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon, Rectangle


def handle_events(events: list[Event], ui_manager):
    for event in events:
        ui_manager.process_events(event)
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

            if event.ui_object_id == "#mass_input":
                return {"input_type": "mass", "text": event.text}

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id == "#manipulate_view_changer_button":
                return "manipulate_mode"

            if event.ui_object_id == "#spawner_view_changer_button":
                return "spawner_mode"

            if event.ui_object_id == "#spawn_button":
                return "spawn"

        if event.type == pygame_gui.UI_BUTTON_DOUBLE_CLICKED:
            if event.ui_object_id == "#clear_button":
                return "clear"

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.text == "Rectangle":
                return "rect"

            if event.text == "Circle":
                return "circle"

            if event.text == "Move":
                return "move"

            if event.text == "Force":
                return "force"

            if event.text == "Velocity":
                return "velocity"

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
            Vector2D(*(view_model.convert_coordinates(*pygame.mouse.get_pos()))),
            view_model
        )
        return

    if isinstance(event, dict):
        if event["input_type"] == "radius":
            state.player_chosen_radius = int(event["text"])
            return

        if event["input_type"] == "mass":
            state.player_chosen_mass = int(event["text"])
            return
        if event["input_type"] == "x_val":
            state.player_chosen_x = int(event["text"])
            return

        if event["input_type"] == "y_val":
            state.player_chosen_y = int(event["text"])
            return

    match event:
        case "manipulate_mode":
            view_model.ui_mode = False
            ui_manager.clear_and_reset()
            view_model.show_manipulate_editor()
            view_model.show_mode_buttons()

        case "spawner_mode":
            view_model.ui_mode = True
            ui_manager.clear_and_reset()
            view_model.show_spawn_editor()
            view_model.show_mode_buttons()

        case "rect":
            view_model.shape = "rect"
            state.player_chosen_shape = Rectangle
            ui_manager.clear_and_reset()
            view_model.show_spawn_editor()
            view_model.show_mode_buttons()

        case "circle":
            view_model.shape = "circle"
            state.player_chosen_shape = Circle
            ui_manager.clear_and_reset()
            view_model.show_spawn_editor()
            view_model.show_mode_buttons()

        case "move":
            view_model.tool = "move"
            state.player_chosen_tool = "move"  # kan ändras i framtiden, lade bara till för jag tror det kommer behövas
            ui_manager.clear_and_reset()
            view_model.show_manipulate_editor()
            view_model.show_mode_buttons()

        case "force":
            view_model.tool = "force"
            state.player_chosen_tool = "force"  # kan ändras i framtiden, lade bara till för jag tror det kommer behövas
            ui_manager.clear_and_reset()
            view_model.show_manipulate_editor()
            view_model.show_mode_buttons()

        case "velocity":
            view_model.tool = "velocity"
            state.player_chosen_tool = "velocity"  # kan ändras i framtiden, lade bara till för jag tror det kommer behövas
            ui_manager.clear_and_reset()
            view_model.show_manipulate_editor()
            view_model.show_mode_buttons()

        case "clear":
            state.del_all_objects()

        case "spawn":
            state.create_object(obj_type=view_model.shape, manual_spawn=True)
