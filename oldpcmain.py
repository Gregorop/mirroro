import pygame as pg
from random import randint
import numpy as np

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)

class Pixel:
    all_pixels = []
    math_pixels = np.zeros((1000, 1000))

    def __init__(self,x,y,typ):
        self.x = x
        self.y = y
        if typ=="particle":
            self.typ = 1
        elif typ=="ray":
            self.typ = 2
        self.rect = pg.Rect(self.x,self.y,1,1)
        if typ == "particle" and not self.check_overlap():
            Pixel.all_pixels.append(self)
            Pixel.math_pixels[x][y] = self.typ
        else:
            Pixel.all_pixels.append(self)
            Pixel.math_pixels[int(x)][int(y)] = self.typ

    def check_overlap(self):
        if Pixel.math_pixels[self.x,self.y] == self.typ:
            return 1
        return 0
        
    def check_collide(x,y):
        if Pixel.math_pixels[int(x)][int(y)] == 1:
            return 1

    def check_laser_overlap(x,y):
        if Pixel.math_pixels[int(x)][int(y)] == 2:
            return 1
        
class Particle:
    def __init__(self,gr,center_x,center_y,radius=10):
        self.color = GREEN
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.pixels = []
        self.init_pixels()
        gr.append(self)

    def init_pixels(self):
        start_x = self.center_x - self.radius
        finish_x = self.center_x + self.radius
        x = start_x
        while x < (self.center_x + self.radius):
            if x < self.center_x:
                for y in range(x-start_x):
                    self.pixels.append(Pixel(x,self.center_y+y,typ="particle"))
                    self.pixels.append(Pixel(x,self.center_y-y,typ="particle"))
            else:
                for y in range(finish_x-x):
                    self.pixels.append(Pixel(x,self.center_y+y,typ="particle"))
                    self.pixels.append(Pixel(x,self.center_y-y,typ="particle"))
            x+=1
    
    def draw(self,screen):
        for pix in self.pixels:
            pg.draw.rect(screen,self.color,pix.rect)    

class Ray:
    def __init__(self,gr,start_x,start_y,dir_x=0,dir_y=1):
        if Pixel.check_collide(start_x,start_y):
            self.split(gr)
            return 0
            
        self.head = Pixel(start_x,start_y,typ="ray")
        self.pixels = [self.head]
        self.direction = [dir_x,dir_y]
        self.color = RED
        self.active = True
        gr.append(self)
        
    
    def make_step(self,gr):
        if not self.active: return 0

        new_x = self.head.x+self.direction[0]
        new_y = self.head.y+self.direction[1]
        if Pixel.check_collide(new_x,new_y):
            self.split(gr)

        self.head = Pixel(new_x,new_y,typ="ray")
        self.pixels.append(self.head)

    def split(self,global_rays):
        self.active = 0
        for new_x in range(-1,2):
            for new_y in range(-1,2):
                Ray(global_rays,self.head.x,self.head.y,new_x,new_y)

    def draw(self,screen):
        for pix in self.pixels:
            pg.draw.rect(screen,self.color,pix.rect)

    
scr = pg.display.set_mode((1000,1000))

global_rays = []
global_particles = []

Ray(global_rays,200,0)
Ray(global_rays,300,0)
Ray(global_rays,400,0)
Ray(global_rays,500,0)
Ray(global_rays,600,0)
Ray(global_rays,700,0)

for i in range(5):
    for y in range(5):
        Particle(global_particles,randint(100,900),450+randint(0,100),radius=randint(5,25))

#print(Pixel.math_pixels)
while True:

    for event in pg.event.get():
        if event.type == 12:
            exit()
    
    scr.fill(BLACK)
    for particle in global_particles:
        particle.draw(scr)

    for ray in global_rays:
        ray.make_step(global_rays)
        ray.draw(scr)

    pg.display.update()