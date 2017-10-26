from pygame import Surface
from pygame.image import load as Load
from pygame.transform import scale, chop
from random import randint as rint

from self_consts import *

#--------------------------------------------------Common elements
class static:
    
    def __init__(self, surface, coordinates, img):
        
        self.act = True

        self.place = (surface, coordinates)
        
        self.image = Load(img)

    def draw(self):

        if self.act:

            self.place[0].blit(self.image, self.place[1])
        
class button:

    def __init__(self, surface, coordinates, img1, img2):

        self.act = False

        self.place = (surface, coordinates)

        self.passive = Load(img1)
        self.p_coords = list(map(lambda c1, c2 : c1 - c2//2,
                                 self.place[1], self.passive.get_size()))
            
        self.active = Load(img2)
        self.a_coords = list(map(lambda c1, c2 : c1 - c2//2,
                                 self.place[1], self.active.get_size()))

        self.area = [[coordinates[0] - self.passive.get_size()[0]//2,
                      coordinates[0] + self.passive.get_size()[0]//2],
                     [coordinates[1] - self.passive.get_size()[1]//2,
                      coordinates[1] + self.passive.get_size()[1]//2]]

    def draw(self, mouse):

        if self.act:

            if self.onit(mouse):    
            
                self.place[0].blit(self.active, self.a_coords)
            
            else:
            
                self.place[0].blit(self.passive, self.p_coords)

    def onit(self, mouse):

        if not self.act:

            return False

        if ((self.area[0][0] < mouse[0] < self.area[0][1])and
            (self.area[1][0] < mouse[1] < self.area[1][1])):

            return True

        else:

            return False

class label:

    def __init__(self, surface, coordinates, font = None, text = None):

            self.act = False
        
            self.place = (surface, coordinates)

            if font:

                self.font = font

            else:

                self.font = DEFAULT_FONT

            if text:
                
                self.text = self.font.render(text, 1, DEFAULT_TEXT_COLOR)

            else:

                self.text = None     
            
            #self.coords = (self.place[1][0] - self.image.get_size()[0]//2,
            #               self.place[1][1] - self.image.get_size()[1]//2)

    def draw(self, text = None):

        if self.act:

            if text:

                self.text = self.font.render(text, 1, DEFAULT_TEXT_COLOR)

            self.place[0].blit(self.text, self.place[1])

class scene:

    def __init__(self, surface):

        self.surface = surface

        self.act = False

        self.statics = []

        self.labels = []

        self.buttons = []

    def draw(self, mouse):

        for s in self.statics:

            s.draw()
            
        for l in self.labels:

            l.draw()

        for b in self.buttons:

            b.draw(mouse)          

#--------------------------------------------------Common elements\
