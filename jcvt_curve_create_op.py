import bpy

from bpy.types import Operator
from bpy.props import *

from .utils.modifier_utils import *
from .utils.select_utils import *

class JCVT_OT_Curve_Remove(Operator):
    bl_idname = "object.jcvt_remove_curve_op"
    bl_label = "Remove Curve"
    bl_description = "Remove Curve" 
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):

        sel_object = get_selected_object(context)

        return has_modifiers(sel_object, ["ARRAY","CURVE" ])

    def execute(self, context):
        sel_object = get_selected_object(context)
        make_active(sel_object)
        bpy.ops.object.delete(use_global=False, confirm=False)

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

class JCVT_OT_Curve_Mesh_Create(Operator):
    bl_idname = "object.jcvt_curve_to_mesh_convert"
    bl_label = "Curve to Mesh"
    bl_description = "Convert curves to meshes and fill holes" 
    bl_options = {'REGISTER', 'UNDO'}   

    @classmethod
    def poll(cls, context): 

      selected_curves = [c for c in context.selected_objects if c.type == "CURVE" and c.visible_get()]
      if len(selected_curves) == 0:
          return False

      if not context.active_object:
          return False
          
      if context.active_object.mode != "OBJECT" and context.active_object.mode != "EDIT":
          return False
  
      return True

    def execute(self, context): 

        # Get all selected curves
        selected_curves = [c for c in context.selected_objects if c.type == "CURVE" and c.visible_get()]

        to_object()

        for curve in selected_curves:
          curve.data.use_fill_caps = True

        bpy.ops.object.convert(target='MESH')

        return {'FINISHED'}