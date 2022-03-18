import bpy
from .vertices import VertexContainer

class LineShape:

    def __init__(self):
        self._vertices = VertexContainer()
        self._vertices.set_type('LINES')

    def get_start_point(self):
        return self._vertices.first_vertex

    def get_end_point(self):
        return self._vertices.last_vertex

    def append(self, vertex):
        self._vertices.append(vertex)

    def get_vertices(self):
        return self._vertices.get_vertices()

    def set_vertex(self, index, vertex):
        self._vertices.set_vertex(index, vertex)

    def draw(self):
        self._vertices.draw()

    def reset(self):
        self._vertices.clear()

    def is_initialized(self):
        return self._vertices.get_vertex_count() == 2