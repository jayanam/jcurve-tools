import bpy

from ..types.vertices import VertexContainer

def apply_bevel(context):
    if context.scene.bevel_depth > 0:
        bpy.context.object.data.bevel_depth = context.scene.bevel_depth
        bpy.context.object.data.use_fill_caps = True

def path_from_vertices(context, vertices : VertexContainer):
  
    bpy.ops.curve.primitive_nurbs_path_add(enter_editmode=True)
    bpy.ops.curve.select_all(action='SELECT')
    bpy.ops.curve.delete()

    if vertices:
      for vertex in vertices.copy():
          bpy.ops.curve.vertex_add(location=vertex)