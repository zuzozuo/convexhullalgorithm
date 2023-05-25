import numpy as np 
import random
from PIL import Image, ImageDraw

POINTS_NUMBER = 10 # how many points
MAX_H_P = 400 # height of png file
MAX_W_P = 400 # height of png file
Y_OFFSET  = 10 # multiplying x coords for png file
X_OFFSET = 10  # multiplying y coords for png file
WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)

class Point:
    global BLACK
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color = BLACK
        
    def set_color(self, c: tuple):
        self.color = c
        

# n - how many points to generate
class Generator:
    def __init__ (self, n: int):
        self.points = np.array(self.generate_points(n), dtype=object)
        
    def generate_points(self, n: int):
        p = set()
        while (len(p) < n):
            p.add(Point(random.randint(0,20), random.randint(0,20)))
            
        return list(p)
    
    def get_points(self): return self.points
    
    def print_points(self):        
        for p in self.points:
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
    d = Draw(g.get_points())
    d.draw_image()

