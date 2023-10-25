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

        self.update(0)

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

        self.set_colours(red, green, blue)
    
    def set_colours(self, red, green, blue):
        self.colour = (red, green, blue)
    
    def set_warningBorder(self, warningFlag):
        if warningFlag:
            self.outlineWidth = 2
            self.outlineColour = (255, 0, 0)
        else:
            self.outlineWidth = 1
            self.outlineColour = (100, 100, 100)

    def update(self, valueChange):
        self.value += valueChange

        dataText_text = self.get_dataText_text()

        self.bar.width = self.get_barWidth()

        self.dataText = self.data_font.render(dataText_text, True, (255, 255, 255))
        self.text_rect = self.dataText.get_rect(center = (self.x + self.width // 2, self.y + self.height // 2))

    def draw(self):
        pygame.draw.rect(self.screen, (150, 150, 150), self.barContainerBg)
        pygame.draw.rect(self.screen, self.outlineColour, self.barContainerOutline, self.outlineWidth)
        pygame.draw.rect(self.screen, (int(self.colour[0]), int(self.colour[1]), int(self.colour[2])), self.bar)

        self.screen.blit(self.dataText, self.text_rect)


class SanityBar(dataBar):
    def __init__(self, screen, x, y):
        sanity = 100
        self.regenTicker = 0

        #(0, 176, 24)
        super().__init__(screen, sanity, sanity, (0, 200, 0), x, y)

    def update(self, valueChange):
        newValue = round(self.value + valueChange, 1)

        if valueChange < 0:
            direction = 1
        elif valueChange > 0:
            direction = -1

        if newValue <= 0: #0%
            self.value = 0
            print("gameEnd")
        elif newValue <= 5: #5%
            #0-5
            self.set_colours(255, 0, 0)
            #self.update_colours(-2 * direction, -1 * direction, 0)
        elif newValue <= 10: #valueRatio >= 8: #12.5%
            #5-10
            #self.update_colours(0, -10 * direction, -6 * direction)
            j = ((10 - 5) / 0.2)
            self.update_colours(0, direction * ((0 - 127) / j), direction * ((0 - 66) / j))
            #(255, 17, 0)
        elif newValue <= 25: #self.maxvalue / newValue >= 4: #25%
            #10-25
            #self.update_colours(10 * direction, -1 * direction, -1 * direction)
            j = ((25 - 10) / 0.2)
            self.update_colours(direction * (255 / j), direction * ((127 - 200) / j), direction * ((66 - 24) / j))
            #(255, 127, 66)
        else:
            #25-100
            #(0, 176, 24)
            self.set_colours(0, 200, 0)
        print(self.colour, newValue)
        
        self.regenTicker = 0
        super().update(valueChange)

        if int(self.value) == 0:
            self.set_warningBorder(True)
        else:
            self.set_warningBorder(False)

class StaminaBar(dataBar):
    def __init__(self, screen, x, y):
        stamina = 100
        self.fatigued = False

        super().__init__(screen, stamina, stamina, (5, 213, 250), x, y)
    
    def update(self, valueChange):
        super().update(valueChange)

        if self.fatigued and self.value > 10:
            self.fatigued = False
            self.set_warningBorder(False)
        elif int(self.value) == 0:
            self.fatigued = True
            self.set_warningBorder(True)
