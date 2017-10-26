from random import randint as rnd
from math import sqrt
import pygame as pgm
from pygame import *

from GUIelements import *

# Checks if coordinates are inside rectangular area
def twoD_in(pos, area):
    if (area[0] <= pos[0] <= area[2]) and (area[1] <= pos[1] <= area[3]):
        return True
    return False

# Normilizes planets system so that mass centre does not move
def normalize(ps):
    
    # Mass of the system
    M = sum(p[6] for p in ps)

    # Components of the system impulse
    xpulse = sum(p[6]*p[2] for p in ps)
    ypulse = sum(p[6]*p[3] for p in ps)

    # Components of the system velocity
    dvx = xpulse/M
    dvy = ypulse/M
    
    for p in ps:
        p[2] -= dvx
        p[3] -= dvy
        
# Merges collided planets
def merge(ps):   
    amount = len(ps)
    for i in range(amount):
        for j in range(i+1,amount):
            if sqrt((ps[i][0]-ps[j][0])**2
                    +(ps[i][1]-ps[j][1])**2)<(ps[i][8]+ps[j][8]):
                M = ps[i][6]+ps[j][6]
                ps.append([(ps[i][0]*ps[i][6]+ps[j][0]*ps[j][6])/M,
                           (ps[i][1]*ps[i][6]+ps[j][1]*ps[j][6])/M,
                           (ps[i][2]*ps[i][6]+ps[j][2]*ps[j][6])/M,
                           (ps[i][3]*ps[i][6]+ps[j][3]*ps[j][6])/M,
                           0,0,M,
                           (round(ps[i][6]*ps[i][7][0]+ps[j][6]*ps[j][7][0])/M,
                            round(ps[i][6]*ps[i][7][1]+ps[j][6]*ps[j][7][1])/M,
                            round(ps[i][6]*ps[i][7][2]+ps[j][6]*ps[j][7][2])/M),
                           sqrt(M)])
                ps.pop(j)
                ps.pop(i)                
                return True
    return False

def recalculate(ps):

    # Accelerations
    amount = len(ps)
                            
    for i in range(amount):
                                
        ps[i][4] = 0
        ps[i][5] = 0
                                
    for i in range(amount):
                                
        for j in range(i + 1, amount):
                                    
            dx = ps[j][0] - ps[i][0]
            dy = ps[j][1] - ps[i][1]
            dss = dx**2 + dy**2
            divider = (dss) * sqrt(dss)
            
            ps[i][4] += G * dx * ps[j][6] / divider
            ps[i][5] += G * dy * ps[j][6] / divider
            ps[j][4] -= G * dx * ps[i][6] / divider
            ps[j][5] -= G * dy * ps[i][6] / divider
                                    
    # Velocities
    for p in ps:
                                
        p[2] += p[4] * PROPORTION
        p[3] += p[5] * PROPORTION

    # Coordinates
    for p in ps:
                                
        p[0] += p[2] * PROPORTION
        p[1] += p[3] * PROPORTION

class SimMenu(scene):

    def __init__(self, surface):

        scene.__init__(self, surface)

        self.statics.append(static(self.surface, ZERO,
                                   "pics\\simulatormenu\\back.png"))

        self.statics[0].image.set_alpha(None)
        self.statics[0].image.set_alpha(50)

        self.statics[0].act = True

        self.buttons.append(button(self.surface, (100, 50),
                                   "pics\\simulatormenu\\norm_P.png",
                                   "pics\\simulatormenu\\norm_A.png"))
        self.buttons[0].act = 1
        
        self.buttons.append(button(surface, (100, 900),
                                   "pics\\mainmenu\\exit_P.png",
                                   "pics\\mainmenu\\exit_A.png"))
        self.buttons[1].act = 1

        self.buttons.append(button(self.surface, (100, 150),
                                   "pics\\simulatormenu\\clean_P.png",
                                   "pics\\simulatormenu\\clean_A.png"))
        self.buttons[2].act = 1
      
class Simulator(scene):

    def __init__(self, surface):

        scene.__init__(self, surface)

        self.labels.append(label(surface, (50, 50)))

        self.labels.append(label(surface, (425, 30),
                                 text = "Hit space to pause"))

        self.labels[1].act = True
        
        # Planet data structure: [x,y,xv,yv,xa,ya,m,color,r]
        self.planets = []
        
        self.system = Surface(surface.get_size())
        self.system.set_colorkey((0,0,0))
        #self.system.fill((0,0,0))
        
        self.traces = Surface(surface.get_size())
        self.traces.fill(BLACK)

        self.motion = False
        self.growth = False
        self.r_growth = 0
        self.t_growth = -1
        
        self.time = 0

        self.x_down = -1
        self.y_down = -1
        self.x_mot = -1
        self.y_mot = -1
        self.x_up = -1
        self.y_up = -1

        self.new_color = (0, 0, 0)

        # Sim menu related

        self.menu = SimMenu(surface)
        
    def on_mb_down(self, mouse):

        if self.motion:

            self.growth = True
            self.r_growth = 0
            self.new_color = (rnd(50, 255), rnd(50, 255), rnd(50, 255))

            self.x_down, self.y_down = mouse
            self.t_down = self.time

        if self.menu.act:

            if self.menu.buttons[0].onit(mouse) and self.menu.buttons[0].act:
                
                normalize(self.planets)

            if self.menu.buttons[2].onit(mouse) and self.menu.buttons[2].act:
                
                self.traces.fill(BLACK)

                self.surface.fill(BLACK)
                self.surface.blit(self.system, ZERO)
                self.menu.draw((-1, -1))
                
                
    def on_m_motion(self, mouse):

        self.x_mot, self.y_mot = mouse

        if self.menu.act:

            self.surface.fill(BLACK)            

            self.surface.blit(self.traces, ZERO)
            self.surface.blit(self.system, ZERO)

            self.labels[0].draw("Time: {:.3f}".format(self.time))

            self.menu.draw(mouse)

    def on_mb_up(self, mouse):

        self.x_up, self.y_up = mouse

        if self.growth:

            self.growth = False
            
            self.planets.append([self.x_down,
                                 self.y_down,
                                 self.x_mot - self.x_down,
                                 self.y_mot - self.y_down,
                                 0,
                                 0,
                                 self.r_growth**2,
                                 self.new_color,
                                 self.r_growth])
            

    def on_key(self, key):

        if key == 32:

            if self.motion:

                self.motion = False

                self.menu.act = True
                self.menu.draw((-1, -1))

            else:

                self.motion = True

                self.menu.act  = False
                
        if key == 83 or key == 115:

            if self.labels[0].act:

                self.labels[0].act = False

            else:

                self.labels[0].act = True
                
    def sequence(self):

        if self.act:

            if self.motion:

                self.time += TIMERATE

                self.surface.fill(BLACK)
                self.system.fill(BLACK)

                while merge(self.planets):
                    pass
                
                recalculate(self.planets)

                for p in self.planets:
                    
                    coords = [round(p[0]),round(p[1])]
                    
                    pgm.draw.circle(self.system, p[7], coords, round(p[8]), 0)
                    
                    pgm.draw.line(self.traces, p[7], coords, coords, 1)

                if self.growth:

                    pgm.draw.line(self.system, self.new_color,
                                  [self.x_down, self.y_down],
                                  [self.x_mot, self.y_mot], 1)

                    pgm.draw.circle(self.system, self.new_color,
                                    [self.x_down, self.y_down],
                                    round(self.r_growth), 0)

                    self.r_growth += self.time - self.t_growth
                    

                self.surface.blit(self.traces, ZERO)
                self.surface.blit(self.system, ZERO)

                self.labels[1].draw()
                self.labels[0].draw("Time: {:.3f}".format(self.time))
