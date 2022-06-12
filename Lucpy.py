import numpy as np
from dataclasses import dataclass
from scipy.spatial.distance import pdist,squareform
import statistics as stats
import pygame
import time
import matplotlib.pyplot as plt

@dataclass
class Firefly:
    '''
    Firefly object

    coordinates: tuple -> position of the firefly
    on: bool -> True if firefly is on false if off
    fase: int -> step of the cycle the firefly is in
    '''
    coordinates: list
    on: bool = False
    cycle: int = 50

    def __post_init__(self):
        self.fase = np.random.randint(self.cycle)
        self.neighbours = []
        self.change_state()
    
    def change_state(self):
        if self.fase < 25:
            self.on = True
        else:
            self.on = False
    
    def check_neighbours(self, list_fireflies):
        '''
        Check if half or more neighbours are on
        list_fireflies: list -> list that contains firefly objects
        '''
        neighbours_state = [list_fireflies[i].on for i in self.neighbours]
        if neighbours_state:
            return(stats.mean(neighbours_state) >= 0.5)
        else:
            return(False)
    
    def skip_step(self, list_fireflies):
        if self.check_neighbours(list_fireflies):
            self.fase += 1
    
    def draw(self,screen):
        off_color = '#6a8f9c'
        on_color = '#fdd310'

        if self.on:
            circle = pygame.draw.circle(screen,on_color,tuple(coord*700 for coord in self.coordinates),3)
        else:
            circle = pygame.draw.circle(screen,off_color,tuple(coord*700 for coord in self.coordinates),3)
        



@dataclass
class Hive:
    '''
    Group of fireflies

    num_fireflies: ind -> Number of fireflies in the system
    radius: float -> Distance whithin wich two fireflies are considered neighbours
    fire_coordinates: A random np.array of dimensions n by 2 where n is num_fireflies
    '''

    num_fireflies: int = 150
    radius: float = 0.45
    timesteps: int = 5000
    
    def __post_init__(self):
        self.fire_coordinates = np.random.rand(self.num_fireflies,2)
        self.fireflies = [Firefly([row[0],row[1]])for row in self.fire_coordinates]
        self.get_neighbours()
        

    def get_neighbours(self):
        distance_matrix = squareform(pdist(self.fire_coordinates))
        boolean_matrix = distance_matrix < self.radius
        for i in range(len(boolean_matrix)):
            boolean_matrix[i,i] = False
        for row,firefly in zip(boolean_matrix,self.fireflies):
            neighbours = [i for i,val in enumerate(row) if val]
            firefly.neighbours = neighbours
    
    def pass_time(self):
        for firefly in self.fireflies:
            firefly.fase = (firefly.fase + 1)%50
            if firefly.fase == 0:
                firefly.skip_step(self.fireflies)
        
        for firefly in self.fireflies:
            firefly.change_state()
    
    def draw(self):
        done = False
        results = []
        pygame.init()
        screen = pygame.display.set_mode((700,700)) #creas una ventana
        pygame.display.set_caption('Firefly Simulation')
        screen.fill((51,24,50)) # color del fondo
        n = 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
            self.pass_time()
            for firefly in self.fireflies:
                firefly.draw(screen) # dibujas cada luciernaga
            n += 1

            if n >= self.timesteps:
                done = True

            on_number = sum([firefly.on for firefly in self.fireflies])
            results.append(on_number)
            time.sleep(0.007)
            pygame.display.update()
        plt.plot(list(range(len(results))),results)
        plt.show()

    
    def analytical_loop(self, mode):
        results = []
        for n in range(self.timesteps):
            on_number = sum([firefly.on for firefly in self.fireflies])

            if mode == 'all':
                results.append(on_number)
            elif mode == 'last_50':
                if n >= self.timesteps - 51:
                    results.append(on_number)
            self.pass_time()
        
        return((results,list(range(len(results)))))
    
    def plot_analysis(self):
        y,x = self.analytical_loop(mode = 'all')
        plt.plot(x,y)
        ax = plt.gca()
        ax.set_ylim(0,150)
        ax.set_xlim(0,5000)
        plt.show()
        


    

def main():

    a = Hive()
    a.draw()
    

if __name__ == '__main__':
    main()