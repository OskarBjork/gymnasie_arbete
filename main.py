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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(RED)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
