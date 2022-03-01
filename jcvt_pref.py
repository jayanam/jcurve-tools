import bpy
from bpy.props import *

from bpy.types import AddonPreferences

def get_preferences():
    return bpy.context.preferences.addons[__package__].preferences

class JCurvePrefs(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout

        # row = self.layout.row()
        # row.label(text="Instant Meshes Application")
        # row.prop(self, 'im_filepath', text='')

        # row = self.layout.row()
        # row.label(text="Quadriflow Application (exe)")
        # row.prop(self, 'qf_filepath', text='')
