import blf
import math
import bpy
from bpy.types import Operator
from bpy.props import *

from .utils.curve_utils import *

from .types.curve_shape import CurveShape
from .types.line_shape import LineShape

from .types.vertices import *
from .utils.view_utils import *
from .utils.select_utils import *
from .utils.textutils import blf_set_size

class JCVT_OT_Create_Curve_Loop_Mode_Operator(Operator):
    bl_idname = "object.jcvt_create_curve_loop_mode_op"
    bl_label = "Create Curve Loop Mode Operator"
    bl_description = "Create Curve Loop Mode Operator"
    bl_options = {"REGISTER", "UNDO", "BLOCKING"}

    @classmethod
    def poll(cls, context): 

        if context.window_manager.in_curve_mode:
            return False

        return True
		
    def __init__(self):
        self.draw_handle_2d = None
        self.draw_handle_3d = None
        self._line_shape = LineShape()
        self._loop_shape = CurveShape()

        self._debug_shape = CurveShape()

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


        # The mouse is moved
        if event.type == "MOUSEMOVE":
            mouse_pos_2d = (event.mouse_region_x, event.mouse_region_y)
            mouse_pos_3d = get_3d_vertex(context, mouse_pos_2d)

            if mouse_pos_3d and self._line_shape.is_initialized():
                self._line_shape.set_vertex(1, mouse_pos_2d, mouse_pos_3d)
            
        # Left mouse button is released
        if event.value == "RELEASE" and event.type == "LEFTMOUSE":
            pass

        # Left mouse button is pressed
        if event.value == "PRESS" and event.type == "LEFTMOUSE":

            mouse_pos_2d = (event.mouse_region_x, event.mouse_region_y)

            mouse_pos_3d = get_3d_vertex(context, mouse_pos_2d)
            if mouse_pos_3d:

                if not self._line_shape.is_initialized() and event.ctrl:
                    self._line_shape.append(mouse_pos_2d, mouse_pos_3d)
                    self._line_shape.append(mouse_pos_2d, mouse_pos_3d.copy())
                    result = "RUNNING_MODAL"

                elif self._line_shape.is_initialized() :
                    self.project_loop_onto_object(context)
                    self._line_shape.reset()
                    self._loop_shape.reset()
                    result = "RUNNING_MODAL"

        return { result }     

    def finish(self):
        self.unregister_handlers(bpy.context)
        return {"FINISHED"}


	# Draw handler to paint in pixels
    def draw_callback_2d(self, op, context):

        region = context.region
        xt = int(region.width / 2.0)

        # Draw text for draw mode
        blf_set_size(0,22)

        blf.color(0, 1, 1, 1, 1)

        blf_set_size(1, 16)
        blf.color(1, 1, 1, 1, 1)

        title = "- Curve Loop Creation Mode -"

        if not self._line_shape.is_initialized():
            desc = "Ctrl + Click: Start to draw line"
        else:
            desc = "Click: End line"

        blf.position(0, xt - blf.dimensions(0, title)[0] / 2, 45, 0)
        blf.draw(0, title)

        blf.position(1, xt - blf.dimensions(1, desc)[0] / 2, 20, 0)
        blf.draw(1, desc)

	# Draw handler to paint in 3d view
    def draw_callback_3d(self, op, context):        
        self._line_shape.draw()
        self._loop_shape.draw()
        # self._debug_shape.draw()

    def project_loop_onto_object(self, context):

        center_object, direction = self.get_center_object(context)

        # self._debug_shape.append_vertex(center_object)

        # 6. Draw cirle around center_object, diameter = line_length
        v1_n = (self._line_shape.get_end_point() - self._line_shape.get_start_point()).normalized()

        t = 0
        r = self._line_shape.get_length() / 2

        circle_points = []

        while t < 2 * math.pi:
            circle_points.append(center_object + r * math.cos(t) * v1_n + r * math.sin(t) * direction)
            t += 2 * math.pi / context.scene.loop_cuts

        # 7. raycast all points of the circle in direction to center_object and collect hit_points
        for cp in circle_points:
            hit, hit_vertex = scene_raycast(-(cp - center_object).normalized(), cp, context)
            if hit:
                self._loop_shape.append_vertex(hit_vertex)

        # 8. Create curve from points
        self.to_curve(context)


    def to_curve(self, context):
        
        path_from_vertices(context, self._loop_shape.get_vertices())

        context.object.data.splines[0].use_cyclic_u = True

        to_object()

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        apply_bevel(context)
        
    def get_center_object(self, context):
        
        # 1. Get center of line (line_center)     
        # 2. raycast from line_center onto selected object (line_center_hit1)
        # 3. raycast from line_center_hit1 in the same direction (line_center_hit2)
        # 4. get center of line_center_hit1 and line_center_hit2 (center_object)

        origin, direction = get_origin_and_direction( self._line_shape.get_center_2d(), context)

        _, line_center_hit1 = scene_raycast(direction, origin, context)

        # self._debug_shape.append_vertex(line_center_hit1)

        _, line_center_hit2 = scene_raycast(direction, line_center_hit1 + (direction * 0.01), context)

        # self._debug_shape.append_vertex(line_center_hit2)

        return get_center_vectors(line_center_hit1, line_center_hit2), direction