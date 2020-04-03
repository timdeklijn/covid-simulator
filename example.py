# https://realpython.com/pygame-a-primer/
# NEVER CALL PYGAME SCRIPT pygame.py !!!!

# TODO: Social Distancing? bonus

import pygame
import numpy as np
import matplotlib.pyplot as plt

# Screen settings
WIDTH = 500
HEIGHT = 500
RADIUS = 10

# Simulation settings
MAX_VELOCITY = 4
MAX_ACCELERATION = 5
POPULATION_SIZE = 100
INFECTION_PROBABILITY = 0.2
INFECTION_RADIUS = 2.5 * RADIUS
INFECTION_TIME = 100

# colors
BACKGROUND = (150, 150, 150)
STATE_COLOR = {0: (0, 255, 0), 1: (255, 0, 0), 2: (255, 255, 0)}


class Data:
    def __init__(self):
        self.healthy = []
        self.infected = []
        self.removed = []

    def add_stats(self, healthy, infected, removed):
        self.healthy.append(healthy)
        self.infected.append(infected)
        self.removed.append(removed)

    def plot(self):
        x = range(len(self.healthy))
        plt.plot(x, self.healthy, label="healthy")
        plt.plot(x, self.infected, label="infected")
        plt.plot(x, self.removed, label="removed")
        plt.legend()
        plt.show()


class Person:
    def __init__(self):
        self.position = self._init_position()
        self.velocity = self._init_velocity()
        self.state = 0  # 0 : healthy, 1 : infected, 2 : removed
        self.timer = None

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

        # if self.state != 1:
        #     self.velocity = np.add(self.velocity, acc)
        # else:
        #     self.velocity = np.array(
        #         [np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])]
        # )
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
                h.timer = INFECTION_TIME


class Population:
    def __init__(self):
        self.population = [Person() for _ in range(POPULATION_SIZE)]
        self.infected = []
        self.healthy = []
        self.data = Data()
        self.done = False
        self._patient_zero()

    def _patient_zero(self):
        self.population[0].state = 1
        self.population[0].timer = INFECTION_TIME

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
            if (
                np.random.rand() < INFECTION_PROBABILITY
            ):  # Less realistic, but less loops in simulation
                p.spread_infection(self.healthy)

    def heal(self):
        for p in self.infected:
            p.timer -= 1
            if p.timer == 0:
                p.state = 2

    def add_stats(self):
        self.data.add_stats(
            len(self.healthy),
            len(self.infected),
            len([p for p in self.population if p.state == 2]),
        )

    def check_done(self):
        if len(self.infected) == 0:
            self.done = True


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Init screen
    running = True
    pop = Population()
    c = 0
    while running:  # start game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pop.done:
                running = False
        screen.fill(BACKGROUND)  # Background
        pop.move()
        pop.infect()
        pop.heal()
        pop.check_done()
        pop.draw(screen)
        if c % 30 == 0:
            pop.add_stats()
        pygame.display.flip()  # actually draw to screen
        clock.tick(30)
        c += 1
    pygame.quit()
    pop.data.plot()