import math
import random

MAX_LOCATION = 1000

def get_lower_bound(circle, radius):
    if circle > radius:
        return circle - radius
    else:
        return 0
    
def get_upper_bound(circle, radius):
    if circle + radius > MAX_LOCATION:
        return MAX_LOCATION
    else:
        return circle + radius


class Location:
    def __init__(self, x = 0.0, y = 0.0):
        self.l_x = x
        self.l_y = y

    def random_locaton(self):
        self.l_x = round(random.uniform(0, MAX_LOCATION), 2)
        self.l_y = round(random.uniform(0, MAX_LOCATION), 2)

    def random_location_with_circle(self, circle, radius):
        self.random_locaton()
        while not self.in_circle_range(circle, radius):
            self.l_x = round(random.uniform(get_lower_bound(circle.l_x, radius), get_upper_bound(circle.l_x, radius)), 2)
            self.l_y = round(random.uniform(get_lower_bound(circle.l_y, radius), get_upper_bound(circle.l_y, radius)), 2)

    def in_circle_range(self, circle, radius):
        distance = math.sqrt((self.l_x - circle.l_x)**2 + (self.l_y - circle.l_y)**2)
        if distance <= radius:
            return True
        else:
            return False

    def set_location(self, x, y):
        self.l_x = x
        self.l_y = y

    def show(self):
        print("location x is", self.l_x)
        print("location y is", self.l_y)



if __name__ == '__main__':
    location0 = Location()
    location0.random_locaton()
    location0.show()
    location1 = Location()
    location1.random_location_with_circle(location0, 100)
    location1.show()