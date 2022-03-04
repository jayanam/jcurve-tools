import bpy
from bpy.types import Panel

from . utils.modifier_utils import get_modifier_of_type

from . utils.select_utils import get_selected_curve, get_selected_object

class JCVT_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Curve Creator"
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

        row = layout.row()
        col = row.column()
        col.label(text="Twist:")

        col = row.column()

        mod_deform = get_modifier_of_type(sel_object, "SIMPLE_DEFORM")
        if mod_deform:
            col.prop(mod_deform, "angle")

        row = layout.row()
        col = row.column()
        op = col.operator('object.jcvt_create_curve_op', icon='OUTLINER_OB_CURVE', text="Create")

        col = row.column()
        op = col.operator('object.jcvt_remove_curve_op', icon='CANCEL', text="Remove")

        row = layout.row()
        row.operator('object.jcvt_create_curve_mode_op', icon='OUTLINER_OB_CURVE', text="Curve Creation Mode")


        