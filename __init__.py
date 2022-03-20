bl_info = {
    "name" : "JCurve Tools",
    "author" : "jayanam",
    "description" : "Curve tools for Blender 2.8 - 3.x",
    "blender" : (2, 80, 0),
    "version" : (0, 4, 2, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy
from bpy.props import *

# Properties
bpy.types.WindowManager.in_curve_mode = bpy.props.BoolProperty(name="Curve Mode", default = False)

bpy.types.Scene.bevel_depth = bpy.props.FloatProperty(name="Bevel Depth", default = 0)

from .jcvt_panel import *
from .jcvt_curve_create_op import *
from .jcvt_pref import JCurvePrefs
from .jcvt_create_curve_mode_op import *
from .jcvt_create_curve_loop_mode_op import *


addon_keymaps = []

classes = ( JCVT_PT_Panel, JCVT_OT_Curve_Create, JCVT_OT_Curve_Remove, JCVT_OT_Curve_Mesh_Create,
            JCVT_OT_Create_Curve_Mode_Operator, JCurvePrefs,
            JCVT_PT_Curve_Tools_Panel, JCVT_PT_Curve_Creator_Panel, JCVT_OT_Curve_From_Mesh_Create,
            JCVT_OT_Create_Curve_Loop_Mode_Operator)

def register():
    for c in classes:
        bpy.utils.register_class(c)

    # add keymap entry
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
 
    # remove keymap entry
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()
    
if __name__ == "__main__":
    register()
