import blf
import bmesh
import bpy
from bpy.types import Operator
from bpy.props import *
from . types.curve_shape import CurveShape

from . types.vertices import *
from . utils.view_utils import *
from . utils.select_utils import *

class JCVT_OT_Create_Curve_Mode_Operator(Operator):
    bl_idname = "object.jcvt_create_curve_mode_op"
    bl_label = "Create Curve Mode Operator"
    bl_description = "Create Curve Mode Operator"
    bl_options = {"REGISTER", "UNDO", "BLOCKING"}

    @classmethod
    def poll(cls, context): 

        if context.window_manager.in_curve_mode:
            return False

        return True
		
    def __init__(self):
        self.draw_handle_2d = None
        self.draw_handle_3d = None
        self._curve_shape = CurveShape()

    def invoke(self, context, event):
        args = (self, context)  

        context.window_manager.in_curve_mode = True   

        # Register drawing handlers for 2d and 3d
        self.register_handlers(args, context)
                   
        # Register as modal operator
        context.window_manager.modal_handler_add(self)

        return {"RUNNING_MODAL"}
    
    def register_handlers(self, args, context):
        self.draw_handle_3d = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_3d, args, "WINDOW", "POST_VIEW")

        self.draw_handle_2d = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_2d, args, "WINDOW", "POST_PIXEL")
        
    def unregister_handlers(self, context):

        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle_2d, "WINDOW")
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle_3d, "WINDOW")
        
        self.draw_handle_2d = None
        self.draw_handle_3d = None
        context.window_manager.in_curve_mode = False

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        result = "PASS_THROUGH"
                              
        if event.type == "ESC" and event.value == "PRESS":
            return self.finish()

        if event.type == "RET" and event.value == "PRESS":
            if event.ctrl:
                self.to_bezier(context)
            else:
                self.to_curve(context)

            self._curve_shape.reset()

        # The mouse is moved
        if event.type == "MOUSEMOVE":
            pass
            
        # Left mouse button is released
        if event.value == "RELEASE" and event.type == "LEFTMOUSE":
            pass

        # Left mouse button is pressed
        if event.value == "PRESS" and event.type == "LEFTMOUSE":
            if event.ctrl:
                mouse_pos_2d = (event.mouse_region_x, event.mouse_region_y)
                mouse_pos_3d, hit_object, normal = get_3d_for_2d(mouse_pos_2d, context)
                if mouse_pos_3d and hit_object:
                    self._curve_shape.append(mouse_pos_3d, normal)
                    result = "RUNNING_MODAL"

        return { result }

    def finish(self):
        self.unregister_handlers(bpy.context)
        return {"FINISHED"}

    def to_bezier(self, context):

        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, location=(0, 0, 0))

        if context.scene.bevel_depth > 0:
            bpy.context.object.data.bevel_depth = context.scene.bevel_depth
            bpy.context.object.data.use_fill_caps = True

        vertices = self._curve_shape.get_vertices().copy()
        curve = context.active_object
        
        bez_points = curve.data.splines[0].bezier_points
        point_count = len(bez_points) - 1
        curve.data.splines[0].resolution_u = 24

        norm_start = self._curve_shape.get_normal_start()
        norm_end = self._curve_shape.get_normal_end()

        bez_points[0].co = vertices[0]
        if norm_start is not None:
            bez_points[0].handle_right = bez_points[0].co + norm_start
            bez_points[0].handle_left = bez_points[0].co - norm_start

        bez_points[point_count].co = vertices[-1]
        if norm_end is not None:
            bez_points[point_count].handle_right = bez_points[point_count].co - norm_end
            bez_points[point_count].handle_left = bez_points[point_count].co + norm_end

        to_object()

    def to_curve(self, context):
        
        to_object()

        bpy.ops.curve.primitive_nurbs_path_add(enter_editmode=True)
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.delete()

        vertices = self._curve_shape.get_vertices().copy()
        if vertices:
            for vertex in vertices:
                bpy.ops.curve.vertex_add(location=vertex)

        to_object()


	# Draw handler to paint in pixels
    def draw_callback_2d(self, op, context):

        region = context.region
        xt = int(region.width / 2.0)

        # Draw text for draw mode
        blf.size(0, 22, 72)
        blf.color(0, 1, 1, 1, 1)

        blf.size(1, 16, 72)
        blf.color(1, 1, 1, 1, 1)

        title = "- Curve Creation Mode -"
        desc = "Ctrl + Click: Add point, Enter: Create, Ctrl + Enter: Create snapped, Esc: Close"

        blf.position(0, xt - blf.dimensions(0, title)[0] / 2, 45, 0)
        blf.draw(0, title)

        blf.position(1, xt - blf.dimensions(0, desc)[0] / 2, 20, 0)
        blf.draw(1, desc)

	# Draw handler to paint in 3d view
    def draw_callback_3d(self, op, context):        
        self._curve_shape.draw()