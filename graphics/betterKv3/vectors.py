"""
STOLEN FROM KV3 MATH.VECTORS
I had to do some changes
"""

__all__ = ('Vector2', 'Vector3', 'Vector4', )

import math
from copy import copy

from kivy.graphics.transformation import Matrix
from kivy3.cameras import Camera as kv3Camera
from kivy3.math.vectors import Vector4 as kv3BaseVector, Vector3 as kv3Vector3


# Vector4 is a base vector but base vector isn't in __all__


class BaseVector(kv3BaseVector):
    @staticmethod
    def get_XY_from_camera(vector: kv3Vector3, camera: kv3Camera):
        print("a", vector, camera)
        print("a", vector, camera.pos)
        x, y = 0, 0

        distance = camera.pos.distance_to(vector)
        angel = Vector3(1, 1, 1).angle_to(vector)
        print("b", distance, angel)



        m = Matrix()
        v = vector
        pos = camera.pos
        m = m.look_at(pos[0], pos[1], pos[2], v[0], v[1], v[2],
                      camera.up[0], camera.up[1], camera.up[2])
        m = m.rotate(math.radians(camera.rot.x), 1.0, 0.0, 0.0)
        m = m.rotate(math.radians(camera.rot.y), 0.0, 1.0, 0.0)
        m = m.rotate(math.radians(camera.rot.z), 0.0, 0.0, 1.0)
        print("c", m)

        return [x, y]


class Vector4(BaseVector):
    pass


class Vector3(BaseVector):
    _d = 3
    _indeces = [0, 1, 2]
    _null = [0, 0, 0]
    _coords = {'x': 0, 'y': 1, 'z': 2}

    def cross(self, v):
        t = copy(self)

        self[0] = t[1] * v[2] - t[2] * v[1]
        self[1] = t[2] * v[0] - t[0] * v[2]
        self[2] = t[0] * v[1] - t[1] * v[0]

    @classmethod
    def cross_vectors(cls):
        pass



class Vector2(BaseVector):
    _d = 2
    _indeces = [0, 1]
    _null = [0, 0]
    _coords = {'x': 0, 'y': 1}

