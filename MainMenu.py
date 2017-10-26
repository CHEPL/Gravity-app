import pygame as pgm
from pygame import *

from GUIelements import *

class MainMenu(scene):

    def __init__(self, surface):

        scene.__init__(self, surface)

        self.surface = surface

        self.statics.append(static(surface, (0, 0),
                                   "pics\\mainmenu\\back.png"))

        self.buttons.append(button(surface, (100, 900),
                                   "pics\\mainmenu\\exit_P.png",
                                   "pics\\mainmenu\\exit_A.png"))

        self.buttons[0].act = 1

        self.buttons.append(button(surface, (100, 50),
                                   "pics\\mainmenu\\new_P.png",
                                   "pics\\mainmenu\\new_A.png"))

        self.buttons[1].act = 1
