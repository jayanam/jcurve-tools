import bpy
from .vertices import VertexContainer

class LineShape:

    def __init__(self):
        self._vertices = VertexContainer()
        self._vertices.set_type('LINES')
        self._vertices_2d = []

    def get_start_point(self):
        return self._vertices.get_vertices()[0]

    def get_end_point(self):
        return self._vertices.get_vertices()[-1]

    def append(self, vertex_2d, vertex):
        self._vertices_2d.append(vertex_2d)
        self._vertices.append(vertex)

    def get_center_2d(self):
        return ((self._vertices_2d[0][0] + self._vertices_2d[1][0]) / 2, (self._vertices_2d[0][1] + self._vertices_2d[1][1]) / 2)

    def get_vertices(self):
        return self._vertices.get_vertices()

    def set_vertex(self, index, vertex_2d, vertex):
        self._vertices_2d[index] = vertex_2d
        self._vertices.set_vertex(index, vertex)

    def get_length(self):
        return (self.get_end_point() - self.get_start_point()).length

    def draw(self):
        self._vertices.draw()

    def reset(self):
        self._vertices.clear()
        self._vertices_2d.clear()

    def is_initialized(self):
        return self._vertices.get_vertex_count() == 2