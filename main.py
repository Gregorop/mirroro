from dis import dis, show_code
from importlib.metadata import distribution
from random import randint
from tracemalloc import start
from pygame import*
import math as mh
from random import randint, shuffle

class Line():
    def __init__(self,win,color,start,aim):
        self.win = win
        self.color = color
        self.start = start
        self.aim = aim
    
    def redraw(self):
        draw.line(self.win,self.color,self.start,self.aim)

class Sim():
    line_obj = []
    detectors = []
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
        self.laser = False
    
    def game(self):
        self.control()
       
        if self.run:
            display.update()
            
            win.fill((0,0,0))
            
            for particle in Particle.all_particles:
                particle.draw(self.win)

            for l in Sim.line_obj:
                l.redraw()

            self.shooting()

            for detector in Sim.detectors:
                detector.draw(self.win)
                
            self.clock.tick(self.FPS)

    def control(self):
        global me
        
        for e in event.get():
            if e.type == KEYDOWN:
                
                if e.key == K_ESCAPE:
                    exit()
                if e.key == K_SPACE:
                    display.update()
                if e.key == K_1:
                    
                    generate_normalno(1,layer_thick,W,layer_roof)
                if e.key == K_2:
                    self.start_shoot()

    def addDetector(det):
        Sim.detectors.append(det)

    def start_shoot(self):
        self.laser = True
        sherloc.power = 0
        Beam.all_beams.clear()
        for i in range(0,n_beam):
            Beam((i,generation_y), 90, all_power/n_beam)

    def shooting(self):
        if not self.laser: return 0
        
        actives = 0
        for beam in Beam.all_beams:
            beam.make_step()
            if beam.active: 
                beam.draw(win)
                actives += 1

        if actives <1:
            print("result",round(Sim.detectors[0].power,3))
            Beam.all_beams.clear()

class Beam:
    all_beams = []
    def __init__(self,start_cor,angle,power,color=(255,0,0)):
        global win,one, W
        self.power = power

        self.start = start_cor
        self.x = start_cor[0]
        self.y = start_cor[1]
        self.angle = angle/360*mh.pi*2
        #for particle in Particle.all_particles:
            #if particle.check_collide(self.x,self.y):
                #Sim.line_obj.append(Line(win,(0,0,0),particle.start,(self.x,self.y)))
        self.red = color[0]
        self.color = color
        self.active = 1
        Beam.all_beams.append(self)
    
    def make_step(self):
        global mirror_kef,generation_y,step_divader, layer_roof
        if not self.active: return 0
        too_hight = (self.y < layer_roof and self.red != 255)
        few_power = self.power < 0.00001
        left_right = self.x < 0 or self.x > W
        if few_power or too_hight or left_right: 
            self.active = 0
            return 0
        self.x += mh.cos(self.angle)/step_divader
        self.y += mh.sin(self.angle)/step_divader

        for particle in Particle.all_particles:
            #если напоролись на частицу, берем угол от точки где столкнулись
            #создаем новый луч
            #этот отрубаем
            if particle.check_collide(self.x,self.y):
                self.active = 0
                new_angle = self.calc_angle(particle)
                new_power = self.power * mirror_kef
                self.red = self.red * 0.9
                #Beam((self.x,self.y),new_angle,(0,255,255))
                Beam((self.x,self.y),new_angle,new_power,(self.red,0,0))
        
        for detector in Sim.detectors:
            if self.y > detector.y and self.active:
                self.active = 0
                detector.power += self.power
                
    def calc_angle(self,aim):
        left_down = self.x <= aim.x and self.y >= aim.y
        right_up = self.x >= aim.x and self.y <= aim.y
        leg = abs(self.y - aim.y)
        
        a = self.angle*180/mh.pi

        if left_down or right_up:
            f = (mh.acos(leg/aim.radius)*180/mh.pi)
            '''
            if f<1:
                if left_down: return 90
                if right_up: return -90
            '''
            n = 180 - a
            ch = a - f - 90
            return -n - 2*ch
        else:
            f = (mh.asin(leg/aim.radius)*180/mh.pi)
            ch = a - f
            return 180 - a + 2*f
    
    def calc_angle_old(self,aim):
        leg = abs(self.x - aim.x)
        result = -self.angle
        if self.x>aim.x and abs(self.y-aim.y)>1:
            alpha = (mh.asin(leg/aim.radius)*180/mh.pi)
            if self.y<aim.y:
                result = alpha*2 - 90
            else:
                result = 90 - alpha*2
        elif self.x<aim.x and abs(self.y-aim.y)>1:
            alpha = (mh.asin(leg/aim.radius)*180/mh.pi)
            if self.y>aim.y:
                result = 90 + alpha*2
            else: 
                result = - alpha*2 - self.angle
                
        if result == 0 or result%360==0: return 180
        return result

    def draw(self,screen):
        draw.line(screen,self.color,self.start,(self.x,self.y))

class Particle:
    all_particles = []
    def __init__(self,start_cor,radius):
        self.start = start_cor
        self.radius = radius
        self.squareR = radius**2
        self.ploshad = 2*(3.14*self.radius)**2

        self.y = self.start[1]
        self.x = self.start[0]
        self.leftX = self.start[0] - self.radius
        self.rightX = self.start[0] + self.radius
        self.topY = self.start[1] - self.radius
        self.bottomY = self.start[1] + self.radius

        self.color = (0,255,0)
        Particle.all_particles.append(self)
    
    def draw(self,screen):
        draw.circle(screen,self.color,(self.x,self.y),self.radius)

    def check_collide(self,x,y):
        if self.leftX < x < self.rightX:
            if ((x-self.x)**2 + (y-self.y)**2) <= self.squareR:
                return 1
        else:
            return 0
    
    def two_sphere_collide(self,another):
        diff_x = abs(self.x-another.x)
        diff_y = abs(self.y-another.y)
        hupotenus = (diff_x**2 + diff_y**2)**0.5
        if hupotenus > self.radius + another.radius:
            return False
        return True

    def check_collides_one_partcle_to_all_others(self):
        for particle in Particle.all_particles:
            if self.two_sphere_collide(particle) and particle != self:
                return True
        return False

    def move_all_particles_outer_one(self):
        for particle in Particle.all_particles:
            if self.x > particle.x: move_x = -1
            if self.x < particle.x: move_x = 1
            if self.x == particle.x: move_x = 0
            if self.y > particle.y: move_y = -1
            if self.y < particle.y: move_y = 1
            if self.y == particle.y: move_y = 0
            particle.x += move_x
            particle.y += move_y
            self.reset_coords()
            
    def reset_coords(self):
        self.leftX = self.x - self.radius
        self.rightX = self.x + self.radius
        self.topY = self.y - self.radius
        self.bottomY = self.y + self.radius

    def check_out(self,left_x,right_x,top_y,down_y):
        hor = self.leftX < left_x or self.rightX > right_x
        ver = self.topY < top_y or self.bottomY
        if hor or ver: self.del_particle()

    def getXY(self):
        return self.x,self.y

    def del_particle(self):
        Particle.all_particles.remove(self)

class Detector:
    def __init__(self,x_left,y,width):
        self.x_left = x_left
        self.y = y
        self.width = width
        self.color = (0,0,255)
        self.power = 0
        font.init()
        self.font = font.SysFont("Impact", 100)
        Sim.addDetector(self)

    def draw(self,screen):
        global win, W
        draw.line(screen,self.color,(self.x_left,self.y),(self.x_left+self.width,self.y))
        self.text_pic = self.font.render(str(round(self.power,7)), False, (0,0,255))
        win.blit(self.text_pic,(W/2,self.y+50))


def tests():

    for i in range(W):
        Beam((i,0),90)
    
    
    for i in range(360):
        Beam((0,0), i)
    
    for i in range(360):
        Beam((1000,0), i)

    for i in range(360):
        Beam((0,1000), i)

    for i in range(0,360,21):
        Beam((287+i,0), 90)

    Particle((500,500), 200)

def random_generate():
    global min_r,max_r,layer_roof,layer_bottom
    n_particles = 350 #количество частиц
    for i in range(n_particles):
        r = randint(min_r, max_r)
        minY = layer_roof + r
        maxY = layer_bottom - r
        Particle((randint(r,W-r),randint(minY, maxY)), r)

def random_generate_in_layer():
    global min_r,max_r,layer_roof,layer_bottom,powder_width
    n_inner_Layers = layer_thick//(max_r*2)
    
    x = 0
    thislayer_y = layer_roof+max_r
    for i in range(n_inner_Layers):
        while x<powder_width:
            r = randint(min_r, max_r)
            Particle((x,thislayer_y), r)
            x += max_r*2
        x = randint(-max_r, max_r) + max_r/2
        thislayer_y += max_r*2

    Sim.line_obj.append(Line(win,(0,255,0),(0,layer_roof),(W,layer_roof)))
    Sim.line_obj.append(Line(win,(0,255,0),(0,layer_bottom),(W,layer_bottom)))

def remove_useless_rad(distrib,max_r):
    for rad in distrib:
        if rad > max_r:
            distrib.remove(rad)
    return distrib

def vanila_disterb():
    distrib = []
    distrib += [10] * 26
    distrib += [15] * 53
    distrib += [20] * 63
    distrib += [25] * 132
    distrib += [30] * 189
    distrib += [35] * 95
    distrib += [40] * 63
    distrib += [45] * 17
    distrib += [50] * 6 
    shuffle(distrib)
    return distrib

def generate_normalno(need_density,layer_thick,powder_width,layer_roof):
    Particle.all_particles.clear()
    distrib = vanila_disterb()
    max_r = layer_thick/2
    distrib = remove_useless_rad(distrib,max_r)

    min_x = 0
    min_y = layer_roof
    max_y = layer_roof + layer_thick

    full_square = layer_thick*powder_width
    fill_square = full_square
    particle_square = 0
    density_now = particle_square/full_square
    
    while density_now < need_density:
        if density_now < need_density:
            x = randint(min_x,powder_width)
            y = randint(min_y,max_y)
            rad = distrib[randint(0,len(distrib)-1)]
            now_particle = Particle((x,y),rad)
            while now_particle.check_collides_one_partcle_to_all_others():
                
                for particle in Particle.all_particles:
                    particle.check_out(0,W,min_y,max_y)
                
                now_particle.move_all_particles_outer_one()
                

        if density_now > need_density:
            to_del_max_r = 0
            to_del_particle = Particle.all_particles[0]
            for particle in Particle.all_particles:
                if particle.radius > to_del_max_r:
                    to_del_max_r = particle.radius
                    to_del_particle = particle
            to_del_particle.del_particle()
        
        particle_square = 0
        for particle in Particle.all_particles:
            particle_square += particle.ploshad
            
        
        density_now = particle_square/full_square
        
    Sim.line_obj.append(Line(win,(0,255,0),(0,layer_roof),(W,layer_roof)))
    Sim.line_obj.append(Line(win,(0,255,0),(0,layer_bottom),(W,layer_bottom)))

def generate_from_pic(filename):
    global layer_thick,layer_roof
    import scrap.picdetect as picdetect

    particles = picdetect.detect(filename)
    for particle in particles:
        x = particle[0][0] + 300
        y = particle[0][1] + layer_roof
        r = particle[1]
        Particle((x,y),r)

if __name__ == "__main__":
    
    W = 1920
    H = 1080
    start_laser = False

    layer_roof = 30 #верх слоя (координата Y кверхногами, тоесть 300px от верха окна)
    generation_y = layer_roof - 20
    layer_thick = 250 #толщина слоя
    layer_bottom = layer_roof + layer_thick
    
    #min_r = 10 #мин и макс радиусы
    #max_r = 25
    #пока без распределения просто рандом от и до

    mirror_kef = 0.4 #кеф отражения
    n_beam = W #количество лучей
    powder_width = W
    all_power = 1.6 #мощь всех лучей
    step_divader = 1 #точность рассчета шага (больше - точнее - медленее)

    win = display.set_mode([W,H],flags=FULLSCREEN)
    one = Sim(win,W,H)

    sherloc = Detector(0, layer_bottom, powder_width)
    
    #random_generate_in_layer()
    
    one.when_start()
    while True:
        one.game()