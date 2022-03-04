import bpy

from bpy.types import Operator
from bpy.props import *

from .utils.modifier_utils import *

from .jcvt_pref import get_preferences

from .utils.select_utils import *

class JCVT_OT_Curve_Remove(Operator):
    bl_idname = "object.jcvt_remove_curve_op"
    bl_label = "Remove Curve"
    bl_description = "Remove Curve" 
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):

        sel_object = get_selected_object(context)

        return sel_object

    def execute(self, context):
        sel_object = get_selected_object(context)
        remove_modifier_of_type(sel_object, "ARRAY")
        remove_modifier_of_type(sel_object, "SIMPLE_DEFORM")
        remove_modifier_of_type(sel_object, "CURVE")
        return {'FINISHED'}

class JCVT_OT_Curve_Create(Operator):
    bl_idname = "object.jcvt_create_curve_op"
    bl_label = "Create Cables"
    bl_description = "Create Cables" 
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):

        sel_curve  = get_selected_curve(context)
        sel_object = get_selected_object(context)

        return sel_curve and sel_object

    def execute(self, context):

        sel_curves  = get_selected_curves(context)
        sel_object = get_selected_object(context)

        for sel_curve in sel_curves:

            deselect_all()

            make_active(sel_object)
            
            bpy.ops.object.duplicate(linked=False)

            active_obj = get_active()
            
            mod_array  = get_or_create_modifier(active_obj, "JCVT_Array", "ARRAY")
            mod_deform = get_or_create_modifier(active_obj, "JCVT_SimpleDeform", "SIMPLE_DEFORM")
            mod_curve  = get_or_create_modifier(active_obj, "JCVT_Curve", "CURVE")

            mod_array.use_merge_vertices = True
            mod_array.fit_type = 'FIT_CURVE'
            mod_array.curve = sel_curve

            mod_deform.angle = 0

            mod_curve.object = sel_curve
            mod_curve.show_in_editmode = True

            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            active_obj.location = (0,0,0)
   
        return {'FINISHED'}