import pygame
from pygame.locals import *
from sprite import Sprite, Player
from GuiElements import SanityBar, StaminaBar
from camera import Camera
from json import load

class GameEngine:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 700

        pygame.init()

        self.abs_origin_vect = pygame.math.Vector2()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("MCS Simulator")

        self.gamecamera = Camera(self.screen_width, self.screen_height)

        self.sanity = 100
        self.stamina = 100
        self.inventory = []

        self.damage_dealing = 0
        self.damage_dealing_tickLimit = 10

        #[Temp json handling elements] =======================================
        with open("settings.json", "r") as f:
            settingsDict = load(f)
        
        self.settingsLibrary = settingsDict["gui"]
        #=====================================================================


        #[Temp virtual elements] =============================================
        self.enitities = {
            "obj1": {
                "colour": (0, 255, 0), 
                "x": 30, 
                "y": 10, 
                "width": 30, 
                "height": 30, 
                "damage": 5
            }, 
            "obj2": {
                "colour": (0, 255, 0), 
                "x": 550, 
                "y": 250, 
                "width": 30, 
                "height": 30, 
                "damage": 5
            },
            "obj3": {
                "colour": (255, 255, 0), 
                "x": 80, 
                "y": 10, 
                "width": 30, 
                "height": 30, 
                "damage": 10
            },
            "obj4": {
                "colour": (255, 255, 0), 
                "x": 250, 
                "y": 600, 
                "width": 30, 
                "height": 30, 
                "damage": 10
            }, 
            "obj5": {
                "colour": (255, 165, 0), 
                "x": 130, 
                "y": 10, 
                "width": 30, 
                "height": 30, 
                "damage": 20
            }, 
            "obj6": {
                "colour": (200, 165, 0), 
                "x": 180, 
                "y": 10, 
                "width": 30, 
                "height": 30, 
                "damage": 30
            }, 
            "obj7": {
                "colour": (150, 80, 0), 
                "x": 230, 
                "y": 10, 
                "width": 30, 
                "height": 30, 
                "damage": 40
            }, 
            "obj8": {
                "colour": (120, 0, 0), 
                "x": 280, 
                "y": 10, 
                "width": 30, 
                "height": 30, 
                "damage": 50
            }, 
            "obj9": {
                "colour": (0, 0, 0), 
                "x": 330, 
                "y": 10, 
                "width": 30, 
                "height": 30, 
                "damage": 80
            }, 
            "obj10": {
                "colour": (0, 0, 0), 
                "x": 300, 
                "y": 1000, 
                "width": 30, 
                "height": 30, 
                "damage": 80
            }
        }
        self.mappedEntities = []
        #=====================================================================

    def create_sprite(self, entityKey, colour, x, y, width, height):
        self.mappedEntities.append(entityKey)

        sprite = Sprite(self.screen, colour, width, height, entityKey)
        self.gamecamera.add(sprite)
        sprite.spawn(x, y, self.abs_origin_vect)
    
    def xy_to_abs(self, x, y):
        abs_x = x - self.abs_origin_vect.x
        abs_y = y - self.abs_origin_vect.y

        return abs_x, abs_y

    def abs_to_xy(self, abs_x, abs_y):
        x = abs_x + self.abs_origin_vect.x
        y = abs_y + self.abs_origin_vect.y

        return x, y

    def isin_screen(self, abs_x, abs_y, width, height):
        x, y = self.abs_to_xy(abs_x, abs_y)

        inScreenFlag = (
            x + width < 0
            or x > self.screen_width
            or y + height < 0
            or y > self.screen_height
        )
        return not inScreenFlag

    def update_stamina(self):
        if self.player.speed == 8 and self.player.moved:
            self.staminaBar.update(-0.5)
        elif self.staminaBar.value < self.staminaBar.maxvalue:
            self.staminaBar.update(0.1)
        
    def update_sanity(self):
        if self.damage_dealing_tickLimit == 0:
            self.damage_dealing_tickLimit = 10

        if self.damage_dealing_tickLimit < 10 and self.sanityBar.value > 0:
            valueChange = (self.damage_dealing / self.damage_dealing_tickLimit)
            self.damage_dealing -= valueChange

            self.sanityBar.update(-valueChange)

            self.damage_dealing_tickLimit -= 1

        for entity in self.gamecamera.sprites():
            if entity.entityKey != "player" and self.player.rect.colliderect(entity.rect):
                entity.despawn()

                if self.sanityBar.value > 0:
                    #========================
                    self.damage_dealing += self.enitities[entity.entityKey]["damage"]
                    #========================

                    valueChange = (self.damage_dealing / self.damage_dealing_tickLimit)
                    self.damage_dealing -= valueChange

                    self.sanityBar.update(-valueChange)

                    self.damage_dealing_tickLimit -= 1
        
        if self.sanityBar.value < self.sanityBar.maxvalue:
            if self.sanityBar.regenTicker < self.settingsLibrary["ticker"]["stamina"]:
                self.sanityBar.regenTicker += 1
            else:
                self.sanityBar.update(0.2)

    def update_inventory(self, item):
        self.inventory.append(item)

    def run(self):
        self.clock = pygame.time.Clock()

        self.sanityBar = SanityBar(self.screen, 30, self.screen_height - 50)
        self.staminaBar = StaminaBar(self.screen, 30, self.screen_height - 30)


        #[Temp player sprite] =================================================================
        self.player = Player(self.screen, (255, 0, 0), 30, 30)
        self.gamecamera.add(self.player)
        x_pos = (self.screen_width - self.player.width) // 2
        y_pos = (self.screen_height - self.player.height) // 2
        self.player.spawn(x_pos, y_pos, self.abs_origin_vect)
        #======================================================================================

        #i = 0
        while True:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            

            keys = pygame.key.get_pressed()
            self.player.handle_input(keys, self.staminaBar.fatigued)

            self.gamecamera.correct_offsets(self.abs_origin_vect, self.player)

            for sprite in self.gamecamera.sprites():
                if sprite.entityKey != "player" and not self.isin_screen(sprite.abs_x, sprite.abs_y, sprite.rect.width, sprite.rect.height):
                    sprite.despawn()
                    self.mappedEntities.remove(sprite.entityKey)

            #[Temp virtual handling code] ==============================================
            for entityKey, entity in self.enitities.items():
                x = entity["x"]
                y = entity["y"]
                width = entity["width"]
                height = entity["height"]
                if self.isin_screen(x, y, width, height) and entityKey not in self.mappedEntities:
                    self.create_sprite(entityKey, entity["colour"], x, y, width, height)
            #===========================================================================

            self.gamecamera.draw()

            # Draw inventory items
            for item in self.inventory:
                item.draw()
            
            self.update_stamina()
            self.update_sanity()

            self.sanityBar.draw()
            self.staminaBar.draw()

            pygame.display.flip()

            self.clock.tick(60)



if __name__ == "__main__":
    game = GameEngine()
    game.run()