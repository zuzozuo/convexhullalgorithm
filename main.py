import numpy as np 
import random
import math
from PIL import Image, ImageDraw, ImageFont

POINTS_NUMBER = 10 # how many points
MAX_H_P = 1000 # height of png file
MAX_W_P = 1000 # height of png file
Y_OFFSET  = 20 # multiplying x coords for png file
X_OFFSET = 20  # multiplying y coords for png file
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
        self.points = np.array(self.generate_points(n), dtype=object)  #self.generate_fixed_points() # 
        
    def generate_points(self, n: int):
        p = set()
        while (len(p) < n):
            p.add(Point(random.randint(3,23), random.randint(3,23)))
            
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
        
        #p_coords = [(6, 20), (9, 16), (12, 4), (17, 1), (23, 7), (25, 9), (21, 18), (15, 23), (3, 24), (2, 10)]
        
        return np.array([Point(x[0], x[1]) for x in p_coords], dtype=object)
        
    
    def get_points(self): return self.points
    
    def print_points(self):        
        for p in self.points:
            print(str(p.x) + " " + str(p.y))
            

class ComplexHull:
    def __init__(self, p: np.array):
        self.p = p # list of points
        self.h = np.array([], dtype=object) # list with solution        
    
    def distance(self, p1: Point, p2: Point):
        return np.linalg.norm( np.array([p2.x, p2.y]) - np.array([p1.x, p1.y]) )
    
    def angle(self, p1: Point, p2: Point):
        return np.arctan2((p2.x - p1.x), (p2.y - p1.y))
    
    def check_orientation(self, p1: Point, p2: Point, p3: Point) -> int:
        
        o = (p3.y - p2.y) * (p2.x - p1.x) - (p2.y - p1.y) * (p3.x - p2.x)
        
        if ( o > 0): 
            return -1 # clockwise
        elif (o < 0): 
            return 1 # counterclockwise
        else: 
            return 0 #colilinear
        
    
    def graham(self):
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
        print("p0: " + str(p0.x) + " " + str(p0.y) )
        self.p = np.concatenate((np.array([p0]), self.p[:i_min], self.p[i_min + 1:])) # move p0 at the beggining of an array
        
        # sort depending on angle and distance 
        self.p = np.array(sorted(self.p, key=lambda p: (self.angle(p0,p), self.distance(p0, p))), dtype=object)
        # scan begin
        for x in range(0, self.p.size):
            # check oritentatnion 
            print(f"Current point check {self.p[x].x} {self.p[x].y}")
            
            while (self.h.size >= 2) and (self.check_orientation(self.h[-2], self.h[-1], self.p[x]) != 1):
                if((self.h[-1].x) == p0.x and (self.h[-1].y == p0.y)): #break if you come back to the first point
                    break
                
                print(f"Checked triplet p1: {self.h[-2].x} {self.h[-2].y} p2: {self.h[-1].x} {self.h[-1].y} p3: {self.p[x].x} {self.p[x].y} ")
                print(f"Throwing out: {self.h[-1].x} {self.h[-1].y}")
                print(f"Distance p1-p2: {self.distance(self.h[-2], self.h[-1])}  Distance p1-p3: {self.distance(self.h[-2], self.p[x])}")
                self.h = self.h[:-1]
            
            self.h = np.append(self.h, self.p[x])
            
        print("======")
        
        while (self.h.size >= 2) and (self.check_orientation(self.h[-2], self.h[-1], self.h[0]) != 1):            
            print(f"Checked triplet p1: {self.h[-2].x} {self.h[-2].y} p2: {self.h[-1].x} {self.h[-1].y} p3: {self.h[0].x} {self.h[0].y} ")
            print(f"Throwing out: {self.h[-1].x} {self.h[-1].y}")
            print(f"Distance p1-p2: {self.distance(self.h[-2], self.h[-1])}  Distance p1-p3: {self.distance(self.h[-2], self.h[0])}")
            self.h = self.h[:-1]
            
        
        for h in self.h:
            h.color = RED
        self.print_hull()
        
        return self.h
        
    
    def print_points(self):
        for p in self.p:
            print(str(p.x) + " " + str(p.y))
    
    def print_hull(self):
        for h in self.h:
            print(str(h.x) + " " + str(h.y) +  " " + str(h.color))
                    
        
class Draw:
    global MAX_H_P, MAX_W_P, BLACK, WHITE, RED
    
    def __init__(self, points: np.array):
        self.points = points
        self.dot_size = 2
        self.image  = Image.new("RGB", (MAX_H_P, MAX_W_P), WHITE)
        
    def draw_image(self):
        draw = ImageDraw.Draw(self.image)
        
        for p in self.points:
            #draw.point((p.x * X_OFFSET, MAX_H_P - (p.y * Y_OFFSET)), p.color)
            y1 = MAX_H_P - (p.y  * Y_OFFSET )
            draw.ellipse((p.x * X_OFFSET - 1, y1 -1, p.x * X_OFFSET + 1, y1 + 1), outline= p.color)
            draw.text((p.x * X_OFFSET, MAX_H_P- ((p.y * Y_OFFSET) - 5)), f"( {p.x},  {p.y} )", fill=(0, 0, 0), size=10)
        self.image.save("points.png")
        
        
        
if __name__ == "__main__":
    g = Generator(POINTS_NUMBER)
    
    h = ComplexHull(g.get_points())
    h.graham()
    
    
    d = Draw(g.get_points())
    d.draw_image()
    

