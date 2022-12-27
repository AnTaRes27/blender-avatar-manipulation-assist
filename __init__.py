"""/// ANTARES AVATAR MANIUPLATION ASSIST v0.0.0 //////////////////////////////
////
//    HELLO!
//
//    COPYRIGHT (C) 2022 ANTARES HUSKY (HUSKY@ANTARES.DOG)
//
////////////////////////////////////////////////////////////////////////////"""

bl_info = {
    'name' : 'Antares Avatar Manipulation Assist',
    'author' : 'Antares Husky',
    'version' : (0, 0, 0),
    'blender' : (3, 3, 1),
    'location': 'View3D > NTRZ',
    'warning': 'I may or may not know what I\'m doing',
    'wiki_url': 'http:\\\\antares.dog',
    'category': 'IDK'
}

import bpy

#////////////////////////////////////////////////#
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



class NTRZ_OT_add_shapekey(bpy.types.Operator):
    """OPERATOR: inserts spacekey into shapekey list
    """
    bl_idname = 'ntrz.add_shapekey'
    bl_label = 'Add Shapekey'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        prefix = ''
        suffix = ''
        match context.scene.NTRZ_shapekey_name_affix:
            case 'BLANK':
                pass
            case 'HDG1':
                prefix = '╠══ '
                suffix = ' ══╣'
            case 'HDG2':
                prefix = '╠═ '
            case _:
                pass

        shapekey_name = prefix + str(context.scene.NTRZ_shapekey_name) + suffix
        shapekey_index = bpy.context.object.active_shape_key_index
        bpy.ops.object.shape_key_add(from_mix=False)
        bpy.context.object.data.shape_keys.key_blocks[bpy.context.object.active_shape_key_index].name = shapekey_name
        if context.scene.NTRZ_shapekey_insert_location == 'BEFORE_ACTIVE':
            for x in range(0,len(bpy.context.object.data.shape_keys.key_blocks) - shapekey_index - 1):
                bpy.ops.object.shape_key_move(type='UP')
        
        return{"FINISHED"}

class NTRZ_OT_add_shapekey_spacer(bpy.types.Operator):
    bl_idname = 'ntrz.add_shapekey_spacer'
    bl_label = 'Add Spacer'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        import re
        text_regex = r'^\s*$'
        text_space = ' '
        spacer_shapekey_lens = [1]
        for shapekey in context.object.data.shape_keys.key_blocks:
            if re.search(text_regex, shapekey.name, re.IGNORECASE):
                spacer_shapekey_lens.append(len(shapekey.name))
        for x in range(max(spacer_shapekey_lens)):
            text_space += ' '

        blendshape_index = context.object.active_shape_key_index
        bpy.ops.object.shape_key_add(from_mix=False)
        context.object.data.shape_keys.key_blocks[context.object.active_shape_key_index].name = text_space
        if context.scene.NTRZ_shapekey_insert_location == 'BEFORE_ACTIVE':
            for x in range(0,len(bpy.context.object.data.shape_keys.key_blocks) - blendshape_index - 1):
                bpy.ops.object.shape_key_move(type='UP')
        return{"FINISHED"}

class NTRZ_OT_rename_shapekey(bpy.types.Operator):
    bl_idname = 'ntrz.rename_shapekey'
    bl_label = 'Rename Shapekey'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        prefix = ''
        suffix = ''
        match context.scene.NTRZ_shapekey_name_affix:
            case 'BLANK':
                pass
            case 'HDG1':
                prefix = '╠══ '
                suffix = ' ══╣'
            case 'HDG2':
                prefix = '╠═ '
            case _:
                pass

        shapekey_name = prefix + str(context.scene.NTRZ_shapekey_name) + suffix
        shapekey_index = bpy.context.object.active_shape_key_index
        bpy.context.object.data.shape_keys.key_blocks[bpy.context.object.active_shape_key_index].name = shapekey_name

        return{'FINISHED'}

class NTRZ_OT_manip_shapekey_list_bulk_add_actions(bpy.types.Operator):
    bl_idname = 'ntrz.manip_shapekey_list_bulk_add_actions'
    bl_label = 'Shapekey List Bulk Add Actions'
    bl_description = ''
    bl_options = {"REGISTER", "UNDO"}

    action: bpy.props.EnumProperty(
        items=(
            ('SET_START', 'Set Start Index', ''),
            ('SET_END', 'Set End Index', ''),
            ('BULK_ADD_INDEXES', 'Bulk Add Indexes', ''),
            ('BULK_INSERT_INDEXES', 'Bulk Insert Indexes', ''),
            ('BULK_ADD_REGEX', 'Bulk Add Regex', ''),
            ('BULK_INSERT_REGEX', 'Bulk Add Regex', ''),
        )
    )

    def invoke(self, context, event):
        scene = context.scene
        index = scene.NTRZ_shapekey_move_shapekey_list_index

        match self.action:
            case 'SET_START':
                scene.NTRZ_shapekey_manip_settings.shapekey_manip_start_index = bpy.context.object.active_shape_key_index
            case 'SET_END':
                scene.NTRZ_shapekey_manip_settings.shapekey_manip_end_index = bpy.context.object.active_shape_key_index
            case 'BULK_ADD_INDEXES':
                for shapekey_index in range(scene.NTRZ_shapekey_manip_settings.shapekey_manip_start_index, scene.NTRZ_shapekey_manip_settings.shapekey_manip_end_index+1):
                    shapekey_name = context.object.data.shape_keys.key_blocks[shapekey_index].name
                    item = scene.NTRZ_shapekey_move_shapekey_list.add()
                    item.name = shapekey_name
                    item.obj_type = 'STRING'
                    item.obj_id = shapekey_index
                    scene.NTRZ_shapekey_move_shapekey_list_index = len(scene.NTRZ_shapekey_move_shapekey_list)-1
            case 'BULK_INSERT_INDEXES':
                for shapekey_index in reversed(range(scene.NTRZ_shapekey_manip_settings.shapekey_manip_start_index, scene.NTRZ_shapekey_manip_settings.shapekey_manip_end_index)):
                    shapekey_name = context.object.data.shape_keys.key_blocks[shapekey_index].name
                    item = scene.NTRZ_shapekey_move_shapekey_list.add()
                    item.name = shapekey_name
                    item.obj_type = 'STRING'
                    item.obj_id = shapekey_index
                    scene.NTRZ_shapekey_move_shapekey_list.move(len(scene.NTRZ_shapekey_move_shapekey_list)-1, scene.NTRZ_shapekey_move_shapekey_list_index)
                scene.NTRZ_shapekey_move_shapekey_list_index += scene.NTRZ_shapekey_manip_settings.shapekey_manip_end_index - scene.NTRZ_shapekey_manip_settings.shapekey_manip_start_index - 1
            case 'BULK_ADD_REGEX':
                import re
                text_regex = scene.NTRZ_shapekey_manip_settings.shapekey_manip_regex
                match_shapekeys = []
                for x in range(1,len(bpy.context.object.data.shape_keys.key_blocks)):
                    shapekey_name = bpy.context.object.data.shape_keys.key_blocks[x].name
                    if re.search(text_regex, shapekey_name, re.IGNORECASE):
                        match_shapekeys.append(x)

                for shapekey_index in match_shapekeys:
                    item = scene.NTRZ_shapekey_move_shapekey_list.add()
                    item.name = context.object.data.shape_keys.key_blocks[shapekey_index].name
                    item.obj_type = 'STRING'
                    item.obj_id = shapekey_index
                scene.NTRZ_shapekey_move_shapekey_list_index = len(scene.NTRZ_shapekey_move_shapekey_list)-1
            case 'BULK_INSERT_REGEX':
                import re
                text_regex = scene.NTRZ_shapekey_manip_settings.shapekey_manip_regex
                match_shapekeys = []
                for x in range(1,len(bpy.context.object.data.shape_keys.key_blocks)):
                    shapekey_name = bpy.context.object.data.shape_keys.key_blocks[x].name
                    if re.search(text_regex, shapekey_name, re.IGNORECASE):
                        match_shapekeys.append(x)

                for shapekey_index in reversed(match_shapekeys):
                    item = scene.NTRZ_shapekey_move_shapekey_list.add()
                    item.name = context.object.data.shape_keys.key_blocks[shapekey_index].name
                    item.obj_type = 'STRING'
                    item.obj_id = shapekey_index
                    scene.NTRZ_shapekey_move_shapekey_list.move(len(scene.NTRZ_shapekey_move_shapekey_list)-1, scene.NTRZ_shapekey_move_shapekey_list_index)
                scene.NTRZ_shapekey_move_shapekey_list_index += len(match_shapekeys) - 1
            case _:
                pass
        return {'FINISHED'}

class NTRZ_OT_manip_shapekey_list_actions(bpy.types.Operator):
    bl_idname = 'ntrz.manip_shapekey_list_actions'
    bl_label = 'Shapekey List Actions'
    bl_description = ''
    bl_options = {"REGISTER", "UNDO"}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', 'Up', ''),
            ('DOWN', 'Down', ''),
            ('REMOVE', 'Remove', ''),
            ('ADD', 'Add', ''),
            ('INSERT', 'Insert', '')
        )
    )

    def invoke(self, context, event):
        scene = context.scene
        index = scene.NTRZ_shapekey_move_shapekey_list_index

        try:
            item = scene.NTRZ_shapekey_move_shapekey_list[index]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and index < len(scene.NTRZ_shapekey_move_shapekey_list)-1:
                scene.NTRZ_shapekey_move_shapekey_list.move(index, index+1)
                scene.NTRZ_shapekey_move_shapekey_list_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.NTRZ_shapekey_move_shapekey_list_index+1)
                self.report({'INFO'}, info)
            elif self.action == 'UP' and index >= 1:
                scene.NTRZ_shapekey_move_shapekey_list.move(index, index-1)
                scene.NTRZ_shapekey_move_shapekey_list_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.NTRZ_shapekey_move_shapekey_list_index+1)
                self.report({'INFO'}, info)
            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scene.NTRZ_shapekey_move_shapekey_list[index].name)
                scene.NTRZ_shapekey_move_shapekey_list.remove(index)
                if index > 0:
                    scene.NTRZ_shapekey_move_shapekey_list_index -= 1
                else:
                    scene.NTRZ_shapekey_move_shapekey_list_index = 0
                self.report({'INFO'}, info)

        if self.action == 'ADD' or self.action == 'INSERT':
            if context.object.active_shape_key_index:
                active_shapekey_index = context.object.active_shape_key_index
                active_shapekey_name = context.object.data.shape_keys.key_blocks[active_shapekey_index].name
                item = scene.NTRZ_shapekey_move_shapekey_list.add()
                item.name = active_shapekey_name
                item.obj_type = 'STRING'
                item.obj_id = active_shapekey_index
                if self.action == 'ADD':
                    scene.NTRZ_shapekey_move_shapekey_list_index = len(scene.NTRZ_shapekey_move_shapekey_list)-1
                else:
                    scene.NTRZ_shapekey_move_shapekey_list.move(len(scene.NTRZ_shapekey_move_shapekey_list)-1, scene.NTRZ_shapekey_move_shapekey_list_index)
                info = '"%s" added to list' % (active_shapekey_name)
                self.report({'INFO'}, info)
        return {'FINISHED'}

class NTRZ_OT_manip_shapekey_clear_list(bpy.types.Operator):
    bl_idname = 'ntrz.manip_shapeky_clear_list'
    bl_label = 'Clear List'
    bl_description = ''
    bl_options = {"INTERNAL", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.NTRZ_shapekey_move_shapekey_list)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.NTRZ_shapekey_move_shapekey_list):
            context.scene.NTRZ_shapekey_move_shapekey_list.clear()
            self.report({'INFO'}, 'List cleared')
        else:
            self.report({'INFO'}, 'Nothing to clear')
        return{'FINISHED'}

class NTRZ_OT_manip_shapekey_list_remove_duplicates(bpy.types.Operator):
    bl_idname = 'ntrz.manip_shapekey_list_remove_duplicates'
    bl_label = 'Remove Duplicates'
    bl_description = ''
    bl_options = {"INTERNAL", "UNDO"}

    def find_duplicates(self, context):
        name_lookup = {}
        for c, i in enumerate(context.scene.NTRZ_shapekey_move_shapekey_list):
            name_lookup.setdefault(i.name, []).append(c)
        duplicates = set()
        for name, indexes in name_lookup.items():
            for i in indexes[1:]:
                duplicates.add(i)
        return sorted(list(duplicates))

    @classmethod
    def poll(cls, context):
        return bool(context.scene.NTRZ_shapekey_move_shapekey_list)

    def execute(self, context):
        scene = context.scene
        for i in reversed(self.find_duplicates(context)):
            scene.NTRZ_shapekey_move_shapekey_list.remove(i)
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

class NTRZ_OT_manip_shapekey_actions(bpy.types.Operator):
    bl_idname = 'ntrz.manip_shapekey_actions'
    bl_label = 'Manipulate Shapekeys'
    bl_description = ''
    bl_options = {"REGISTER", "UNDO"}

    action: bpy.props.EnumProperty(
        items=(
            ('MOVE', 'Move Shapekeys Block Before Active', ''),
            # ('MOVE_TO_END', 'Move Shapekeys Block to the End', ''),
        )
    )

    def invoke(self, context, event):
        scene = context.scene

        try:
            item = scene.NTRZ_shapekey_move_shapekey_list[0]
        except IndexError:
            pass
        else:
            match self.action:
                case 'MOVE':
                    shapekey_move_target_index = context.object.active_shape_key_index
                    shapekeys_before_indexes = []
                    shapekeys_after_indexes = []

                    #remove duplicates first
                    name_lookup = {}
                    for c, i in enumerate(context.scene.NTRZ_shapekey_move_shapekey_list):
                        name_lookup.setdefault(i.name, []).append(c)
                    duplicates = set()
                    for name, indexes in name_lookup.items():
                        for i in indexes[1:]:
                            duplicates.add(i)
                    for i in reversed(sorted(list(duplicates))):
                        scene.NTRZ_shapekey_move_shapekey_list.remove(i)

                    #separate
                    for x in range(len(context.scene.NTRZ_shapekey_move_shapekey_list)):
                        shapekey_index = context.scene.NTRZ_shapekey_move_shapekey_list[x].obj_id
                        if shapekey_index < shapekey_move_target_index:
                            shapekeys_before_indexes.append(shapekey_index)
                        else:
                            shapekeys_after_indexes.append(shapekey_index)

                    if context.scene.NTRZ_shapekey_manip_location == 'BEFORE_ACTIVE':
                        #move ones before
                        offset = 1 #want to put it before active index
                        for shapekey_index in reversed(sorted(shapekeys_before_indexes)):
                            bpy.context.object.active_shape_key_index = shapekey_index
                            # print('moving ' + context.object.data.shape_keys.key_blocks[shapekey_index].name)
                            for x in range(shapekey_move_target_index-shapekey_index-offset):
                                bpy.ops.object.shape_key_move(type='DOWN')
                            offset += 1

                        #move ones after
                        offset = 0
                        for shapekey_index in sorted(shapekeys_after_indexes):
                            bpy.context.object.active_shape_key_index = shapekey_index
                            for x in range(shapekey_index-shapekey_move_target_index-offset):
                                bpy.ops.object.shape_key_move(type='UP')
                            offset += 1
                    else:
                        #move in one go
                        shapekey_move_target_index = len(context.object.data.shape_keys.key_blocks)
                        offset = 1
                        for shapekey_index in reversed(sorted(shapekeys_before_indexes+shapekeys_after_indexes)):
                            bpy.context.object.active_shape_key_index = shapekey_index
                            print('moving ' + context.object.data.shape_keys.key_blocks[shapekey_index].name)
                            for x in range(shapekey_move_target_index-shapekey_index-offset):
                                bpy.ops.object.shape_key_move(type='DOWN')
                            offset += 1

                # case 'MOVE_TO_END':
                #   pass
                case _:
                    pass
        return{'FINISHED'}

class NTRZ_OT_breathing_shapekey_list_actions(bpy.types.Operator):
    bl_idname = 'ntrz.breathing_shapekey_list_actions'
    bl_label = 'Shapekey List Actions'
    bl_description = ''
    bl_options = {"REGISTER", "UNDO"}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', 'Up', ''),
            ('DOWN', 'Down', ''),
            ('REMOVE', 'Remove', ''),
            ('ADD', 'Add', ''),
            ('INSERT', 'Insert', '')
        )
    )

    def invoke(self, context, event):
        scene = context.scene
        index = scene.NTRZ_breathing_shapekey_list_index

        try:
            item = scene.NTRZ_breathing_shapekey_list[index]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and index < len(scene.NTRZ_breathing_shapekey_list)-1:
                scene.NTRZ_breathing_shapekey_list.move(index, index+1)
                scene.NTRZ_breathing_shapekey_list_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.NTRZ_breathing_shapekey_list_index+1)
                self.report({'INFO'}, info)
            elif self.action == 'UP' and index >= 1:
                scene.NTRZ_breathing_shapekey_list.move(index, index-1)
                scene.NTRZ_breathing_shapekey_list_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.NTRZ_breathing_shapekey_list_index+1)
                self.report({'INFO'}, info)
            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scene.NTRZ_breathing_shapekey_list[index].name)
                scene.NTRZ_breathing_shapekey_list.remove(index)
                if index > 0:
                    scene.NTRZ_breathing_shapekey_list_index -= 1
                else:
                    scene.NTRZ_breathing_shapekey_list_index = 0
                self.report({'INFO'}, info)

        if self.action == 'ADD' or self.action == 'INSERT':
            if context.object.active_shape_key_index:
                active_shapekey_index = context.object.active_shape_key_index
                active_shapekey_name = context.object.data.shape_keys.key_blocks[active_shapekey_index].name
                item = scene.NTRZ_breathing_shapekey_list.add()
                item.name = active_shapekey_name
                item.obj_type = 'STRING'
                item.obj_id = active_shapekey_index
                if self.action == 'ADD':
                    scene.NTRZ_breathing_shapekey_list_index = len(scene.NTRZ_breathing_shapekey_list)-1
                else:
                    scene.NTRZ_breathing_shapekey_list.move(len(scene.NTRZ_breathing_shapekey_list)-1, scene.NTRZ_breathing_shapekey_list_index)
                info = '"%s" added to list' % (active_shapekey_name)
                self.report({'INFO'}, info)
        return {'FINISHED'}

class NTRZ_OT_breathing_shapekey_clear_list(bpy.types.Operator):
    bl_idname = 'ntrz.breathing_shapeky_clear_list'
    bl_label = 'Clear List'
    bl_description = ''
    bl_options = {"INTERNAL", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.NTRZ_breathing_shapekey_list)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.NTRZ_breathing_shapekey_list):
            context.scene.NTRZ_breathing_shapekey_list.clear()
            self.report({'INFO'}, 'List cleared')
        else:
            self.report({'INFO'}, 'Nothing to clear')
        return{'FINISHED'}

class NTRZ_OT_breathing_shapekey_transfer(bpy.types.Operator):
    bl_idname = 'ntrz.breathing_shapekey_transfer'
    bl_label = 'Transfer breathing shapekeys'
    bl_description = ''
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.NTRZ_breathing_shapekey_list)

    def execute(self, context):
        scene = context.scene

        #get source object
        src_mesh = scene.NTRZ_breathing_assist.src_mesh
        src_obj_name = ''
        for o in bpy.context.scene.objects:
            if o.type == 'MESH' and o.data.name == src_mesh.name:
                src_obj_name = o.name
        src_obj = bpy.context.scene.objects[src_obj_name]

        #get destination object
        dest_mesh = scene.NTRZ_breathing_assist.dest_mesh
        dest_obj_name = ''
        for o in bpy.context.scene.objects:
            if o.type == 'MESH' and o.data.name == dest_mesh.name:
                dest_obj_name = o.name
        dest_obj = bpy.context.scene.objects[dest_obj_name]

        #create duplicate of source object to make sure it's manifold
        new_obj = src_obj.copy()
        new_obj.data = src_obj.data.copy()
        new_obj.animation_data_clear()
        bpy.context.collection.objects.link(new_obj)

        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = new_obj

        tolerance = 1e-5

        breathing_shapekey_indexes = []
        for x in range(len(context.scene.NTRZ_breathing_shapekey_list)):
            shapekey_index = context.scene.NTRZ_breathing_shapekey_list[x].obj_id
            breathing_shapekey_indexes.append(shapekey_index)

        shapekeys = bpy.context.active_object.data.shape_keys.key_blocks
        shapekey_basis_data = shapekeys[0].data

        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.object.mode_set(mode="OBJECT")

        for shapekey_index in breathing_shapekey_indexes:
            shapekey_data = shapekeys[shapekey_index].data
            for i, (x, y) in enumerate(zip(shapekey_data, shapekey_basis_data)):
                if (x.co - y.co).length > tolerance:
                    bpy.context.active_object.data.vertices[i].select = True


        bpy.ops.object.mode_set(mode="EDIT")

        bpy.ops.mesh.select_linked(delimit={'NORMAL'})
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.delete(type='VERT')

        #fix non manifold
        try:
            bpy.ops.mesh.select_non_manifold()
            bpy.ops.mesh.fill()
        except RuntimeError:
            print('mesh is manifold')

        bpy.ops.object.mode_set(mode="OBJECT")

        new_mod_triangulate = new_obj.modifiers.new('BreathingAssistTriangulate', 'TRIANGULATE')
        # src_mod_remesh = src_obj.modifiers.new('BreathingAssistRemesh', 'REMESH')
        # src_mod_remesh.voxel_size = src_obj.dimensions.x * src_obj.dimensions.y * src_obj.dimensions.z / 1000

        dest_mod = dest_obj.modifiers.new('BreathingAssistSurfaceDeform', 'SURFACE_DEFORM')
        dest_mod.target = new_obj
        bpy.context.view_layer.objects.active = dest_obj
        bpy.ops.object.surfacedeform_bind(modifier=dest_mod.name)


        if not dest_mesh.shape_keys:
            bpy.ops.object.shape_key_add(from_mix=False)
        for shapekey_index in breathing_shapekey_indexes:
            new_obj.show_only_shape_key = True
            new_obj.active_shape_key_index = shapekey_index
            bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier=dest_mod.name)
            dest_mesh.shape_keys.key_blocks[len(dest_mesh.shape_keys.key_blocks)-1].name = src_mesh.shape_keys.key_blocks[shapekey_index].name

        dest_obj.modifiers.remove(dest_mod)
        bpy.data.objects.remove(new_obj, do_unlink=True)
        

        return{"FINISHED"}

class NTRZ_OT_unload(bpy.types.Operator):
    bl_idname = 'ntrz.unload'
    bl_label = 'Unload NTRZ'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        unregister()
        return{"FINISHED"}

class NTRZ_PG_manip_shapekey_settings(bpy.types.PropertyGroup):
    shapekey_manip_start_index: bpy.props.IntProperty(
        name='Shapekey Manipulation Start Index',
        default=0
    )

    shapekey_manip_end_index: bpy.props.IntProperty(
        name='Shapekey Manipulation End Index',
        default=0
    )

    shapekey_manip_regex: bpy.props.StringProperty(
        name='Shapekey Manipulation Regex Text'
    )

class NTRZ_PG_manip_shapekey_list(bpy.types.PropertyGroup):
    #name: StringProperty() -> instantiated by default
    obj_type: bpy.props.StringProperty()
    obj_id: bpy.props.IntProperty()

class NTRZ_PG_breathing_assist(bpy.types.PropertyGroup):
    """PROPERTYGROUP: properties needed to generate breathing shapekeys
    """
    src_mesh: bpy.props.PointerProperty(
        type=bpy.types.Mesh, 
        name='Source Mesh', 
        description='Source Mesh', 
        options={'ANIMATABLE'}, 
        update=None
        )
    
    dest_mesh: bpy.props.PointerProperty(
        type=bpy.types.Mesh, 
        name='Destination Mesh', 
        description='Select a destination mesh', 
        options={'ANIMATABLE'}, 
        update=None
        )

class NTRZ_PG_breathing_shapekey_list(bpy.types.PropertyGroup):
    #name: StringProperty() -> instantiated by default
    obj_type: bpy.props.StringProperty()
    obj_id: bpy.props.IntProperty()

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
    )

def register():
    from bpy.utils import register_class
    for cls in classes:
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