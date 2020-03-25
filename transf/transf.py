#!/usr/bin/env python
import math
import functools

class Transformation:
    def __init__(self, scale=0, shift=None, angle=0):
        self.scale = scale
        self.shift = shift
        self.angle = angle

    '''def __matmul__(self, *functions):
        def compose2(f, g):
            return lambda x: f(g(x))

        return functools.reduce(compose2, functions, lambda x: x)'''

    def __matmul__(self, *functions):
        def compose2(f, g):
            #compose = lambda f, g: (lambda x: f(g(x)))
            print("scale:")
            print(self.scale)
            print("shift:")
            print(self.shift)
            print("shift:")
            self.shift = [1, 2]
            print(self.shift)
            print(f)
            print(g)
            compose = lambda x: f(g(x))
            return compose

        return functools.reduce(compose2, functions, lambda x: x)

    '''def __matmul__(self, *functions):
        return Compose(functions(lambda x: x))'''



class Scaling(Transformation):

    def __call__(Transformation, p):
        x, y = p
        return [x*Transformation.scale, y*Transformation.scale]


class Translation(Transformation):

    def __call__(Transformation, p):
        return [x + y for x, y in zip(p, Transformation.shift)]

class Rotation(Transformation):

    def __call__(Transformation, p):
        return Transformation.rotate(p,[0,0],Transformation.angle)

    def rotate(self, origin, point, angle):
        #this one i had to look up:
        #https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(-angle) * (px - ox) - math.sin(-angle) * (py - oy)
        qy = oy + math.sin(-angle) * (px - ox) + math.cos(-angle) * (py - oy)
        return qx, qy


'''class Compose(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, x):
        return self.func(x)

    def __mul__(self, neighbour):
        return Compose(lambda x: self.func(neighbour.func(x)))'''