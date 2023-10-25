import pygame
from pygame.locals import *

class dataBar:
    def __init__(self, screen, value, maxvalue, colour, x, y):
        self.width = 500
        self.height = 16

        self.screen = screen
        self.value = value
        self.maxvalue = maxvalue
        self.colour = colour
        self.outlineWidth = 1
        self.outlineColour = (100, 100, 100)

        self.x = x
        self.y = y

        self.barContainerBg = pygame.Rect(x, y, self.width, self.height)
        self.barContainerOutline = pygame.Rect(x, y, self.width, self.height)
        self.bar = pygame.Rect(x + 1, y + 1, self.get_barWidth(), self.height - 2)

        self.data_font = pygame.font.SysFont("Calibri", 15, bold = True)

        self.update(value)

    def get_barWidth(self):
        return int((self.value / self.maxvalue) * (self.width - 2))

    def get_dataText_text(self):
        return f"{int(self.value)} / {self.maxvalue}"
    
    def update_colour(self, colourValue, colourChange):
        if colourValue + colourChange > 255:
            return 255
        elif colourValue + colourChange < 0:
            return 0
        else:
            return colourValue + colourChange

    def update_colours(self, redChange, greenChange, blueChange):
        red = self.update_colour(self.colour[0], redChange)
        green = self.update_colour(self.colour[1], greenChange)
        blue = self.update_colour(self.colour[2], blueChange)

        self.colour = (red, green, blue)
    
    def set_warningBorder(self, warningFlag):
        if warningFlag:
            self.outlineWidth = 2
            self.outlineColour = (255, 0, 0)
        else:
            self.outlineWidth = 1
            self.outlineColour = (100, 100, 100)

    def update(self, newValue):
        self.value = newValue

        dataText_text = self.get_dataText_text()

        self.bar.width = self.get_barWidth()

        self.dataText = self.data_font.render(dataText_text, True, (255, 255, 255))
        self.text_rect = self.dataText.get_rect(center = (self.x + self.width // 2, self.y + self.height // 2))

    def draw(self):
        pygame.draw.rect(self.screen, (150, 150, 150), self.barContainerBg)
        pygame.draw.rect(self.screen, self.outlineColour, self.barContainerOutline, self.outlineWidth)
        pygame.draw.rect(self.screen, self.colour, self.bar)

        self.screen.blit(self.dataText, self.text_rect)


class SanityBar(dataBar):
    def __init__(self, screen, x, y):
        sanity = 100
        self.regenTicker = 0

        super().__init__(screen, sanity, sanity, (0, 176, 24), x, y)

    def update(self, newValue):
        if newValue <= 0: #0%
            self.value = 0
            print("gameEnd")
        elif int(newValue) <= 10: #5%
            #self.update_colour(153, 0, 0)
            self.update_colours(-2, -1, 0)
        elif self.maxvalue / newValue >= 8: #12.5%
            self.update_colours(0, -10, -6)
            #self.update_colour(255, 17, 0)
        elif self.maxvalue / newValue >= 4: #25%
            self.update_colours(10, -1, -1)
            #self.update_colour(255, 127, 66)
        #else:
            #self.update_colour(0, 176, 24)
        
        self.regenTicker = 0
        super().update(newValue)

        if int(self.value) == 0:
            self.set_warningBorder(True)
        else:
            self.set_warningBorder(False)

class StaminaBar(dataBar):
    def __init__(self, screen, x, y):
        stamina = 100
        self.fatigued = False

        super().__init__(screen, stamina, stamina, (5, 213, 250), x, y)
    
    def update(self, newValue):
        super().update(newValue)

        if self.fatigued and self.value > 10:
            self.fatigued = False
            self.set_warningBorder(False)
        elif int(self.value) == 0:
            self.fatigued = True
            self.set_warningBorder(True)
