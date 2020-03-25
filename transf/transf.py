#!/usr/bin/env python
import math
import functools

class Transformation:
    def __int__(self):
        self.nothing = 0

    def compose(*functions):
        def compose2(f, g):
            return lambda x: f(g(x))

        return functools.reduce(compose2, functions, lambda x: x)

class Scaling(Transformation):
    def __init__(self, scale=0):
        Transformation.__init__(self)
        self.scale = scale

    def __call__(self, p):
        x, y = p
        return [x*self.scale, y*self.scale]


class Translation(Transformation):
    def __init__(self, shift):
        Transformation.__init__(self)
        self.shift = shift

    def __call__(self, p):
        return [x + y for x, y in zip(p, self.shift)]

class Rotation(Transformation):
    def __init__(self, angle=0):
        Transformation.__init__(self)
        self.angle = angle

    def __call__(self, p):
        return self.rotate(p,[0,0],self.angle)

    def rotate(self, origin, point, angle):
        #this one i had to look up:
        #https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(-angle) * (px - ox) - math.sin(-angle) * (py - oy)
        qy = oy + math.sin(-angle) * (px - ox) + math.cos(-angle) * (py - oy)
        return qx, qy


