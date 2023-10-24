import pygame
from pygame.locals import *

class Camera(pygame.sprite.Group):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.offset_vec = pygame.math.Vector2()

        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def correct_offsets(self, abs_origin_vect, player):
        self.offset_vec.x = player.rect.centerx - self.screen_width // 2
        self.offset_vec.y = player.rect.centery - self.screen_height // 2

        abs_origin_vect.x -= self.offset_vec.x
        abs_origin_vect.y -= self.offset_vec.y

        for sprite in self.sprites():
            sprite.rect.topleft -= self.offset_vec

            
    def draw(self):
        for sprite in self.sprites():
            sprite.draw()
