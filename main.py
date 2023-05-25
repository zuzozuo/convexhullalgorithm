import numpy as np 
import random
import math
from PIL import Image, ImageDraw

POINTS_NUMBER = 10 # how many points
MAX_H_P = 250 # height of png file
MAX_W_P = 250 # height of png file
Y_OFFSET  = 10 # multiplying x coords for png file
X_OFFSET = 10  # multiplying y coords for png file
WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)

class Point:
    
    global BLACK
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.angle = 0 #  polar angle with P0
        self.color = BLACK
        
    def set_color(self, c: tuple):
        self.color = c
        

# n - how many points to generate
class Generator:
    def __init__ (self, n: int):
        self.points =  self.generate_fixed_points() # np.array(self.generate_points(n), dtype=object)
        
    def generate_points(self, n: int):
        p = set()
        while (len(p) < n):
            p.add(Point(random.randint(0,20), random.randint(0,20)))
            
        return list(p)
    
    def generate_fixed_points(self):
        p_coords = [
            (18, 2),
            (10, 16),
            (2, 12),
            (20, 7),
            (10, 7),
            (15, 6),
            (15, 14),
            (14, 9),
            (1, 14),
            (8, 14),
            (1, 2),
            (20, 18)
        ]
        
        return np.array([Point(x[0], x[1]) for x in p_coords], dtype=object)
        
    
    def get_points(self): return self.points
    
    def print_points(self):        
        for p in self.points:
            print(str(p.x) + " " + str(p.y))
            

class ComplexHull:
    def __init__(self, p: np.array):
        self.p = p # list of points
        
    
    def graham(self):
        # print("Before: ")
        # self.print_points()
        # find the lowest y-coord and leftmost point, P0 
        i_min = 0 # minimum index, will be needed for swapping
        y_min = self.p[0].y # starting y coord of first point in array
        x_min = self.p[0].x # starting x coord of first point in array

        for x in range(1, self.p.size):

            if (self.p[x].y < y_min) or ((y_min == self.p[x].y) and (self.p[x].x < x_min)): 
                y_min = self.p[x].y
                x_min = self.p[x].x
                i_min = x
                
        p0 = self.p[i_min]
        self.p = np.concatenate((np.array([p0]), self.p[:i_min], self.p[i_min + 1:])) # move p0 at the beggining of an array
        

        # print("After: ")
        # self.print_points()
    
    def print_points(self):
        for p in self.p:
            print(str(p.x) + " " + str(p.y))
        
        
        
            
        
class Draw:
    global MAX_H_P, MAX_W_P, BLACK, WHITE, RED
    
    def __init__(self, points: np.array):
        self.points = points
        self.dot_size = 2
        self.image  = Image.new("RGB", (MAX_H_P, MAX_W_P), WHITE)
        
    def draw_image(self):
        draw = ImageDraw.Draw(self.image)
        
        for p in self.points:
            draw.point((p.x * X_OFFSET, p.y * Y_OFFSET), p.color)
        self.image.save("points.png")
        
        
        
if __name__ == "__main__":
    g = Generator(POINTS_NUMBER)
    g.print_points()
    
    h = ComplexHull(g.get_points())
    h.graham()
    
    
    d = Draw(g.get_points())
    d.draw_image()
    

