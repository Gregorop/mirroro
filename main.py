from random import randint
from pygame import*
import math as mh

class Sim():
    def __init__(self,win,W,H):
        super().__init__()
        self.win = win
        self.W = W
        self.H = H
        self.run = False
        self.clock = time.Clock()
        self.FPS = 60

    def when_start(self):
        print("я запустилась")
        self.run = True
    
    def game(self):
        self.control()
        if self.run:
            display.update()
            win.fill((0,0,0))
            for beam in Beam.all_beams:
                beam.make_step()
                beam.draw(self.win)

            for particle in Particle.all_particles:
                particle.draw(self.win)

            self.clock.tick(self.FPS)

    def control(self):
        for e in event.get():
            if e.type == KEYDOWN:
                keys = key.get_pressed()
                if keys[K_ESCAPE]:
                    exit()
            
            #if e.type == KEYUP:
            #    keys = key.get_pressed()
            #    if keys[K_SPACE]:
            #        Beam.all_beams[0].angle += 1 

class Beam:
    all_beams = []
    def __init__(self,start_cor,angle,color=(255,0,0)):
        self.start = start_cor
        self.x = start_cor[0]
        self.y = start_cor[1]
        self.angle = angle/360*mh.pi*2
        self.color = color
        self.active = 1
        Beam.all_beams.append(self)
    
    def make_step(self):
        if not self.active: return 0
        self.x += mh.cos(self.angle)
        self.y += mh.sin(self.angle) 
        for particle in Particle.all_particles:
            if particle.check_collide(self.x,self.y):
                self.active = 0
                if self.x < particle.x:
                    Beam((self.x,self.y),self.angle+180,self.color)
                else:
                    Beam((self.x,self.y),self.angle,self.color)

                
        #если напоролись на частицу, берем угол от точки где столкнулись
        #создаем новый луч
        #этот отрубаем

    def draw(self,screen):
        draw.line(screen,self.color,self.start,(self.x,self.y))

class Particle:
    all_particles = []
    def __init__(self,start_cor,radius):
        self.start = start_cor
        self.radius = radius
        self.squareR = radius**2

        self.y = self.start[1]
        self.x = self.start[0]
        self.leftX = self.start[0] - self.radius
        self.rightX = self.start[0] + self.radius

        self.color = (0,255,0)
        Particle.all_particles.append(self)
    
    def draw(self,screen):
        draw.circle(screen,self.color,self.start,self.radius)

    def check_collide(self,x,y):
        if self.leftX < x < self.rightX:
            if ((x-self.x)**2 + (y-self.y)**2) < self.squareR:
                return 1
        else:
            return 0
    
    def getXY(self):
        return self.x,self.y

if __name__ == "__main__":
    W = 1920
    H = 1080

    win = display.set_mode([W,H],flags=FULLSCREEN)
    one = Sim(win,W,H)
    Beam((190,0),90)
    Beam((290,0),90)
    Beam((190,1000),-90,color=(255,0,255))
    Beam((290,1000),-90,color=(0,255,255))
    Beam((250,1000),-90,color=(0,0,255))
    Particle((250,600),70)
    Particle((400,550),20)
    Particle((400,650),30)
    one.when_start()
    while True:
        one.game()