from math import sqrt
from random import randint as rnd
import pygame as pgm
from pygame import *

#from time import sleep as slp

# Checks if coordinates are inside rectangular area
def twoD_in(pos,area):
    if (area[0]<=pos[0]<=area[2])and(area[1]<=pos[1]<=area[3]):
        return 1
    return 0

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
                return 1
    return 0

# Initials
wh = 1000
ww = 1000

cx = ww//2
cy = wh//2

pgm.init()

scrn = pgm.display.set_mode((wh,ww))
pgm.display.set_caption('Gravity')

space=Surface((wh,ww))
space.set_colorkey((0,0,0))

# Planet data structure: [x,y,xv,yv,xa,ya,m,color,r]
planets = []

traces = Surface((wh,ww))
traces.fill((0,0,0))

# Labels
pen = pgm.font.SysFont("monospace", 15)
mpen = pgm.font.SysFont("monospace", 13)
spen = pgm.font.SysFont("monospace", 10)
upen = pgm.font.SysFont("monospace", 14)
pause_label = pen.render('hit space to stop',1,(150,220,250))
# Menu
menu_area = (ww-200,180,ww-100,300)
menu_label = mpen.render('CLICK TO:',1,(150,220,250))
opt_norm = pen.render('Normalize',1,(150,220,250))
opt_norm_area = (ww-200,220,ww-119,232)
opt_clear = pen.render('Clear',1,(150,220,250))
opt_clear_area = (ww-200,200,ww-155,212)
opt3 = spen.render('',1,(150,220,250))
# Menu underlayer
opt_clear_ul = pen.render('Clear',1,(100,250,150))
uclear = 0
opt_norm_ul = pen.render('Normalize',1,(100,250,150))
unorm = 0

grows = 0
ini = 1
act = 1
while ini:
    space.fill((0,0,0))
    
    # Check on collision and merge if it is
    if act == 1:
        while merge(planets):
            pass
    
    for e in pgm.event.get():
        
        if e.type == pgm.QUIT:
            ini = 0
            
        if e.type == pgm.MOUSEBUTTONDOWN:
            x_buf,y_buf = pgm.mouse.get_pos()
            if not(twoD_in((x_buf,y_buf),menu_area)):
                r0 = 1
                grows = 1
                xv_buf,yv_buf = x_buf,y_buf
                new_color = (rnd(0,255),rnd(0,255),rnd(0,255))

            # Clear tracefield    
            if twoD_in((x_buf,y_buf),opt_clear_area):
                traces.fill((0,0,0))
            # Normalize system    
            if twoD_in((x_buf,y_buf),opt_norm_area):
                normalize(planets)
                
        if e.type == pgm.MOUSEMOTION:
            xx,yy = pgm.mouse.get_pos()
            if grows == 1:
                xv_buf,yv_buf = xx,yy
            # Menu
            if act==0:
                if twoD_in((xx,yy),opt_clear_area):
                    uclear=1
                else:
                    uclear=0
                if twoD_in((xx,yy),opt_norm_area):
                    unorm=1
                else:
                    unorm=0                
                
        if e.type == pgm.MOUSEBUTTONUP:
            if grows == 1:
                grows = 0
                xv = (xv_buf-x_buf)/100
                yv = (yv_buf-y_buf)/100
                mass = r0**2
                planets.append([x_buf,y_buf,xv,yv,0,0,mass,new_color,r0])
                
        if e.type==pgm.KEYDOWN:

            # Pause
            if e.key == 32:
                if act == 1:
                    act = 0
                else:
                    act = 1
                    
    # Action
    if act == 1:
        # Calculations
          # Accelerations
        amount=len(planets)
        for i in range(amount):
            planets[i][4] = 0
            planets[i][5] = 0
        for i in range(amount):
            for j in range(i+1,amount):
                dx = planets[j][0]-planets[i][0]
                dy = planets[j][1]-planets[i][1]
                dss = dx**2+dy**2
                divider = (dss)*sqrt(dss)
                planets[i][4] += dx*planets[j][6]/divider
                planets[i][5] += dy*planets[j][6]/divider
                planets[j][4] -= dx*planets[i][6]/divider
                planets[j][5] -= dy*planets[i][6]/divider
          # Velocities
        for p in planets:
            p[2] += p[4]
            p[3] += p[5]

          # Coordinates
        for p in planets:
            p[0] += p[2]
            p[1] += p[3]
            
    # New planet
    if grows == 1:
        pgm.draw.circle(space,new_color,[x_buf,y_buf],round(r0),0)
        pgm.draw.line(space,new_color,[x_buf,y_buf],[xv_buf,yv_buf],1)
        r0 += 0.1

    # Draw planets
    for p in planets:
        coords = [round(p[0]),round(p[1])]
        pgm.draw.circle(space,p[7],coords,round(p[8]),0)
        pgm.draw.line(traces,p[7],coords,coords,1)

    scrn.blit(traces,(0,0))    
    scrn.blit(space,(0,0))
    if act == 1:
        scrn.blit(pause_label,(ww//2-50,5))
    else:
        # Menu
        scrn.blit(menu_label,(opt_clear_area[0],opt_clear_area[1]-30))
        if uclear == 1:
            scrn.blit(opt_clear_ul,(opt_clear_area[0],opt_clear_area[1]))
        if unorm == 1:
            scrn.blit(opt_norm_ul,(opt_norm_area[0],opt_norm_area[1]))
        scrn.blit(opt_clear,(opt_clear_area[0],opt_clear_area[1]))
        scrn.blit(opt_norm,(opt_norm_area[0],opt_norm_area[1]))
        
    pgm.display.update()
    #slp(0.001)

pgm.quit()
