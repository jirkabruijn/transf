#!/usr/bin/env python
import math
import functools

class Transformation:

    def compose(self, f, g):
        print("scale:")
        print(self.scale)
        print("shift:")
        print(self.shift)
        print("f:")
        print(f)
        print("g:")
        print(g)
        compose = lambda x: g(f(x))
        return compose


class Scaling(Transformation):
    def __init__(self, scale):
        Transformation.__init__(self)
        Transformation.scale = scale

    def __call__(Transformation, p):
        x, y = p
        return [x*Transformation.scale, y*Transformation.scale]

    def __matmul__(self, *functions):

        composed = functools.reduce(self.compose, functions, lambda x: x)
        return composed


class Translation(Transformation):
    def __init__(self, shift):
        Transformation.__init__(self)
        Transformation.shift = shift

    def __call__(Transformation, p):
        return [x + y for x, y in zip(p, Transformation.shift)]

    def __matmul__(self, *functions):
        composed = functools.reduce(self.compose, functions, lambda x: x)
        return composed

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
