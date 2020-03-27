#!/usr/bin/env python
import math
import functools
import numpy as np

class Transformation:

    def __init__(self):
        self.mx = np.array([[1,0,0],[0,1,0],[0,0,1]])

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def compose(self, f, g):
        func = lambda x: f(g(x))
        #self.mx = lambda x: self.mx * f(x) * g(x)
        self.mx = lambda x: f(x) * g(x)
        #func.matrix = self.mx
        return func

    def __matmul__(self, *functions):
        composed = (functools.reduce(self.compose, functions, self))
        #composed.matrix = self.mx
        #setattr(composed, 'matrix', self.mx)
        #composed.__setattr__('matrix', self.mx)
        #self.matrix = self.mx
        #composed.__dict__['matrix'] = self.mx

        return composed

    @property
    def matrix(self):
        return self.mx

    def base_matrix(self):
        return np.array([[1,0,0],[0,1,0],[0,0,1]])


class Scaling(Transformation):
    def __init__(self, scale):
        Transformation.__init__(self)
        self.scale = scale
        self.mx = []

    def __call__(self, p):
        x, y = p
        result = [x*self.scale, y*self.scale]
        #self.mx = np.array(self.construct_mx([p[0], p[1]]))
        self.mx = np.array(self.construct_mx())
        return result

    #def construct_mx(self, result):
    def construct_mx(self):

        #x = float(result[0])
        #y = float(result[1])
        x = float(self.scale)
        y = float(self.scale)
        #res_matrix = np.array([[x,0.0,0.0],[0.0,y,0.0],[0.0,0.0,1.0]])
        res_matrix = np.array([[x],[y],[1.0]])
        return res_matrix

class Translation(Transformation):
    def __init__(self, shift):
        Transformation.__init__(self)
        self.shift = shift
        self.mx = []

    def __call__(self, p):
        result = [x + y for x, y in zip(p, self.shift)]
        self.mx = np.array(self.construct_mx([p[0], p[1]]))
        #self.mx = np.array(self.construct_mx(result))
        return result

    def construct_mx(self, result):
        x = float(result[0])
        y = float(result[1])
        res_matrix = np.array([[1.0,0.0,x],[0.0,1.0,y],[0.0,0.0,1]])

        return res_matrix

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


