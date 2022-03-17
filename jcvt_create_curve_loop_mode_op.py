import blf
import bmesh
import bpy
from bpy.types import Operator
from bpy.props import *

from .types.line_shape import LineShape

from .types.vertices import *
from .utils.view_utils import *
from .utils.select_utils import *

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
            pass
            
        # Left mouse button is released
        if event.value == "RELEASE" and event.type == "LEFTMOUSE":
            pass

        # Left mouse button is pressed
        if event.value == "PRESS" and event.type == "LEFTMOUSE":

            mouse_pos_2d = (event.mouse_region_x, event.mouse_region_y)

            mouse_pos_3d = get_3d_vertex(context, mouse_pos_2d)
            if mouse_pos_3d:
               self._line_shape.append(mouse_pos_3d)
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
        blf.size(0, 22, 72)
        blf.color(0, 1, 1, 1, 1)

        blf.size(1, 16, 72)
        blf.color(1, 1, 1, 1, 1)

        title = "- Curve Loop Creation Mode -"
        desc = "Click: Start to draw Line"

        blf.position(0, xt - blf.dimensions(0, title)[0] / 2, 45, 0)
        blf.draw(0, title)

        blf.position(1, xt - blf.dimensions(0, desc)[0] / 2, 20, 0)
        blf.draw(1, desc)

	# Draw handler to paint in 3d view
    def draw_callback_3d(self, op, context):        
        self._line_shape.draw()