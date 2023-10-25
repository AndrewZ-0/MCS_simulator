import pygame
from pygame.locals import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, screen, colour, width, height, entityKey):
        super().__init__()

        self.screen = screen
        self.colour = colour
        self.width = width
        self.height = height

        self.entityKey = entityKey

    def spawn(self, abs_x, abs_y, abs_origin_vect):
        self.abs_x = abs_x
        self.abs_y = abs_y

        x = abs_x + abs_origin_vect.x
        y = abs_y + abs_origin_vect.y

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, self.rect)

    def despawn(self):
        del self.rect
    
    def moveto(self, x, y):
        self.rect.x = x
        self.rect.y = y
    

#[Temp player sprite] =================================================================
class Player(Sprite):
    def __init__(self, screen, colour, width, height):
        super().__init__(screen, colour, width, height, "player")

        self.speed = 3

    def handle_input(self, keys, stamina, fatigued):
        if keys[K_SPACE] and not fatigued:
            self.speed = 8
        else:
            self.speed = 3

        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed
#======================================================================================