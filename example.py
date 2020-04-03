# https://realpython.com/pygame-a-primer/

import pygame


WIDTH = 500
HEIGHT = 500


class Person:
    def __init__(self):
        self.position = None

    def _init_position(self):
        pass

    def move(self):
        pass

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (259, 250), 75)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Init screen
    running = True
    # x, y = 0, 0
    p = Person()
    while running:  # start game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))  # Background
        p.move()
        p.draw(screen)
        # pygame.draw.circle(
        #     screen, (0, 0, 255), (x, y), 75
        # )  # circle(screen, color, (x,y), radius)
        pygame.display.flip()  # actually draw to screen
        # x += 1
        # y += 1
    pygame.quit()
