import bpy
from bpy.types import Panel

from . utils.modifier_utils import get_modifier_of_type

from . utils.select_utils import get_selected_curve, get_selected_object

class JCVT_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "JCurve"
    bl_category = "JCurve"

    def draw(self, context)    :
        pass

class JCVT_PT_Curve_Tools_Panel(Panel):
    bl_parent_id = "JCVT_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Curve & Mesh Tools"
    bl_category = "JCurve"

    def draw(self, context):
       
        layout = self.layout

        sel_curve = get_selected_curve(context)
        sel_object = get_selected_object(context)

        row = layout.row()
        col = row.column()
        col.label(text="Curve:")
        col = row.column()

        if sel_curve:
            col.label(text=sel_curve.name)

        row = layout.row()
        col = row.column()
        col.label(text="Object:")
        col = row.column()

        if sel_object:
            col.label(text=sel_object.name)

        # Properties of Array
        mod_array = get_modifier_of_type(sel_object, "ARRAY")
        if mod_array:
            row = layout.row()
            row.prop(mod_array, "fit_type")

            if mod_array.fit_type == "FIT_LENGTH":
                row = layout.row()
                row.prop(mod_array, "fit_length")

            if mod_array.fit_type == "FIXED_COUNT":
                row = layout.row()
                row.prop(mod_array, "count")
 
            row = layout.row()
            row.prop(mod_array, "relative_offset_displace", index=0, text="Offset")


        # Properties of simple deform
        mod_deform = get_modifier_of_type(sel_object, "SIMPLE_DEFORM")
        if mod_deform:
            row = layout.row()
            row.prop(mod_deform, "angle", text="Twist angle")

        if sel_curve:
            row = layout.row()
            row.prop(sel_curve.data, "bevel_depth")

        row = layout.row()
        col = row.column()
        op = col.operator('object.jcvt_create_curve_op', icon='OUTLINER_OB_CURVE', text="Create")

        col = row.column()
        op = col.operator('object.jcvt_remove_curve_op', icon='CANCEL', text="Remove")

class JCVT_PT_Curve_Creator_Panel(Panel):

    bl_parent_id = "JCVT_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Curve Creator"
    bl_category = "JCurve"

    def draw(self, context):

        layout = self.layout
        row = layout.row()
        row.operator('object.jcvt_create_curve_mode_op', icon='OUTLINER_OB_CURVE', text="Enter Creation Mode")

        row = layout.row()
        row.prop(context.scene, 'bevel_depth') 

        row = layout.row()
        row.operator('object.jcvt_curve_to_mesh_convert', icon='MESH_DATA', text="To Mesh")