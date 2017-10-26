import pygame as pgm
from pygame import *

from GUIelements import *
from MainMenu import *
from Simulator import Simulator

pgm.init()

screen = pgm.display.set_mode(win_size)
pgm.display.set_caption("Gravity")
pgm.display.set_icon(Load("pics\icon.png"))

MM = MainMenu(screen)
MM.act = True
MM.draw((-1, -1))
pgm.display.update()

Sim = Simulator(screen)

time = 0

run = True
while run:

    pass_one = False
    
    for e in pgm.event.get():
        
        if e.type == pgm.QUIT:
            
            run = False

        if e.type == pgm.MOUSEMOTION:
            
            mouse = pgm.mouse.get_pos()

            if MM.act:

                MM.draw(mouse)

                pgm.display.update()

            if Sim.act:

                Sim.on_m_motion(pgm.mouse.get_pos())

        if e.type == pgm.MOUSEBUTTONDOWN:

            if Sim.act:

                Sim.on_mb_down(pgm.mouse.get_pos())

                if Sim.menu.act:
                        
                    if (Sim.menu.buttons[1].onit(mouse) and
                        Sim.menu.buttons[1].act):

                        Sim.act = False
                        MM.act = True

                        for b in MM.buttons:

                            b.act = True
                            
                        pass_one = True
                        
            if MM.act and not pass_one:
                
                if (MM.buttons[0].onit(mouse) and
                    MM.buttons[0].act):

                    run = False

                if (MM.buttons[1].onit(mouse) and
                    MM.buttons[1].act):

                    MM.act = False

                    Sim.planets = []
                    Sim.traces.fill(BLACK)
                    
                    Sim.act = True
                    Sim.motion = True
                    Sim.time = 0

        if e.type == pgm.MOUSEBUTTONUP:

            if Sim.act:

                Sim.on_mb_up(pgm.mouse.get_pos())

        if e.type==pgm.KEYDOWN:

            Sim.on_key(e.key)

    Sim.sequence()
    pgm.display.update()

    time += TIMERATE

pgm.quit()
