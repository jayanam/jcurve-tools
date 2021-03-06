import bpy
from .vertices import VertexContainer

class CurveShape:

    def __init__(self):
        self._normals = []
        self._vertices = VertexContainer()

    def get_start_point(self):
        return self._vertices.get_vertices()[0]

    def get_end_point(self):
        return self._vertices.get_vertices()[-1]

    def append_vertex(self, vertex):
        self._vertices.append(vertex)

    def append(self, vertex, normal):
        self._vertices.append(vertex)
        self._normals.append(normal)

    def get_normal_start(self):
        return self._normals[0]

    def get_normal_end(self):
        return self._normals[-1]

    def get_vertices(self):
        return self._vertices.get_vertices()

    def draw(self) :
        self._vertices.draw()

    def reset(self):
        self._vertices.clear()
        self._normals.clear()