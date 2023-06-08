"""
This code demonstrates the generation of random points, computation of the convex hull using the Graham's scan algorithm,
and drawing the resulting points and convex hull on an image.
"""

from consts import *
import numpy as np 
import random
import os
from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------------
class Point:
    
    """
    Represents a point in 2D space.
    
    Args:
            x (int): The x-coordinate of the point.
            y (int): The y-coordinate of the point.
            
    """

    def __init__(self, x: int, y: int):        
        self.x = x
        self.y = y
        self.color = BLACK
        
    def set_color(self, c: tuple) -> None:
        self.color = c

# --------------------------------------------------------------------------------        

class Generator:
    
    """
    Generates a set of random points.
    
    Args:
            n (int): The number of points to generate.
    """

    def __init__ (self, n: int):
        self.points = np.array(self.generate_points(n), dtype=object)
        
    def generate_points(self, n: int) -> np.array:
        
        """
        Generates a random set of points.

        Args:
            n (int): The number of points to generate.

        Returns:
            np.array: An array of Point objects representing the generated points.
        """
        
        points = np.array([], dtype=object)
        p = set()
        while (len(p) < n):
            p.add((random.randint(3,20), random.randint(3,20)))
            
        for c in p:
            points = np.append(points, Point(c[0], c[1]))
            
        return points

    def set_fixed_points(self, coords: list) -> None:
        
        """
        Sets the points to a fixed set of coordinates.

        Args:
            coords (list): A list of tuples representing the x and y coordinates of the points.
        """
        
        self.points = np.array([Point(x[0], x[1]) for x in coords], dtype=object)
        
    def get_points(self) -> np.array: return self.points
    
    def print_points(self) -> None:        
        for p in self.points:
            print(str(p.x) + " " + str(p.y))
            
# --------------------------------------------------------------------------------
class ComplexHull:
    
    """
    Computes the convex hull of a set of points using Graham's scan algorithm.
    """
    
    def __init__(self, p: np.array):
        self.p = p # list of points
        self.h = self.graham() # list with solution        
    
    def distance(self, p1: Point, p2: Point) -> float:
        
        """
        Computes the Euclidean distance between two points.

        Args:
            p1 (Point): The first point.
            p2 (Point): The second point.

        Returns:
            float: The distance between the two points.
        """
        
        return np.linalg.norm( np.array([p2.x, p2.y]) - np.array([p1.x, p1.y]) )
    
    def angle(self, p1: Point, p2: Point) -> np.array:
        
        """
        Computes the angle between two points.

        Args:
            p1 (Point): The first point.
            p2 (Point): The second point.

        Returns:
            np.array: The angle between the two points.
        """
        
        return np.arctan2((p2.x - p1.x), (p2.y - p1.y))
    
    
    def check_shape(self, p: np.array) -> int:
        
        """
        Determines the shape of the convex hull based on the number of points.

        Args:
            p (np.array): An array of Point objects representing the convex hull points.

        Returns:
            int: The shape of the convex hull.
        """
        
        if(p.size < 5):
            return SHAPE_NAME[str(p.size)]
        else:        
            return SHAPE_NAME["5"]
            
    def check_orientation(self, p1: Point, p2: Point, p3: Point) -> int:
        
        """
        Checks the orientation of three points (clockwise, counterclockwise, or colinear).

        Args:
            p1 (Point): The first point.
            p2 (Point): The second point.
            p3 (Point): The third point.

        Returns:
            int: The orientation of the points.
        """
        
        
        o = (p3.y - p2.y) * (p2.x - p1.x) - (p2.y - p1.y) * (p3.x - p2.x)
        
        if ( o > 0): 
            return -1 # clockwise
        elif (o < 0): 
            return 1 # counterclockwise
        else:  
            if self.distance(p1, p2) < self.distance(p3,p1):
                return 0 # colinear, closer to p2
            else:
                return 1 # colinear, closer to p3
    
    def graham(self) -> np.array:
        
        """
        Computes the convex hull using Graham's scan algorithm.

        Returns:
            np.array: An array of Point objects representing the convex hull points.
        """
        
        hull = np.array([], dtype=object)
        
        if (self.p.size < 3 ):
            hull = self.p
            for h in hull: 
                h.color = RED
            return hull
        
        
        i_min = 0 # minimum index, will be needed for swapping
        y_min = self.p[0].y # starting y coord of first point in array
        x_min = self.p[0].x # starting x coord of first point in array

        for x in range(1, self.p.size):

            if (self.p[x].y < y_min) or ((y_min == self.p[x].y) and (self.p[x].x < x_min)): 
                y_min = self.p[x].y
                x_min = self.p[x].x
                i_min = x
                
        p0 = self.p[i_min] # save p0

        self.p = np.delete(self.p, i_min) # delete p0 from array temp
        
        # sort depending on angle and distance 
        self.p = np.array(sorted(self.p, key=lambda p: (self.angle(p0,p), self.distance(p0, p))), dtype=object)
        
        #add p0 at the beggining of the array
        self.p = np.insert(self.p, 0, p0)
        
        # scan begin
        hull = self.p[0:2]
        
        for x in range(2, self.p.size):
            
            while  (hull.size >=2) and (self.check_orientation(hull[-2], hull[-1], self.p[x]) != 1):
                hull = hull[:-1]
            
            hull = np.append(hull, self.p[x])
                    
        # additional check at the end in case of colinearrity
        while (hull.size >= 2) and (self.check_orientation(hull[-2], hull[-1], hull[0]) != 1):            
            hull = hull[:-1]
            
        
        for h in hull:
            h.color = RED
            
        return hull

    def print_results(self) -> None:
        
        print("Input points: ")
        self.print_coords(self.p)
        
        print("Hull: ")
        self.print_coords(self.h)
        
        print(f"Shape of the hull: {self.check_shape(self.h)}")
        
    
    def print_coords(self, coords: np.array) -> None:
            print(', '.join(f"({p.x}, {p.y})" for p in coords))
    
# ------------------------------------------------------------------------        
class Draw:
    
    """
    Draws the points and convex hull on an image.
    """
    
    def __init__(self, points: np.array):
        self.points = points
        self.image  = Image.new("RGB", (MAX_H_P, MAX_W_P), WHITE)
        
        if not os.path.exists(IMG_DIR):
            os.makedirs(IMG_DIR)
        
    def draw_image(self) -> None:
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype(FONT_NAME, FONT_SIZE)
        draw.font = font

        # draw dots
        for p in self.points:
            x = p.x * X_OFFSET
            y = MAX_H_P - (p.y  * Y_OFFSET )
            draw.ellipse((x - DOT_SIZE, y -DOT_SIZE, x + DOT_SIZE, y + DOT_SIZE), outline= p.color)
            draw.text((x + DOT_SIZE * 2, y - DOT_SIZE * 2), f"( {p.x},  {p.y} )", fill=(0, 0, 0))
        self.image.save(f"{IMG_DIR}/points{random.randint(100,456)}.png")
        
        
# --------------------------------------------------------------------------------       
if __name__ == "__main__":
    
    g = Generator(POINTS_NUMBER)
    
    h = ComplexHull(g.get_points())
    h.print_results()

    d = Draw(g.get_points())
    d.draw_image()
        