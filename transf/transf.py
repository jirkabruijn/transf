#!/usr/bin/env python
import math
import functools
import numpy as np

class Transformation:

    def compose(self, f, g):
        func = lambda x: f(g(x))
        return func

    def __matmul__(self, *functions):
        #print("matmul")
        #print("__matmul__", functions)
        composed = functools.reduce(self.compose, functions, self)
        #print("composed:", composed)
        return composed


class Scaling(Transformation):
    def __init__(self, scale):
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
    def __init__(self, angle):
        Transformation.__init__(self)
        self.angle = angle

    def __call__(self, p):
        return self.rotate(p,[0,0],self.angle)

    def rotate(self, origin, point, angle):
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(-angle) * (px - ox) - math.sin(-angle) * (py - oy)
        qy = oy + math.sin(-angle) * (px - ox) + math.cos(-angle) * (py - oy)
        return qx, qy
