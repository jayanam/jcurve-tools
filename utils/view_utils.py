import bpy

from bpy_extras.view3d_utils import (
    region_2d_to_origin_3d,
    region_2d_to_vector_3d,
    region_2d_to_location_3d
)

import mathutils

def get_view_rotation(context):
    rv3d      = context.space_data.region_3d
    view_rot  = rv3d.view_rotation
    return view_rot  

def get_view_direction(context):
    view_rot  = get_view_rotation(context)
    
    dir = view_rot @ mathutils.Vector((0,0,-1))

    return dir.normalized()

def get_view_matrix(context):
    rv3d      = context.space_data.region_3d
    view_matrix = rv3d.view_matrix
    x, y, z = view_matrix.to_3x3()
    return x, y, z


def get_3d_vertex(context, vertex_2d):
    region    = context.region
    rv3d      = context.space_data.region_3d

    dir = get_view_direction(context) * -1
    
    return region_2d_to_location_3d(region, rv3d, vertex_2d, dir)   

def get_3d_for_2d(pos_2d, context):

    result = None, None, None

    scene = context.scene

    origin, direction = get_origin_and_direction(pos_2d, context)
    
    # Try to hit an object in the scene
    ray_cast_param = __get_raycast_param(context.view_layer)
    hit, hit_vertex, normal, hit_face, hit_obj, *_ = scene.ray_cast(ray_cast_param, origin, direction)

    if hit:
        result = hit_vertex.copy(), hit_obj, normal
        
    return result

def __get_raycast_param(view_layer):        
    if bpy.app.version >= (2, 91, 0):
        return view_layer.depsgraph
    else:
        return view_layer 

def get_origin_and_direction(pos_2d, context):
    region    = context.region
    region_3d = context.space_data.region_3d
    
    origin    = region_2d_to_origin_3d(region, region_3d, pos_2d)
    direction = region_2d_to_vector_3d(region, region_3d, pos_2d)

    return origin, direction

def get_center_vectors(v1 : mathutils.Vector, v2 : mathutils.Vector):
    region    = bpy.context.region
    rv3d      = bpy.context.space_data.region_3d

    return (v2 + v1) / 2

def obj_ray_cast(direction, origin, context):
    obj = context.object

    """Wrapper for ray casting that moves the ray into object space"""

    ray_target = origin + direction

    matrix = obj.matrix_world.copy()

    # get the ray relative to the object
    matrix_inv = matrix.inverted()
    ray_origin_obj = matrix_inv @ origin
    ray_target_obj = matrix_inv @ ray_target
    ray_direction_obj = ray_target_obj - ray_origin_obj

    # cast the ray
    success, location, normal, face_index = obj.ray_cast(ray_origin_obj, ray_direction_obj)

    return success, location


def scene_raycast(direction, origin, context):

    scene = context.scene

    # Try to hit an object in the scene
    ray_cast_param = __get_raycast_param(context.view_layer)
    hit, hit_vertex, normal, hit_face, hit_obj, *_ = scene.ray_cast(ray_cast_param, origin, direction)
    return hit, hit_vertex