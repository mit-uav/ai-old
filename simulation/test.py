import math
from math import pi, sqrt, atan2

tuples = [(0, 0), (1, 1), (math.sqrt(3), 1), (1, sqrt(3)), (-1, -sqrt(3))]
for (x, y) in tuples: 
    angle = (atan2(y, x))
    if angle < 0:
        angle += 2*pi
    print angle*180/pi
