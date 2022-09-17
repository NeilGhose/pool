import pygame as pg
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
    def __init__(self, pos):
        self.velx = 0
        self.vely = 0
        self.posx = pos[0]
        self.posy = pos[1]

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
        pg.draw.circle(win, (255,255,255), tableToAbsolute(table_size, y_buffer, self.posx, self.posy), ball_size)
    
    def hit(self, m_pos):
        b_x, b_y = tableToAbsolute(table_size, y_buffer, self.posx, self.posy)
        self.velx = (b_x - m_pos[0]) / 500
        self.vely = (b_y - m_pos[1]) / 500
                
def tableToAbsolute(size, y_buffer, x, y):
    x = 100+x*size[0]/200
    y = y_buffer+y*size[1]/100
    return int(x),int(y)

def redraw():
    win.fill(bg_color)
    pg.draw.rect(win, (150,100,0), (100-3*ball_size, y_buffer-3*ball_size, table_size[0]+6*ball_size, table_size[1]+6*ball_size))
    pg.draw.rect(win, (0,150,0), (100, y_buffer, table_size[0], table_size[1]))
    for x in range(3):
        pg.draw.circle(win, (0,0,0), tableToAbsolute(table_size, y_buffer, 100*x, 0), 2*ball_size)
        pg.draw.circle(win, (0,0,0), tableToAbsolute(table_size, y_buffer, 100*x, 100), 2*ball_size)
    ball.draw()            
            

ball = Ball((50,50))
ball.velx, ball.vely = 2, 2
while run:
    pg.time.delay(10)
    ball.move()
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
    
    if pg.mouse.get_pressed()[0]:
        ball.hit(pg.mouse.get_pos())

    pg.display.update()

pg.quit()
