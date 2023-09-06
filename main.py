import time

import pygame

from pyng.space.phys_world import PhysWorld
from pyng.space.phys_obj import PhysObj
from pyng.space.vectors import TwoDimensionalVector

FPS = 60
RED = (255, 0, 0)


def convert_coordinates(vec: TwoDimensionalVector) -> (float, float):
    return vec.x, (1280 / 2) - vec.y

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280 / 2, 720 / 2))
    clock = pygame.time.Clock()

    world = PhysWorld()
    obj = PhysObj(10, TwoDimensionalVector(500, 250), TwoDimensionalVector(1, 1), TwoDimensionalVector(1, 1))
    world.add_object(obj)

    screen.fill((0, 0, 0))
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

        world.step(dt)
        x, y = convert_coordinates(obj.position)
        pygame.draw.rect(screen, (255, 0, 0), (x, y, 20, 20))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
