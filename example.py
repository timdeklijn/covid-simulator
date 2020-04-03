# https://realpython.com/pygame-a-primer/
# NEVER CALL PYGAME SCRIPT pygame.py !!!!

# TODO: Heal/Remove individuals
# TODO: Social Distancing? bonus

import pygame
import numpy as np

# Screen settings
WIDTH = 500
HEIGHT = 500
RADIUS = 10

# Simulation settings
MAX_VELOCITY = 5
MAX_ACCELERATION = 5
POPULATION_SIZE = 100
INFECTION_PROBABILITY = 0.2
INFECTION_RADIUS = 3 * RADIUS

# colors
BACKGROUND = (150, 150, 150)
STATE_COLOR = {0: (0, 255, 0), 1: (255, 0, 0), 2: (255, 255, 0)}


class Person:
    def __init__(self):
        self.position = self._init_position()
        self.velocity = self._init_velocity()
        self.state = 0  # 0 : healthy, 1 : infected, 2 : removed

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
        pygame.draw.circle(
            screen, STATE_COLOR[self.state], tuple(self.position), RADIUS
        )

    def spread_infection(self, healthy_people):
        for h in healthy_people:
            d = np.linalg.norm(self.position - h.position)
            if d < INFECTION_RADIUS:
                h.state = 1


class Population:
    def __init__(self):
        self.population = [Person() for _ in range(POPULATION_SIZE)]
        self.infected = []
        self.healthy = []
        self._patient_zero()

    def _patient_zero(self):
        self.population[0].state = 1

    def draw(self, screen):
        for p in self.population:
            p.draw(screen)

    def move(self):
        for p in self.population:
            p.move()

    def infect(self):
        self.infected = [p for p in self.population if p.state == 1]
        self.healthy = [p for p in self.population if p.state == 0]
        for p in self.infected:
            if np.random.rand() < INFECTION_PROBABILITY:  # Less realistic, but less loops in simulation
                p.spread_infection(self.healthy)


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Init screen
    running = True
    pop = Population()
    while running:  # start game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BACKGROUND)  # Background
        pop.move()
        pop.infect()
        pop.draw(screen)
        pygame.display.flip()  # actually draw to screen
        clock.tick(30)
    pygame.quit()
