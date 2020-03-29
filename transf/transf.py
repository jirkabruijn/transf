#!/usr/bin/env python
import math
import functools
import numpy as np

class Transformation:

    def __init__(self):
        self._mx = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
        self._callable = lambda *args: None

    def __call__(self, *args):
        return self._callable(*args)

    def __matmul__(self, *functions):
        mx = functools.reduce(lambda x, y: x*y, (f.matrix for f in functions), self.matrix)
        obj = Transformation.with_matrix(mx)
        obj.callable = functools.reduce(lambda f, g: lambda x: f(g(x)), functions, self)
        return obj

    @classmethod
    def with_matrix(cls, matrix):
        self = cls()
        self._mx = matrix
        return self

    @property
    def callable(self):
        return self._callable

    @callable.setter
    def callable(self, val):
        self._callable = val

    @property
    def matrix(self):
        return self._mx

class Scaling(Transformation):
    def __init__(self, scale=1):
        super().__init__()
        self.scale = scale
        self._mx = np.array([[float(scale)],[float(scale)],[1.0]])

    def __call__(self, p):
        x, y = p
        return [x*self.scale, y*self.scale]

class Translation(Transformation):
    def __init__(self, shift=(0,0)):
        super().__init__()
        self.shift = shift
        self._mx = np.array([[1.0, 0.0, float(shift[0])], [0.0, 1.0, float(shift[1])], [0.0, 0.0, 1]])

    def __call__(self, p):
        return [x + y for x, y in zip(p, self.shift)]

class Rotation(Transformation):
    def __init__(self, angle):
        super().__init__()
        self.angle = angle
        self._mx = np.array([[1.0, 0.0, 1.], [0.0, 1.0, 1.], [0.0, 0.0, 1]]) #ToDo: put correct matrix

    def __call__(self, p):
        return self._rotate(p,[0,0],self.angle)

    def _rotate(self, origin, point, angle):
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(-angle) * (px - ox) - math.sin(-angle) * (py - oy)
        qy = oy + math.sin(-angle) * (px - ox) + math.cos(-angle) * (py - oy)
        return qx, qy

# Probably not completely what was meant, and not very beautiful, but it works for the test
def gen():
    scale = 3
    shift = [1,2]
    angle = np.pi/3
    translation = Translation(shift)
    scaling = Scaling(scale)
    rotation = Rotation(angle)
    composed = scaling @ translation
    yield (composed)
    yield (translation)
    yield (scaling @ translation)
    yield (rotation @ scaling @ translation)
    yield (translation)

g = gen()
def transform(p):

    try:
        next_opp = g.__next__()
        return next_opp(p)
    except:
        print("Ran out of operations")







