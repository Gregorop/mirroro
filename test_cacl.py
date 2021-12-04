import matplotlib.pyplot as plt
from random import randint

class Particle():
    def __init__(self,T,R):
        self.T = T
        self.R = R
        self.square = 4*3.14*R**2

    
dist = 10*10**-9

particles = []
for i in range(10):
    particles.append([])

for row in particles:
    for p in range(10):
        row.append(Particle(0,randint(10,50)*10**-9))


particles[0][0].T = 600

def changeT():
    for row in range(len(particles)):
        if row != 0 or row != len(particles):
            for p in range(len(particles[row])):
                if p != 0 or p != len(particles[row]):
                    for i in range(-1,1,1):
                        for j in range(-1,1,1):
                            #tmp_T = 
                            particles[row+i][p+j]