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
            for i in all_sphere:
                i.update()
            self.clock.tick(self.FPS)

    def control(self):
        for e in event.get():
            if e.type == KEYDOWN:
                keys = key.get_pressed()
                if keys[K_ESCAPE]:
                    exit()
                if keys[K_SPACE]:
                    self.run = not(self.run)
                if keys[K_g]:
                    earth.gravity(all_sphere)
                if keys[K_t]:
                    test()

class Sphere(sprite.Sprite):
    def __init__(self,x,y,r,mass):
        super().__init__()
        self.mass = mass
        self.r = r
        self.x = x
        self.y = y
        self.rect = Rect(x,y,r,r)
        self.color = (255,0,0)
        self.center = (int(self.x+r/2),int(self.y+r/2))
        all_sphere.append(self)

    def reset(self):
        self.center = (int(self.x+self.r/2),int(self.y+self.r/2))
        draw.circle(win,self.color,self.center,self.r)
    
    def update(self):
        self.gravity(all_sphere)
        self.norm_cor()
        self.reset()

    def randc(self):
        self.color = (randint(0,255),randint(0,255),randint(0,255))

    def norm_cor(self):
        self.rect.x = self.x
        self.rect.y = self.y
    
    def gravity(self,all_sphere):
        global G
        self.randc()
        for i in all_sphere:
            if self.distance(i) > self.r*2:
                F = ((self.mass * i.mass) / (self.distance(i)) ** 2)
                res = 1
                print(F)
                self.x += res * self.arcx(i)
                self.y += res * self.arcy(i)
                self.norm_cor()
                #display.update()
            else:
                res = -1
                self.x += res * self.arcx(i)
                self.y += res * self.arcy(i)
                print(self.x,i.x)
                self.norm_cor()

    def arcx(self,aim):
        if self.distance(aim) > 0:
            if self.x > aim.x:
                return -abs(abs(self.x) - abs(aim.x))/self.distance(aim)
            else:
                return abs(abs(aim.x) - abs(self.x))/self.distance(aim)
        else:
            return 0
    
    def arcy(self,aim):
        if self.distance(aim) > 0:
            if self.y > aim.y:
                return -abs(abs(self.y) - abs(aim.y))/self.distance(aim)
            else:
                return abs(abs(aim.y) - abs(self.y))/self.distance(aim)
        else:
            return 0

    def distance(self,aim):
        dx = abs(self.x) - abs(aim.x)
        dy = abs(self.y) - abs(aim.y)
        return mh.sqrt(  dx**2+dy**2  )

class Test(Sphere):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d]:
            self.x += 1
        if keys[K_a]:
            self.x -= 1
        if keys[K_s]:
            self.y += 1
        if keys[K_w]:
            self.y -= 1
        self.color = (randint(0,255),randint(0,255),randint(0,255))
        self.norm_cor()
        self.reset()

def test():
    t = draw.circle(win,(255,0,0),(0,0),5)
    print(t)

if __name__ == "__main__":
    W = 1920
    H = 1080

    win = display.set_mode([W,H],flags=FULLSCREEN)

    all_sphere = []
    earth = Test(100,100,r=20 ,mass=6*10**24)

    moon = Sphere(400,100,r=30 ,mass=7.3*10**22)

    one = Sim(win,W,H)
    #one.when_start()
    while True:
        one.game()