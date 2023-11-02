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
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id == "#manipulate_view_changer_button":
                return "manipulate_mode"
            
            if  event.ui_object_id == "#spawner_view_changer_button":
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

    # if pygame.mouse.get_pressed()[0] == True:  # Kollar ifall mouse1 är nedtryckt
    #     return "mouse 1"


def delegate_event(event, state, view_model, UI_manager):
    if event is None:
        return

    if event == "mouse 1":
        state.parse_mouse_click(
            Vector2D(*(view_model.convert_coordinates(*pygame.mouse.get_pos())))
        )
        return

    #elif isinstance(event, str):
    #    state.player_chosen_radius = int(event)
    
    if event == "manipulate_mode":
        view_model.ui_mode = False
        UI_manager.clear_and_reset()
        view_model.show_manipulate_editor()
        view_model.show_mode_buttons()
        return
        
    
    if event == "spawner_mode":
        view_model.ui_mode = True
        UI_manager.clear_and_reset()
        view_model.show_spawn_editor()
        view_model.show_mode_buttons()
        return
    
    if event == "rect":
        view_model.shape = "rect"
        UI_manager.clear_and_reset()
        view_model.show_spawn_editor()
        view_model.show_mode_buttons()
        return

    if event == "circle":
        view_model.shape = "circle"
        UI_manager.clear_and_reset()
        view_model.show_spawn_editor()
        view_model.show_mode_buttons()
        return
    
    if event == "spawn":
        return