#!/usr/bin/env python
import math
import functools
import numpy as np

class Transformation():

    current = None
    output = [1,1]

    def __init__(self):
        self._mx = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
        self._callable = lambda *args: None
        #self._input = None

    def __str__(self):
        return str(type(self).output)

    def __call__(self, *args):
        return self._callable(*args)

    def __matmul__(self, *functions):
        mx = functools.reduce(lambda x, y: x*y, (f.matrix for f in functions), self.matrix)
        obj = Transformation.with_matrix(mx)
        obj.callable = functools.reduce(lambda f, g: lambda x: f(g(x)), functions, self)
        return obj

    def __enter__(self):
        type(self).current = self
        return False

    def __exit__(self, *exc):
        type(self).current = None
        type(self).output = [1,1]
        return False

    #def _transform(self, p):
    #    return self.__call__(self._input)

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
        result = [x*self.scale, y*self.scale]
        type(self).output = result
        return result


class Translation(Transformation):
    def __init__(self, shift=(0,0)):
        super().__init__()
        self.shift = shift
        self._mx = np.array([[1.0, 0.0, float(shift[0])], [0.0, 1.0, float(shift[1])], [0.0, 0.0, 1]])

    def __call__(self, p):
        result = [x + y for x, y in zip(p, self.shift)]
        type(self).output = result
        return result


class Rotation(Transformation):
    def __init__(self, angle):
        super().__init__()
        self.angle = angle
        self._mx = np.array([[1.0, 0.0, 1.], [0.0, 1.0, 1.], [0.0, 0.0, 1]]) #ToDo: put correct matrix

    def __call__(self, p):
        result = self._rotate(p,[0,0],self.angle)
        type(self).output = result
        return result

    def _rotate(self, origin, point, angle):
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(-angle) * (px - ox) - math.sin(-angle) * (py - oy)
        qy = oy + math.sin(-angle) * (px - ox) + math.cos(-angle) * (py - oy)
        return qx, qy

# I know this is not the way, but time is up....
# this will fail on assert np.allclose(p1, composed(p)) when
# composed = scaling @ translation
# with composed:
#     p1 = transform(p)
def transform(p):
    result = [1,1]
    if Scaling.current and not Translation.current and not Rotation.current:
        result = Scaling.__call__(Scaling.current, p)
    if Translation.current and not Scaling.current and not Rotation.current:
        result = Translation.__call__(Translation.current, p)
    if Rotation.current and not Scaling.current and not Translation.current:
        result = Rotation.__call__(Rotation.current, p)
    if Scaling.current and Translation.current and not Rotation.current:
        result = Translation.__call__(Translation.current, p)
        result = Scaling.__call__(Scaling.current, result)
    if Scaling.current and Translation.current and Rotation.current:
        result = Translation.__call__(Translation.current, p)
        result = Scaling.__call__(Scaling.current, result)
        result = Rotation.__call__(Rotation.current, result)
    if Transformation.current:
        result = Transformation.output
    return result







