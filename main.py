import time

import pygame

from pyng.space.phys_world import PhysWorld
from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import TwoDimensionalVector

FPS = 60
RED = (255, 0, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280 / 2, 720 / 2))
    clock = pygame.time.Clock()

    world = PhysWorld()

    running = True
    prev_time = time.time()
    while running:
        clock.tick(FPS)
        now = time.time()
        dt = now - prev_time
        prev_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(RED)

        world.step(dt)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
