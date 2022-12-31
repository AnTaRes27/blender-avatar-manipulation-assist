"""/// ANTARES AVATAR MANIUPLATION ASSIST v0.1.0 //////////////////////////////
 ///
//    HELLO!
//
//    COPYRIGHT (C) 2022 ANTARES HUSKY (HUSKY@ANTARES.DOG)
//
////////////////////////////////////////////////////////////////////////////"""

import bpy

#////////////////////////////////////////////////#

class TestPanel(bpy.types.Panel):
    bl_idname = 'PT_TestPanel'
    bl_label = 'TestPanel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NTRZ'
        
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text='TestText', icon='CUBE')
        
        
        row = layout.row()
        row.operator('ntrz.unload')


#////////////////////////////////////////////////#

class NTRZ_PT_shapekey_insert(bpy.types.Panel):
    """displays functions related to inserting shapekey
    attr:
            [TODO insert attributes]
    """
    bl_idname = 'NTRZ_PT_shapekey_insert'
    bl_label = 'Insert Shapekey'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NTRZ'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, 'NTRZ_shapekey_name')

        row = layout.row()
        split = row.split()
        split.ui_units_x = 2.25
        split.prop(scene, 'NTRZ_shapekey_name_affix', text='')
        row.label(text=str(scene.NTRZ_shapekey_name))
        
        row = layout.row()
        row.prop(scene, 'NTRZ_shapekey_insert_location', expand=True)
        
        row = layout.row()
        row.operator('ntrz.add_shapekey')

        row = layout.row()
        row.operator('NTRZ_OT_rename_shapekey')

        row = layout.row()
        row.operator('ntrz.add_shapekey_spacer')

#////////////////////////////////////////////////#
#////////////////////////////////////////////////#

class NTRZ_PT_shapekey_manip(bpy.types.Panel):
    """displays functions related to manipulating shapekey
    attr:
            [TODO insert attributes]
    """
    bl_idname = 'NTRZ_PT_shapekey_manip'
    bl_label = 'Move Shapekey'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NTRZ'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column()
        row = col.row()
        split = row.split(factor=0.2)
        col = split.column()
        col.label(text='By Index')
        split = split.split()
        row = split.row(align=True)
        # row.alignment = 'RIGHT'
        row.label(text='from: ')
        row.operator('ntrz.manip_shapekey_list_bulk_add_actions', icon='TRACKING_BACKWARDS_SINGLE', text='').action = 'SET_START'
        row.label(text=str(scene.NTRZ_shapekey_manip_settings.shapekey_manip_start_index))
        row.separator()
        row.label(text='to: ')
        row.operator('ntrz.manip_shapekey_list_bulk_add_actions', icon='TRACKING_FORWARDS_SINGLE', text='').action = 'SET_END'
        row.label(text=str(scene.NTRZ_shapekey_manip_settings.shapekey_manip_end_index))
        row.separator()
        row.operator('ntrz.manip_shapekey_list_bulk_add_actions', icon='ADD', text='').action = 'BULK_ADD_INDEXES'
        row.operator('ntrz.manip_shapekey_list_bulk_add_actions', icon='BACK', text='').action = 'BULK_INSERT_INDEXES'

        col = layout.column()
        row = col.row()
        split = row.split(factor=0.2)
        col = split.column()
        col.label(text='By PyRegEx')
        split = split.split()
        row = split.row(align=True)
        # row = layout.row(align=True)
        row.prop(scene.NTRZ_shapekey_manip_settings, 'shapekey_manip_regex', text='')
        row.operator('ntrz.manip_shapekey_list_bulk_add_actions', icon='ADD', text='').action = 'BULK_ADD_REGEX'
        row.operator('ntrz.manip_shapekey_list_bulk_add_actions', icon='BACK', text='').action = 'BULK_INSERT_REGEX'

        rows=2
        row = layout.row()
        row.template_list('NTRZ_UL_shapekey_list', '', scene, 'NTRZ_shapekey_move_shapekey_list', scene, 'NTRZ_shapekey_move_shapekey_list_index', rows=rows)

        col = row.column(align=True)
        col.operator('ntrz.manip_shapekey_list_actions', icon='ADD', text='').action = 'ADD'
        col.operator('ntrz.manip_shapekey_list_actions', icon='BACK', text='').action = 'INSERT'
        col.operator('ntrz.manip_shapekey_list_actions', icon='REMOVE', text='').action = 'REMOVE'
        col.separator()
        col.operator('ntrz.manip_shapekey_list_actions', icon='TRIA_UP', text='').action = 'UP'
        col.operator('ntrz.manip_shapekey_list_actions', icon='TRIA_DOWN', text='').action = 'DOWN'
        col.separator()
        col.operator('ntrz.manip_shapeky_clear_list', icon='PANEL_CLOSE', text='')

        row = layout.row()
        row.operator('ntrz.manip_shapekey_list_remove_duplicates', icon="FORCE_VORTEX")

        row = layout.row()
        row.prop(scene, 'NTRZ_shapekey_manip_location', expand=True)

        row = layout.row()
        row.operator('ntrz.manip_shapekey_actions', text='Move These Shapekeys').action = 'MOVE'
        # row.operator('')

class NTRZ_UL_shapekey_list(bpy.types.UIList):
    """displays UI List of shapekeys to manipulate
    attr:
            [TODO insert attributes]
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
        #   split = layout.split(factor=0.3)
        #   split.label(text="Index: %d" % (index))
        #   split.label(text=item.name) #avoid renaming item by accident
        # elif self.layout_type in {'GRID'}:
        #   layout.alignment = 'CENTER'
        #   layout.label(text='')
        split = layout.split(factor=0.2)
        # split.prop(item, 'obj_id', text='', emboss=False, icon_value=icon)
        # split.prop(item, 'name', text='', emboss=False, icon_value=icon)
        split.label(text=str(item.obj_id))
        split.label(text=item.name)
        # split.enabled = False
        # layout.prop(item, 'name', text='', emboss=False, icon_value=icon)

    def invoke(self, context, event):
        pass

#////////////////////////////////////////////////#
#////////////////////////////////////////////////#

class NTRZ_PT_breathing_assist(bpy.types.Panel):
    """displays functions related to create breathing shapekeys
    attr:
            [TODO insert attributes]
    """
    bl_idname = 'NTRZ_PT_breathing_assist'
    bl_label = 'Breathing Shapekeys Generator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NTRZ'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene.NTRZ_breathing_assist, "src_mesh", text="Body Mesh") 
        layout.prop(scene.NTRZ_breathing_assist, "dest_mesh", text="Aux Mesh")

        rows=2
        row = layout.row()
        row.template_list('NTRZ_UL_breathing_shapekey_list', '', scene, 'NTRZ_breathing_shapekey_list', scene, 'NTRZ_breathing_shapekey_list_index', rows=rows)

        col = row.column(align=True)
        col.operator('ntrz.breathing_shapekey_list_actions', icon='ADD', text='').action = 'ADD'
        col.operator('ntrz.breathing_shapekey_list_actions', icon='BACK', text='').action = 'INSERT'
        col.operator('ntrz.breathing_shapekey_list_actions', icon='REMOVE', text='').action = 'REMOVE'
        col.separator()
        col.operator('ntrz.breathing_shapekey_list_actions', icon='TRIA_UP', text='').action = 'UP'
        col.operator('ntrz.breathing_shapekey_list_actions', icon='TRIA_DOWN', text='').action = 'DOWN'
        col.separator()
        col.operator('ntrz.breathing_shapeky_clear_list', icon='PANEL_CLOSE', text='')

        row = layout.row()
        row.operator('ntrz.breathing_shapekey_transfer')

class NTRZ_UL_breathing_shapekey_list(bpy.types.UIList):
    """displays UI List of shapekeys to manipulate
    attr:
            [TODO insert attributes]
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
        #   split = layout.split(factor=0.3)
        #   split.label(text="Index: %d" % (index))
        #   split.label(text=item.name) #avoid renaming item by accident
        # elif self.layout_type in {'GRID'}:
        #   layout.alignment = 'CENTER'
        #   layout.label(text='')
        split = layout.split(factor=0.2)
        # split.prop(item, 'obj_id', text='', emboss=False, icon_value=icon)
        # split.prop(item, 'name', text='', emboss=False, icon_value=icon)
        split.label(text=str(item.obj_id))
        split.label(text=item.name)
        # split.enabled = False
        # layout.prop(item, 'name', text='', emboss=False, icon_value=icon)

    def invoke(self, context, event):
        pass

#////////////////////////////////////////////////#
#////////////////////////////////////////////////#

class NTRZ_PT_vertgroup_manip(bpy.types.Panel):
    """displays functions related to manipulating vertex groups
    attr:
            [TODO insert attributes]
    """
    bl_idname = 'NTRZ_PT_vertgroup_manip'
    bl_label = 'Vertex Weight Manipulator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NTRZ'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column()
        row = col.row()
        split = row.split(factor=0.2)
        col = split.column()
        col.label(text='By Index')
        split = split.split()
        row = split.row(align=True)
        # row.alignment = 'RIGHT'
        row.label(text='from: ')
        row.operator('ntrz.vertgroup_manip_list_bulk_add_actions', icon='TRACKING_BACKWARDS_SINGLE', text='').action = 'SET_START'
        row.label(text=str(scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_start_index))
        row.separator()
        row.label(text='to: ')
        row.operator('ntrz.vertgroup_manip_list_bulk_add_actions', icon='TRACKING_FORWARDS_SINGLE', text='').action = 'SET_END'
        row.label(text=str(scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_end_index))
        row.separator()
        row.operator('ntrz.vertgroup_manip_list_bulk_add_actions', icon='ADD', text='').action = 'BULK_ADD_INDEXES'
        row.operator('ntrz.vertgroup_manip_list_bulk_add_actions', icon='BACK', text='').action = 'BULK_INSERT_INDEXES'

        col = layout.column()
        row = col.row()
        split = row.split(factor=0.2)
        col = split.column()
        col.label(text='By PyRegEx')
        split = split.split()
        row = split.row(align=True)
        # row = layout.row(align=True)
        row.prop(scene.NTRZ_vertgroup_manip_settings, 'vertgroup_manip_regex', text='')
        row.operator('ntrz.vertgroup_manip_list_bulk_add_actions', icon='ADD', text='').action = 'BULK_ADD_REGEX'
        row.operator('ntrz.vertgroup_manip_list_bulk_add_actions', icon='BACK', text='').action = 'BULK_INSERT_REGEX'

        rows=2
        row = layout.row()
        row.template_list('NTRZ_UL_vertgroup_list', '', scene, 'NTRZ_vertgroup_manip_list', scene, 'NTRZ_vertgroup_manip_list_index', rows=rows)

        col = row.column(align=True)
        col.operator('ntrz.vertgroup_manip_list_actions', icon='ADD', text='').action = 'ADD'
        col.operator('ntrz.vertgroup_manip_list_actions', icon='BACK', text='').action = 'INSERT'
        col.operator('ntrz.vertgroup_manip_list_actions', icon='REMOVE', text='').action = 'REMOVE'
        col.separator()
        col.operator('ntrz.vertgroup_manip_list_actions', icon='TRIA_UP', text='').action = 'UP'
        col.operator('ntrz.vertgroup_manip_list_actions', icon='TRIA_DOWN', text='').action = 'DOWN'
        col.separator()
        col.operator('ntrz.vertgroup_manip_clear_list', icon='PANEL_CLOSE', text='')

        row = layout.row()
        row.operator('ntrz.vertgroup_manip_list_remove_duplicates', icon="FORCE_VORTEX")

class NTRZ_UL_vertgroup_list(bpy.types.UIList):
    """displays UI List of vertex group to manipulate
    attr:
            [TODO insert attributes]
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
        #   split = layout.split(factor=0.3)
        #   split.label(text="Index: %d" % (index))
        #   split.label(text=item.name) #avoid renaming item by accident
        # elif self.layout_type in {'GRID'}:
        #   layout.alignment = 'CENTER'
        #   layout.label(text='')
        split = layout.split(factor=0.2)
        # split.prop(item, 'obj_id', text='', emboss=False, icon_value=icon)
        # split.prop(item, 'name', text='', emboss=False, icon_value=icon)
        split.label(text=str(item.index))
        split.label(text=item.name)
        # split.enabled = False
        # layout.prop(item, 'name', text='', emboss=False, icon_value=icon)

    def invoke(self, context, event):
        pass


#////////////////////////////////////////////////#
#////////////////////////////////////////////////#

class NTRZ_PT_housekeeping(bpy.types.Panel):
    """displays functions related to housekeeping
    attr:
            [TODO insert attributes]
    """
    bl_idname = 'NTRZ_PT_housekeeping'
    bl_label = 'Housekeeping'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NTRZ'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.operator('ntrz.housekeeping_actions').action = 'RENAME_MESH_TO_OBJECT'

#////////////////////////////////////////////////#