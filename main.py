import pygame

from pyng.space.phys_world import PhysWorld
from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import TwoDimensionalVector
from pyng.space.interface.view_model import ViewModel
from pyng.space.data.state import State
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

    state = State()

    state.create_objects(world)

    running = True
    while running:
        screen.fill(BLACK)
        event_handler.handle_events(pygame.event.get())

        space_analyzer.analyze(world)

        view_model.render_objects(world.objects)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
