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

        match event.type:
            case pygame_gui.UI_TEXT_ENTRY_FINISHED:
                # kan ändras till UI_TEXT_ENTRY_CHANGED när inmatningssäker
                if event.ui_object_id == "#radius_input":
                    return {"input_type": "radius", "text": event.text}

                if event.ui_object_id == "#x_coordinate_input":
                    return {"input_type": "x_val", "text": event.text}

                if event.ui_object_id == "#y_coordinate_input":
                    return {"input_type": "y_val", "text": event.text}

                if event.ui_object_id == "#mass_input":
                    return {"input_type": "mass", "text": event.text}
                
            case pygame_gui.UI_BUTTON_PRESSED:
                match event.ui_object_id:
                    case "#manipulate_view_changer_button":
                        return "manipulate_mode"

                    case "#spawner_view_changer_button":
                        return "spawner_mode"

                    case "#spawn_button":
                        return "spawn"
                    
                    case "#spawn_gravity_toggle_button":
                        return "toggle_spawn_gravity"
                    
                    case "#pause_button":
                        return "pause"
            
            case pygame_gui.UI_BUTTON_DOUBLE_CLICKED:         
                if event.ui_object_id == "#clear_button":
                    return "clear"
            
            case pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                match event.text:
                    case "Rectangle":
                        return "rect"

                    case "Circle":
                        return "circle"

                    case "Move":
                        return "move"

                    case "Force":
                        return "force"

                    case "Velocity":
                        return "velocity"
                
        # Jag vet inte hur man gör != i en match statement
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
            view_model,
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
            view_model.show_spawn_editor(state.spawn_gravity)
            view_model.show_mode_buttons()

        case "rect":
            view_model.shape = "rect"
            state.player_chosen_shape = "rect"
            ui_manager.clear_and_reset()
            view_model.show_spawn_editor(state.spawn_gravity)
            view_model.show_mode_buttons()

        case "circle":
            view_model.shape = "circle"
            state.player_chosen_shape = "circle"
            ui_manager.clear_and_reset()
            view_model.show_spawn_editor(state.spawn_gravity)
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

        case "toggle_spawn_gravity":
            if state.spawn_gravity:
                state.spawn_gravity = False
                view_model.spawn_gravity_toggle_button.set_text("Gravity: Off")
            else:
                state.spawn_gravity = True
                view_model.spawn_gravity_toggle_button.set_text("Gravity: On")

        case "pause":
            if state.is_paused:
                state.is_paused = False
            else:
                state.is_paused = True
