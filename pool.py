import pygame as pg
import numpy as np
from pygame.locals import *

pg.init()

win_size = (1600,800)
win=pg.display.set_mode(win_size, RESIZABLE)
pg.display.set_caption("Game")
bg_color = (255,255,255)
win.fill(bg_color)
run = True
table_size = (win_size[0]-200, win_size[0]/2-100)
ball_size = int(9*win_size[0]/704-225/88)
y_buffer = win_size[1]/2-win_size[0]/4+50
            

class Ball:
    def __init__(self, pos, color):
        self.velx = 0
        self.vely = 0
        self.posx = pos[0]
        self.posy = pos[1]
        self.color = color

    def move(self):
        self.posx += self.velx
        self.posy += self.vely
        self.velx *= 0.99
        self.vely *= 0.99
        
        if self.posx < 900/352:
            self.velx = abs(self.velx)
        elif self.posx > 200-900/352:
            self.velx = -abs(self.velx)
        
        if self.posy < 900/352:
            self.vely = abs(self.vely)
        elif self.posy > 100-900/352:
            self.vely = -abs(self.vely)
            
        if self.velx**2 + self.vely**2 <0.005:
            self.velx = 0
            self.vely = 0

    def draw(self):
        pg.draw.circle(win, self.color, tableToAbsolute(table_size, y_buffer, self.posx, self.posy), ball_size)
    
    def hit(self, m_pos):
        b_x, b_y = tableToAbsolute(table_size, y_buffer, self.posx, self.posy)
        self.velx = (b_x - m_pos[0]) / 500
        self.vely = (b_y - m_pos[1]) / 500
    
    def follow(self, m_pos):
        b_x, b_y = tableToAbsolute(table_size, y_buffer, self.posx, self.posy)
        #self.velx = (b_x - m_pos[0]) / 500
        #self.vely = (b_y - m_pos[1]) / 500
        self.velx = -(b_x - m_pos[0]) / 10
        self.vely = -(b_y - m_pos[1]) / 10
        self.posx, self.posy = absoluteToTable(table_size, y_buffer, m_pos[0], m_pos[1])

    def bump(self, ball):
        elasticity = 0 #perfectly elastic, more negative = more inelastic
        delta_x = ball.posx - self.posx
        delta_y = ball.posy - self.posy
        dir = delta_y / delta_x
        a = 2+2*dir*dir
        b = -2*(dir*(self.vely+ball.vely) + self.velx+ball.velx + ball.velx*(2*dir*dir + 1) - dir*ball.vely)
        c = (elasticity)*(self.velx*self.velx + self.vely*self.vely + ball.velx*ball.velx + ball.vely*ball.vely) + 2*ball.velx*(self.velx + dir*(self.vely-ball.vely+dir*ball.velx))
        v1, v2 = np.roots([a,b,c])
        if np.iscomplex(v1) or np.iscomplex(v2):
            return
        vi = ball.velx
        if np.sign(v1) == np.sign(delta_x):
            ball.velx = v1
        elif np.sign(v2) == np.sign(delta_x):
            ball.velx = v2
        else:
            ball.velx = 0
        
        ball.vely = dir * (ball.velx - vi) + ball.vely
        self.velx = self.velx + vi - ball.velx
        self.vely = self.vely + dir*(vi - ball.velx)

def tableToAbsolute(size, y_buffer, x, y):
    x = 100+x*size[0]/200
    y = y_buffer+y*size[1]/100
    return int(x),int(y)

def absoluteToTable(size, y_buffer, x, y):
    x = 200*(x-100)/size[0]
    y = 100*(y-y_buffer)/size[1]
    return x,y

def redraw():
    win.fill(bg_color)
    pg.draw.rect(win, (150,100,0), (100-3*ball_size, y_buffer-3*ball_size, table_size[0]+6*ball_size, table_size[1]+6*ball_size))
    pg.draw.rect(win, (0,150,0), (100, y_buffer, table_size[0], table_size[1]))
    for x in range(3):
        pg.draw.circle(win, (0,0,0), tableToAbsolute(table_size, y_buffer, 100*x, 0), 2*ball_size)
        pg.draw.circle(win, (0,0,0), tableToAbsolute(table_size, y_buffer, 100*x, 100), 2*ball_size)
    for ball in balls:
        ball.draw()
    #invisiball.draw()

def collision_detect(ball1, ball2):
    dist = (ball1.posx - ball2.posx)**2 + (ball1.posy - ball2.posy)**2
    return dist < ball_size

cue_ball = Ball((50,50), (255,255,255))
cue_ball.velx, cue_ball.vely = 2, 2

invisiball = Ball((50,50), (0,0,0))

balls = [cue_ball, Ball((75,25), (255,0,0)), Ball((25,75), (0,255,0)), Ball((25,25), (0,0,255))]

mode = "STRIKE"
switched = False

while run:
    pg.time.delay(10)
    for ball in balls:
        ball.move()
        if mode is "CURSOR" and collision_detect(ball, invisiball):
            invisiball.bump(ball)
    for i in range(len(balls) - 1):
        for j in range(i+1, len(balls)):
            if collision_detect(balls[i], balls[j]):
                balls[i].bump(balls[j])
    redraw()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run=False
        elif i.type == pg.VIDEORESIZE:
            win_size = i.size
            table_size = (win_size[0]-200, win_size[0]/2-100)
            ball_size = int(9*win_size[0]/704-225/88)
            y_buffer = win_size[1]/2-win_size[0]/4+50
            win=pg.display.set_mode(win_size, RESIZABLE)
            
            
    k = pg.key.get_pressed()
            
    if k[pg.K_ESCAPE]:
        run=False

    space = k[pg.K_SPACE]
    switched = switched and space
    
    if mode is "STRIKE":
        if pg.mouse.get_pressed()[0]:
            cue_ball.hit(pg.mouse.get_pos())
        if space and not switched:
            mode = "CURSOR"
            switched = True
    
    elif mode is "CURSOR":
        invisiball.follow(pg.mouse.get_pos())
        if space and not switched:
            mode = "STRIKE"
            switched = True
    

    pg.display.update()

pg.quit()
