bl_info = {
    "name": "Portal Cube Spawner",
    "author": "RegularLunar",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Add > Mesh > Cube",
    "description": "Replaces the default Cube with a Portal Weighted Cube.",
    "category": "Object",
}

import bpy
import os
from bl_ui.space_view3d import VIEW3D_MT_mesh_add as OriginalMeshAddMenu

class MESH_OT_portal_cube_add(bpy.types.Operator):
    bl_idname = "mesh.portal_cube_add"
    bl_label = "Cube"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        addon_dir = os.path.dirname(__file__)
        portal_blend = os.path.join(addon_dir, "portal_cube.blend")
        
        if not os.path.exists(portal_blend):
            self.report({'ERROR'}, "portal_cube.blend not found in the add-on folder!")
            return {'CANCELLED'}
            
        with bpy.data.libraries.load(portal_blend) as (data_from, data_to):
            if "PortalCube" in data_from.objects:
                data_to.objects = ["PortalCube"]
        
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
                
                obj.location = context.scene.cursor.location
                
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                context.view_layer.objects.active = obj          
        return {'FINISHED'}


class Custom_VIEW3D_MT_mesh_add(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_mesh_add" 
    bl_label = "Mesh"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_plane_add", text="Plane", icon='MESH_PLANE')
        layout.operator("mesh.portal_cube_add", text="Cube", icon='MESH_CUBE') 
        layout.operator("mesh.primitive_circle_add", text="Circle", icon='MESH_CIRCLE')
        layout.operator("mesh.primitive_uv_sphere_add", text="UV Sphere", icon='MESH_UVSPHERE')
        layout.operator("mesh.primitive_ico_sphere_add", text="Ico Sphere", icon='MESH_ICOSPHERE')
        layout.operator("mesh.primitive_cylinder_add", text="Cylinder", icon='MESH_CYLINDER')
        layout.operator("mesh.primitive_cone_add", text="Cone", icon='MESH_CONE')
        layout.operator("mesh.primitive_torus_add", text="Torus", icon='MESH_TORUS')
        layout.separator()
        layout.operator("mesh.primitive_grid_add", text="Grid", icon='MESH_GRID')
        layout.operator("mesh.primitive_monkey_add", text="Monkey", icon='MESH_MONKEY')


def register():
    bpy.utils.register_class(MESH_OT_portal_cube_add)
    try:
        bpy.utils.unregister_class(OriginalMeshAddMenu)
    except Exception:
        pass
    bpy.utils.register_class(Custom_VIEW3D_MT_mesh_add)

def unregister():
    bpy.utils.unregister_class(MESH_OT_portal_cube_add)
    bpy.utils.unregister_class(Custom_VIEW3D_MT_mesh_add)
    bpy.utils.register_class(OriginalMeshAddMenu)

if __name__ == "__main__":
    register()
