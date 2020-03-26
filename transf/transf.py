#!/usr/bin/env python
import math
import functools
import numpy as np

class Transformation:

    def __init__(self):
        self.mx = np.array([[1,0,0],[0,1,0],[0,0,1]])

    def compose(self, f, g):
        func = lambda x: f(g(x))
        func.mx = lambda x: self.mx * f(x) * g(x)
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
        self.mx = []

    def __call__(self, p):
        x, y = p
        result = [x*self.scale, y*self.scale]
        self.mx = np.array(result)
        return result

    @property
    def matrix(self):
        return self.mx

class Translation(Transformation):
    def __init__(self, shift):
        Transformation.__init__(self)
        self.shift = shift
        self.mx = []

    def __call__(self, p):
        result = [x + y for x, y in zip(p, self.shift)]
        self.mx = np.array(result)
        return result

    @property
    def matrix(self):
        return self.mx


class Rotation(Transformation):
    def __init__(self, angle):
        Transformation.__init__(self)
        self.angle = angle
        self.mx = []

    def __call__(self, p):
        return self.rotate(p,[0,0],self.angle)

    def rotate(self, origin, point, angle):
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(-angle) * (px - ox) - math.sin(-angle) * (py - oy)
        qy = oy + math.sin(-angle) * (px - ox) + math.cos(-angle) * (py - oy)
        self.mx = np.array([qx, qy])
        return qx, qy

    @property
    def matrix(self):
        return self.mx
