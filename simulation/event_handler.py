import sys

import pygame
import pygame_gui
from pygame.event import Event
from pyng.space.vectors import Vector2D
from pyng.space.phys_obj import PhysObj, Circle, ConvexPolygon, Rectangle
from pyng.config import PIXELS_PER_METER

def handle_events(events: list[Event], ui_manager):
    move_force = Vector2D(0, 0)

    for event in events:
        ui_manager.process_events(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        match event.type:
            case pygame_gui.UI_TEXT_ENTRY_FINISHED:
                # kan ändras till UI_TEXT_ENTRY_CHANGED när inmatningssäker
                match event.ui_object_id:
                    case "#radius_input":
                        return {"input_type": "radius", "text": event.text}

                    case "#x_coordinate_input":
                        return {"input_type": "x_val", "text": event.text}

                    case "#y_coordinate_input":
                        return {"input_type": "y_val", "text": event.text}

                    case "#mass_input":
                        return {"input_type": "mass", "text": event.text}

                    case "#x_force_input":
                        return {"input_type": "x_force", "text": event.text}
                    
                    case "#y_force_input":
                        return {"input_type": "y_force", "text": event.text}
                    
                    case "#x_velocity_input":
                        return {"input_type": "x_velocity", "text": event.text}
                    
                    case "#y_velocity_input":
                        return {"input_type": "y_velocity", "text": event.text}
                    
                    case "#x_teleport_input":
                        return {"input_type": "x_teleport", "text": event.text}
                    
                    case "#y_teleport_input":
                        return {"input_type": "y_teleport", "text": event.text}
                    
                    case "#width_input":
                        return {"input_type": "rect_width", "text": event.text}
                    
                    case "#height_input":
                        return {"input_type": "rect_height", "text": event.text}
                
                
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
                    
                    case "#set_button":
                        return "set"
                    
                    case "#add_button":
                        return "add"
                    
                    case "#teleport_button":
                        return "teleport"
            
            case pygame_gui.UI_BUTTON_DOUBLE_CLICKED:         
                if event.ui_object_id == "#clear_button":
                    return "clear"
            
            case pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                match event.text:
                    case "Rectangle":
                        return "rect"

                    case "Circle":
                        return "circle"
                    
                    case "Polygon":
                        return "polygon"

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
        
    #Movement av valt objekt, inte säker på hur optimiserad denna process är 
        # if event.type == pygame.KEYDOWN:
        #     match event.key:
        #         case pygame.K_RIGHT:
        #             print("key Right pressed")
        #             move_force = move_force + Vector2D(1000, 0)
        #         case pygame.K_LEFT:
        #             print("key left pressed")
        #             move_force = move_force + Vector2D(-1000, 0)
        #         case pygame.K_UP:
        #             print("key up pressed")
        #             move_force = move_force + Vector2D(0, 1000)
        #         case pygame.K_DOWN:
        #             print("key down pressed")
        #             move_force = move_force + Vector2D(0, -1000)
        # if event.type == pygame.KEYUP:
        #     print("sysiphus")
        #     match event.key:
        #         case pygame.K_RIGHT:
        #             print("key Right released")
        #             move_force = move_force + Vector2D(-1000, 0)
        #         case pygame.K_LEFT:
        #             print("key left released")
        #             move_force = move_force + Vector2D(1000, 0)
        #         case pygame.K_UP:
        #             print("key up released")
        #             move_force = move_force + Vector2D(0, -1000)
        #         case pygame.K_DOWN:
        #             print("key down released")
        #             move_force = move_force + Vector2D(0, 1000)
            
    if pygame.mouse.get_pressed()[0] == True:  # Kollar ifall mouse1 är nedtryckt
        return "mouse 1"
    
    # Arrowkey Movement
    if move_force.x != 0 or move_force.y != 0:
        return {"input_type": "arrow_key", "move_force": move_force}

def delegate_event(event, state, view_model, ui_manager):
    if event is None:
        return

    if isinstance(event, dict):
        match event["input_type"]:
            case "radius":
                state.player_chosen_radius = int(event["text"])
                return
            
            case "mass":
                state.player_chosen_mass = float(event["text"])
                return
            
            case "x_val":
                state.player_chosen_x = int(event["text"])
                return
            case "y_val":
                state.player_chosen_y = int(event["text"])
                return
            
            case "x_force":
                state.player_force.x = int(event["text"])
                return
            case "y_force":
                state.player_force.y = int(event["text"])
                return
            
            case "x_velocity":
                state.player_velocity.x = float(event["text"]) * PIXELS_PER_METER
                return
            case "y_velocity":
                state.player_velocity.y = float(event["text"]) * PIXELS_PER_METER
                return
            
            case "x_teleport":
                state.player_teleport_coordinates.x = int(event["text"])
                return
            case "y_teleport":
                state.player_teleport_coordinates.y = int(event["text"])
                return  
            
            case "rect_width":
                state.player_rect_dimensions[0] = int(event["text"])
            case "rect_height":
                state.player_rect_dimensions[1] = int(event["text"])
            
            case "arrow_key":
                if not view_model.selected_object is None:
                    view_model.selected_object.force.x = event["move_force"].x
                    view_model.selected_object.force.y = event["move_force"].y
                return


            
    match event:
        case "mouse 1":
            state.parse_mouse_click(
                Vector2D(*(view_model.convert_coordinates(*pygame.mouse.get_pos()))),
                view_model,
            )
            return
        
        case "manipulate_mode":
            view_model.ui_mode = False
            ui_manager.clear_and_reset()
            view_model.show_manipulate_editor()
            view_model.show_mode_buttons()

            state.reset_manipulate_data() # clunky sätt att resetta data (alltså att man behöver lägga det manuellt i varje rätt event), kommer inte på något "finare" sätt att göra det utan att det blir för jobbigt
                                          # möjligt att göra för spawner data också
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

        case "polygon":
            view_model.shape = "polygon"
            state.player_chosen_shape = "circle"
            ui_manager.clear_and_reset()
            view_model.show_spawn_editor(state.spawn_gravity)
            view_model.show_mode_buttons()

        case "move":
            view_model.tool = "move"
            ui_manager.clear_and_reset()
            view_model.show_manipulate_editor()
            view_model.show_mode_buttons()

            state.reset_manipulate_data() # clunky sätt att resetta data (alltså att man behöver lägga det manuellt i varje rätt event), kommer inte på något "finare" sätt att göra det utan att det blir för jobbigt

        case "force":
            view_model.tool = "force"
            ui_manager.clear_and_reset()
            view_model.show_manipulate_editor()
            view_model.show_mode_buttons()

            state.reset_manipulate_data() # clunky sätt att resetta data (alltså att man behöver lägga det manuellt i varje rätt event), kommer inte på något "finare" sätt att göra det utan att det blir för jobbigt

        case "velocity":
            view_model.tool = "velocity"
            ui_manager.clear_and_reset()
            view_model.show_manipulate_editor()
            view_model.show_mode_buttons()

            state.reset_manipulate_data() # clunky sätt att resetta data (alltså att man behöver lägga det manuellt i varje rätt event), kommer inte på något "finare" sätt att göra det utan att det blir för jobbigt

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

        case "set":
            state.change_selected_object_attribute("set")

        case "add":
            state.change_selected_object_attribute("add")

        case "teleport":
            state.change_selected_object_attribute("teleport")