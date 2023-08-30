import pygame

from pyng.space.phys_world import PhysWorld
from pyng.space.grid import Grid

from pyng.config import FPS, RED



def main():
    pygame.init()
    screen = pygame.display.set_mode((1280 / 2, 720 / 2))
    clock = pygame.time.Clock()

    world = PhysWorld(Grid(screen.get_width(), screen.get_height()))

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
