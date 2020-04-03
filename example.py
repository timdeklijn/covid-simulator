# https://realpython.com/pygame-a-primer/
# NEVER CALL PYGAME SCRIPT pygame.py

import pygame
import numpy as np

WIDTH = 500
HEIGHT = 500

RADIUS = 20

MAX_VELOCITY = 5
MAX_ACCELERATION = 5


class Person:
    def __init__(self):
        self.position = self._init_position()
        self.velocity = self._init_velocity()

    def _init_velocity(self):
        x = np.random.randint(-MAX_VELOCITY, MAX_VELOCITY + 1)
        y = np.random.randint(-MAX_VELOCITY, MAX_VELOCITY + 1)
        return np.array([x, y])

    def _init_position(self):
        x = np.random.randint(0, WIDTH)
        y = np.random.randint(0, HEIGHT)
        return np.array([x, y])

    def _boundary_conditions(self):
        if self.position[0] < 0:
            self.position[0] = WIDTH - 1
        if self.position[0] > WIDTH:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = HEIGHT - 1
        if self.position[1] > HEIGHT:
            self.position[1] = 0

    def _limit_velocity(self):
        if self.velocity[0] < -MAX_VELOCITY:
            self.velocity[0] = -MAX_VELOCITY
        if self.velocity[0] > MAX_VELOCITY:
            self.velocity[0] = MAX_VELOCITY
        if self.velocity[1] < -MAX_VELOCITY:
            self.velocity[1] = -MAX_VELOCITY
        if self.velocity[1] > MAX_VELOCITY:
            self.velocity[1] = MAX_VELOCITY

    def move(self):
        # acc <- calc every frame
        x_acc = np.random.randint(-MAX_ACCELERATION, MAX_ACCELERATION + 1)
        y_acc = np.random.randint(-MAX_ACCELERATION, MAX_ACCELERATION + 1)
        acc = np.array([x_acc, y_acc])
        # vel <- update based on acc
        self.velocity = np.add(self.velocity, acc)
        self._limit_velocity()
        # pos <- update based on vel
        self.position = np.add(self.position, self.velocity)
        self._boundary_conditions()

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), tuple(self.position), RADIUS)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Init screen
    running = True
    p = Person()
    while running:  # start game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))  # Background
        p.move()
        p.draw(screen)
        pygame.display.flip()  # actually draw to screen
    pygame.quit()
