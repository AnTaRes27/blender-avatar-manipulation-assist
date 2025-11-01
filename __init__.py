"""/// ANTARES AVATAR MANIUPLATION ASSIST v0.2.0 //////////////////////////////
 ///
//    HELLO!
//
//    COPYRIGHT (C) 2022 ANTARES HUSKY (HUSKY@ANTARES.DOG)
//
////////////////////////////////////////////////////////////////////////////"""

# bl_info = {
#     'name' : 'Antares Avatar Manipulation Assist',
#     'author' : 'Antares Husky',
#     'version' : (0, 2, 0),
#     'blender' : (3, 3, 1),
#     'location': 'View3D > NTRZ',
#     'warning': 'I may or may not know what I\'m doing',
#     'wiki_url': 'http:\\\\antares.dog',
#     'category': 'View3D'
# }

import bpy

from .housekeeping import NTRZ_OT_housekeeping_actions
from .ui import (
    NTRZ_PT_shapekey_insert,
    NTRZ_PT_shapekey_manip,
    NTRZ_UL_shapekey_list,
    NTRZ_PT_breathing_assist,
    NTRZ_UL_breathing_shapekey_list,
    NTRZ_PT_vertgroup_manip,
    NTRZ_UL_vertgroup_list,
    NTRZ_PT_housekeeping
    )
from .shapekey_manip import (
    NTRZ_OT_add_shapekey,
    NTRZ_OT_add_shapekey_spacer,
    NTRZ_OT_rename_shapekey,
    NTRZ_OT_manip_shapekey_list_bulk_add_actions,
    NTRZ_OT_manip_shapekey_list_actions,
    NTRZ_OT_manip_shapekey_clear_list,
    NTRZ_OT_manip_shapekey_list_remove_duplicates,
    NTRZ_OT_manip_shapekey_actions,
    NTRZ_OT_breathing_shapekey_list_actions,
    NTRZ_OT_breathing_shapekey_clear_list,
    NTRZ_OT_breathing_shapekey_transfer,
    NTRZ_PG_manip_shapekey_settings,
    NTRZ_PG_manip_shapekey_list,
    NTRZ_PG_breathing_assist,
    NTRZ_PG_breathing_shapekey_list
    )
from .vertgroup_manip import (
    NTRZ_PG_vertgroup_manip_settings,
    NTRZ_PG_vertgroup_manip_list,
    NTRZ_OT_vertgroup_manip_list_bulk_add_actions,
    NTRZ_OT_vertgroup_manip_list_actions,
    NTRZ_OT_vertgroup_manip_clear_list,
    NTRZ_OT_vertgroup_manip_list_remove_duplicates,
    NTRZ_OT_vertgroup_manip_duplicate_and_rename,
    NTRZ_OT_vertgroup_manip_remove_zero_weight_vertgroup,
    NTRZ_OT_vertgroup_manip_transfer_vertex_weight,
    NTRZ_OT_vertgroup_manip_project_vertex_weight
    )

#////////////////////////////////////////////////#

class NTRZ_OT_unload(bpy.types.Operator):
    bl_idname = 'ntrz.unload'
    bl_label = 'Unload NTRZ'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        unregister()
        return{"FINISHED"}

class TestPanel(bpy.types.Panel):
    bl_idname = 'PT_TestPanel'
    bl_label = 'TestPanel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NTRZ'
        
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text='Ahoy!', icon='CUBE')
        
        
        row = layout.row()
        row.operator('ntrz.unload')

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#
#>>           REGISTER & UNREGISTER             <<
#////////////////////////////////////////////////#

classes = (
        TestPanel,
        NTRZ_PT_shapekey_insert,
        NTRZ_PT_shapekey_manip,
        NTRZ_UL_shapekey_list,
        NTRZ_PT_breathing_assist,
        NTRZ_UL_breathing_shapekey_list,
        NTRZ_OT_add_shapekey,
        NTRZ_OT_add_shapekey_spacer,
        NTRZ_OT_rename_shapekey,
        NTRZ_OT_manip_shapekey_list_bulk_add_actions,
        NTRZ_OT_manip_shapekey_list_actions,
        NTRZ_OT_manip_shapekey_clear_list,
        NTRZ_OT_manip_shapekey_list_remove_duplicates,
        NTRZ_OT_manip_shapekey_actions,
        NTRZ_OT_unload,
        NTRZ_PG_manip_shapekey_settings,
        NTRZ_PG_manip_shapekey_list,
        NTRZ_PG_breathing_assist,
        NTRZ_PG_breathing_shapekey_list,
        NTRZ_OT_breathing_shapekey_list_actions,
        NTRZ_OT_breathing_shapekey_clear_list,
        NTRZ_OT_breathing_shapekey_transfer,
        NTRZ_PT_housekeeping,
        NTRZ_OT_housekeeping_actions,
        NTRZ_PT_vertgroup_manip,
        NTRZ_UL_vertgroup_list,
        NTRZ_PG_vertgroup_manip_settings,
        NTRZ_PG_vertgroup_manip_list,
        NTRZ_OT_vertgroup_manip_list_bulk_add_actions,
        NTRZ_OT_vertgroup_manip_list_actions,
        NTRZ_OT_vertgroup_manip_clear_list,
        NTRZ_OT_vertgroup_manip_list_remove_duplicates,
        NTRZ_OT_vertgroup_manip_duplicate_and_rename,
        NTRZ_OT_vertgroup_manip_remove_zero_weight_vertgroup,
        NTRZ_OT_vertgroup_manip_transfer_vertex_weight,
    )

def register():
    from bpy.utils import register_class
    for cls in classes:
        print('registering %s' % cls)
        register_class(cls)
        
    from bpy.types import Scene
    from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty, CollectionProperty, PointerProperty

    Scene.NTRZ_shapekey_name = StringProperty(
        name='Shapekey Name'
    )

    Scene.NTRZ_shapekey_name_affix = EnumProperty(
        name='Shapekey Affix',
        description='',
        items=[
            ("BLANK", ' ', ''),
            ("HDG1", '╠══', ''),
            ("HDG2", '╠═', ''),
        ]
    )

    Scene.NTRZ_shapekey_insert_location = EnumProperty(
        name='Shapekey Insert Location',
        description='',
        items=[
            ("BEFORE_ACTIVE", 'Insert Before Selected', ''),
            ("LAST", 'Insert Last', '')
        ],
        default='BEFORE_ACTIVE'
    )

    Scene.NTRZ_shapekey_manip_location = EnumProperty(
        name='Shapekey Manipulate Location',
        description='',
        items=[
            ("BEFORE_ACTIVE", 'Move to Before Selected', ''),
            ("LAST", 'Move to Last', '')
        ],
        default='BEFORE_ACTIVE'
    )

    Scene.NTRZ_shapekey_manip_settings = PointerProperty(
        type=NTRZ_PG_manip_shapekey_settings  
    )

    Scene.NTRZ_shapekey_move_shapekey_list = CollectionProperty(
        name='Shapekey Move List',
        type=NTRZ_PG_manip_shapekey_list
    )

    Scene.NTRZ_shapekey_move_shapekey_list_index = IntProperty(
        name='Shapekey Move List Index'
    )

    Scene.NTRZ_breathing_assist = PointerProperty(
        type=NTRZ_PG_breathing_assist
    )

    Scene.NTRZ_breathing_shapekey_list = CollectionProperty(
        name='Shapekey Move List',
        type=NTRZ_PG_breathing_shapekey_list
    )

    Scene.NTRZ_breathing_shapekey_list_index = IntProperty(
        name='Shapekey Move List Index'
    )

    Scene.NTRZ_vertgroup_manip_settings = PointerProperty(
        type=NTRZ_PG_vertgroup_manip_settings  
    )

    Scene.NTRZ_vertgroup_manip_list = CollectionProperty(
        name='Shapekey Move List',
        type=NTRZ_PG_vertgroup_manip_list
    )

    Scene.NTRZ_vertgroup_manip_list_index = IntProperty(
        name='Shapekey Move List Index'
    )

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        info = 'Unregistering "%s"' % str(cls)
        print(info)
        try:
            unregister_class(cls)
        except:
            print('error')

    from bpy.types import Scene
    properties = (
            Scene.NTRZ_shapekey_name,
            Scene.NTRZ_shapekey_name_affix,
            Scene.NTRZ_shapekey_insert_location,
            # Scene.NTRZ_shapekey_move_start_index,
            # Scene.NTRZ_shapekey_move_end_index,
            Scene.NTRZ_shapekey_manip_location,
            Scene.NTRZ_shapekey_manip_settings,
            Scene.NTRZ_shapekey_move_shapekey_list,
            Scene.NTRZ_shapekey_move_shapekey_list_index,
            Scene.NTRZ_breathing_assist,
            Scene.NTRZ_breathing_shapekey_list,
            Scene.NTRZ_breathing_shapekey_list_index,

        )
    for prop in properties:
        del prop
        
if __name__ == '__main__':
    register()