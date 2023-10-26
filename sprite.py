import pygame
from pygame.locals import *
from random import choices, randint

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
        self.kill()
        del self.rect
    
    def moveto(self, x, y):
        self.rect.x = x
        self.rect.y = y
    

#[Temp player sprite] =================================================================
class Player(Sprite):
    def __init__(self, screen, colour, width, height):
        super().__init__(screen, colour, width, height, "player")

        self.speed = 3
        self.sprint = False
        self.jittering = [1, 0]
    
    def moveLeft(self):
        self.rect.x -= self.speed
        self.moved = True

    def moveRight(self):
        self.rect.x += self.speed
        self.moved = True
    
    def moveUp(self):
        self.rect.y -= self.speed
        self.moved = True
    
    def moveDown(self):
        self.rect.y += self.speed
        self.moved = True

    def handle_movement(self, keys, fatigued):
        self.moved = False

        if choices((True, False), self.jittering[0 : 2], k = 1)[0]:
            if keys[K_SPACE] and not fatigued:
                self.speed = 8
                self.sprint = True
            else:
                self.speed = 3
                self.sprint = False


            if keys[K_LEFT]:
                self.moveLeft()
            if keys[K_RIGHT]:
                self.moveRight()
            if keys[K_UP]:
                self.moveUp()
            if keys[K_DOWN]:
                self.moveDown()
        else:
            randMovementChoice = randint(0, 4)

            maxJitterSpeed = self.jittering[2]
            if maxJitterSpeed >= 3:
                if fatigued or choices((True, False), (maxJitterSpeed, 2), k = 1)[0]:
                    self.speed = 3
                    self.sprint = False
                else:
                    self.speed = maxJitterSpeed
                    self.sprint = True
            else:
                self.speed = maxJitterSpeed


            if randMovementChoice == 1:
                self.moveLeft()
            if randMovementChoice == 2:
                self.moveRight()
            if randMovementChoice == 3:
                self.moveUp()
            if randMovementChoice == 4:
                self.moveDown()
#======================================================================================