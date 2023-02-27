import pygame
import pytmx
import os
import Box2D

class GameObject:
    def update(self):
        pass

    def draw(self, screen):
        pass


class PlayerObject(GameObject):
    def __init__(self, position=(0, 0)):
        self.position = position

    def update(self):
        self.position = (self.position[0] + 1, self.position[1])

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, 10)