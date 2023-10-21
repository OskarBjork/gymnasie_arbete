import sys

import pygame
from pygame.event import Event


def handle_events(events: list[Event]):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if pygame.mouse.get_pressed()[0] == True:  # Kollar ifall mouse1 är nedtryckt
        return "mouse 1"
