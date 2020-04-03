import pygame
import random
import numpy as np

WIDTH = 500
HEIGHT = 500
RADIUS = 5

MAX_VELOCITY = 5
MAX_ACCELERATION = 5
POPULATION_SIZE = 200
INFECTION_PROBABILITY = 0.2
SICK_TIME = 400

BACKGROUND_COLOR = (0, 0, 0)

STATE_COLOR = {"healthy": (0, 255, 0), "sick": (255, 0, 0), "cured": (0, 0, 255)}


class Person:
    def __init__(self):
        self.position = None
        self.velocity = None
        self.state = "healthy"
        self.timer = None
        self._init_position()
        self._init_velocity()

    def _init_position(self):
        self.position = np.array(
            [np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT)]
        )

    def _init_velocity(self):
        self.velocity = np.array(
            [
                np.random.randint(-MAX_VELOCITY, MAX_VELOCITY + 1),
                np.random.randint(-MAX_VELOCITY, MAX_VELOCITY + 1),
            ]
        )

    def _limit_velocity(self):
        if self.velocity[0] > MAX_VELOCITY:
            self.velocity[0] = MAX_VELOCITY
        elif self.velocity[0] < -MAX_VELOCITY:
            self.velocity[0] = -MAX_VELOCITY
        elif self.velocity[1] > MAX_VELOCITY:
            self.velocity[1] = MAX_VELOCITY
        elif self.velocity[1] < -MAX_VELOCITY:
            self.velocity[1] = -MAX_VELOCITY

    def _check_boundaries(self):
        if self.position[0] < 0:
            self.velocity[0] *= -1
        if self.position[0] > WIDTH + 1:
            self.velocity[0] *= -1
        if self.position[1] > HEIGHT + 1:
            self.velocity[1] *= -1
        if self.position[1] < 0:
            self.velocity[1] *= -1

    def draw(self, screen):
        pygame.draw.circle(
            screen, STATE_COLOR[self.state], tuple(self.position), RADIUS
        )

    def _distance(self, a, b):
        return np.linalg.norm(a - b)

    def infect(self, others):
        for o in others:
            if (
                self.state == "healthy"
                and self != o
                and self._distance(self.position, o.position) < 2 * RADIUS
                and o.state == "sick"
            ):
                if random.random() < INFECTION_PROBABILITY:
                    self.state = "sick"
                    self.timer = SICK_TIME

    def reduce_timer(self):
        self.timer -= 1
        if self.timer == 0:
            self.state = "cured"

    def move(self):
        acc = np.array(
            [
                np.random.randint(-MAX_ACCELERATION, MAX_ACCELERATION + 1),
                np.random.randint(-MAX_ACCELERATION, MAX_ACCELERATION + 1),
            ]
        )
        self.velocity += acc
        self._limit_velocity()
        self._check_boundaries()
        self.position = np.add(self.position, self.velocity).astype(int)


class Population:
    def __init__(self):
        self.population = [Person() for i in range(POPULATION_SIZE)]
        self.sick_list = []

    def move(self):
        for p in self.population:
            p.move()

    def draw(self, screen):
        for p in self.population:
            p.draw(screen)

    def get_sick_list(self):
        self.sick_list = [p for p in self.population if p.state == "sick"]

    def infect(self):
        self.get_sick_list()
        for p in self.sick_list:
            p.reduce_timer()
        self.get_sick_list()
        for p in self.population:
            p.infect(self.sick_list)

    def random_infect(self):
        rand = random.randint(0, POPULATION_SIZE - 1)
        self.population[rand].state = "sick"
        self.population[rand].timer = SICK_TIME


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    running = True
    pop = Population()
    pop.random_infect()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BACKGROUND_COLOR)
        pop.move()
        pop.infect()
        pop.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
