# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Test",
    "description": "Test",
    "author": "Marek Hanzelka",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "Test",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}

import bpy
from bpy.types import Operator

def OriginToSelected(context):
    try:
        cursorPositionX = context.scene.cursor.location[0]
        cursorPositionY = context.scene.cursor.location[1]
        cursorPositionZ = context.scene.cursor.location[2]
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.object.mode_set(mode='EDIT')
        context.scene.cursor.location[0] = cursorPositionX
        context.scene.cursor.location[1] = cursorPositionY
        context.scene.cursor.location[2] = cursorPositionZ
        return True
    except:
        return False


def add_set_origin_entry(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("object.setorigintoselected_edit", text="Snap Origin to Selected", icon="TRANSFORM_ORIGINS")

# Add the operator and entry to the shape key context menu
def register():
    bpy.utils.register_class(SetOriginToSelected_edit)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(add_set_origin_entry)

# Remove the operator and entry from the shape key context menu
def unregister():
    bpy.utils.unregister_class(SetOriginToSelected_edit)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(add_set_origin_entry)

# Operator class
class SetOriginToSelected_edit(Operator):
    bl_idname = "object.setorigintoselected_edit"
    bl_label = "Set Origin to Selected"
    bl_description = "Set Origin to Selected"

    @classmethod
    def poll(cls, context):
        return (context.area.type == "VIEW_3D" and context.active_object is not None)

    def execute(self, context):
        check = OriginToSelected(context)
        if not check:
            self.report({"ERROR"}, "Set Origin to Selected could not be performed")
            return {'CANCELLED'}

        return {'FINISHED'}


if __name__ == "__main__":
    register()
