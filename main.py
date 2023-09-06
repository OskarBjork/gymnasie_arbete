# TODO: Ta bort all third-part dependencies

import time

import pygame

from pyng.space.phys_world import PhysWorld
from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import TwoDimensionalVector
from pyng.space.interface.view_model import ViewModel
from pyng.space.data.space_analyzer import SpaceAnalyzer
from pyng.config import FPS, RED, BLACK
from pyng.time.events.event_handler import EventHandler

def main():
    pygame.init()

    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    world = PhysWorld(screen_width, screen_height)
    space_analyzer = SpaceAnalyzer()

    event_handler = EventHandler()

    view_model = ViewModel(screen)

    obj = PhysObj(10, (255, 0, 0), TwoDimensionalVector(500, 250))
    world.add_object(obj)

    screen.fill((0, 0, 0))
    running = True
    prev_time = time.time()
    while running:
        clock.tick(FPS)
        now = time.time()
        dt = now - prev_time
        prev_time = now

        screen.fill(BLACK)
        event_handler.handle_events(pygame.event.get())

        space_analyzer.analyze(world)

        world.step(dt)
        view_model.render_objects(world.objects)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
