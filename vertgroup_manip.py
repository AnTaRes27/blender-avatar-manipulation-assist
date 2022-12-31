"""/// ANTARES AVATAR MANIUPLATION ASSIST: VERTGROUP_MANIP /////////////////////
 ///
//    HELLO!
//
//    COPYRIGHT (C) 2022 ANTARES HUSKY (HUSKY@ANTARES.DOG)
//
////////////////////////////////////////////////////////////////////////////"""

import bpy

class NTRZ_PG_vertgroup_manip_settings(bpy.types.PropertyGroup):
    vertgroup_manip_start_index: bpy.props.IntProperty(
        name='Vertex Group Manipulation Start Index',
        default=0
    )

    vertgroup_manip_end_index: bpy.props.IntProperty(
        name='Vertex Group Manipulation End Index',
        default=0
    )

    vertgroup_manip_regex: bpy.props.StringProperty(
        name='Vertex Group Manipulation Regex Text'
    )

class NTRZ_PG_vertgroup_manip_list(bpy.types.PropertyGroup):
    #name: StringProperty() -> instantiated by default
    obj_type: bpy.props.StringProperty()
    vertgroup_index: bpy.props.IntProperty()


class NTRZ_OT_vertgroup_manip_list_bulk_add_actions(bpy.types.Operator):
    bl_idname = 'ntrz.vertgroup_manip_list_bulk_add_actions'
    bl_label = 'Vertex List Bulk Add Actions'
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
        index = scene.NTRZ_vertgroup_list_index

        match self.action:
            case 'SET_START':
                scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_start_index = bpy.context.object.active_shape_key_index
            case 'SET_END':
                scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_end_index = bpy.context.object.active_shape_key_index
            case 'BULK_ADD_INDEXES':
                for shapekey_index in range(scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_start_index, scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_end_index+1):
                    shapekey_name = context.object.data.shape_keys.key_blocks[shapekey_index].name
                    item = scene.NTRZ_vertgroup_list.add()
                    item.name = shapekey_name
                    item.obj_type = 'STRING'
                    item.vertgroup_index = shapekey_index
                    scene.NTRZ_vertgroup_list_index = len(scene.NTRZ_vertgroup_list)-1
            case 'BULK_INSERT_INDEXES':
                for shapekey_index in reversed(range(scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_start_index, scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_end_index)):
                    shapekey_name = context.object.data.shape_keys.key_blocks[shapekey_index].name
                    item = scene.NTRZ_vertgroup_list.add()
                    item.name = shapekey_name
                    item.obj_type = 'STRING'
                    item.vertgroup_index = shapekey_index
                    scene.NTRZ_vertgroup_list.move(len(scene.NTRZ_vertgroup_list)-1, scene.NTRZ_vertgroup_list_index)
                scene.NTRZ_vertgroup_list_index += scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_end_index - scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_start_index - 1
            case 'BULK_ADD_REGEX':
                import re
                text_regex = scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_regex
                match_shapekeys = []
                for x in range(1,len(bpy.context.object.data.shape_keys.key_blocks)):
                    shapekey_name = bpy.context.object.data.shape_keys.key_blocks[x].name
                    if re.search(text_regex, shapekey_name, re.IGNORECASE):
                        match_shapekeys.append(x)

                for shapekey_index in match_shapekeys:
                    item = scene.NTRZ_vertgroup_list.add()
                    item.name = context.object.data.shape_keys.key_blocks[shapekey_index].name
                    item.obj_type = 'STRING'
                    item.vertgroup_index = shapekey_index
                scene.NTRZ_vertgroup_list_index = len(scene.NTRZ_vertgroup_list)-1
            case 'BULK_INSERT_REGEX':
                import re
                text_regex = scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_regex
                match_shapekeys = []
                for x in range(1,len(bpy.context.object.data.shape_keys.key_blocks)):
                    shapekey_name = bpy.context.object.data.shape_keys.key_blocks[x].name
                    if re.search(text_regex, shapekey_name, re.IGNORECASE):
                        match_shapekeys.append(x)

                for shapekey_index in reversed(match_shapekeys):
                    item = scene.NTRZ_vertgroup_list.add()
                    item.name = context.object.data.shape_keys.key_blocks[shapekey_index].name
                    item.obj_type = 'STRING'
                    item.vertgroup_index = shapekey_index
                    scene.NTRZ_vertgroup_list.move(len(scene.NTRZ_vertgroup_list)-1, scene.NTRZ_vertgroup_list_index)
                scene.NTRZ_vertgroup_list_index += len(match_shapekeys) - 1
            case _:
                pass
        return {'FINISHED'}

class NTRZ_OT_vertgroup_manip_list_actions(bpy.types.Operator):
    bl_idname = 'ntrz.vertgroup_manip_list_actions'
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
        index = scene.NTRZ_vertgroup_list_index

        try:
            item = scene.NTRZ_vertgroup_list[index]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and index < len(scene.NTRZ_vertgroup_list)-1:
                scene.NTRZ_vertgroup_list.move(index, index+1)
                scene.NTRZ_vertgroup_list_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.NTRZ_vertgroup_list_index+1)
                self.report({'INFO'}, info)
            elif self.action == 'UP' and index >= 1:
                scene.NTRZ_vertgroup_list.move(index, index-1)
                scene.NTRZ_vertgroup_list_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.NTRZ_vertgroup_list_index+1)
                self.report({'INFO'}, info)
            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scene.NTRZ_vertgroup_list[index].name)
                scene.NTRZ_vertgroup_list.remove(index)
                if index > 0:
                    scene.NTRZ_vertgroup_list_index -= 1
                else:
                    scene.NTRZ_vertgroup_list_index = 0
                self.report({'INFO'}, info)

        if self.action == 'ADD' or self.action == 'INSERT':
            if context.object.active_shape_key_index:
                active_shapekey_index = context.object.active_shape_key_index
                active_shapekey_name = context.object.data.shape_keys.key_blocks[active_shapekey_index].name
                item = scene.NTRZ_vertgroup_list.add()
                item.name = active_shapekey_name
                item.obj_type = 'STRING'
                item.vertgroup_index = active_shapekey_index
                if self.action == 'ADD':
                    scene.NTRZ_vertgroup_list_index = len(scene.NTRZ_vertgroup_list)-1
                else:
                    scene.NTRZ_vertgroup_list.move(len(scene.NTRZ_vertgroup_list)-1, scene.NTRZ_vertgroup_list_index)
                info = '"%s" added to list' % (active_shapekey_name)
                self.report({'INFO'}, info)
        return {'FINISHED'}

class NTRZ_OT_vertgroup_manip_clear_list(bpy.types.Operator):
    bl_idname = 'ntrz.vertgroup_manip_clear_list'
    bl_label = 'Clear List'
    bl_description = ''
    bl_options = {"INTERNAL", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.NTRZ_vertgroup_list)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.NTRZ_vertgroup_list):
            context.scene.NTRZ_vertgroup_list.clear()
            self.report({'INFO'}, 'List cleared')
        else:
            self.report({'INFO'}, 'Nothing to clear')
        return{'FINISHED'}

class NTRZ_OT_vertgroup_manip_list_remove_duplicates(bpy.types.Operator):
    bl_idname = 'ntrz.vertgroup_manip_list_remove_duplicates'
    bl_label = 'Remove Duplicates'
    bl_description = ''
    bl_options = {"INTERNAL", "UNDO"}

    def find_duplicates(self, context):
        name_lookup = {}
        for c, i in enumerate(context.scene.NTRZ_vertgroup_list):
            name_lookup.setdefault(i.name, []).append(c)
        duplicates = set()
        for name, indexes in name_lookup.items():
            for i in indexes[1:]:
                duplicates.add(i)
        return sorted(list(duplicates))

    @classmethod
    def poll(cls, context):
        return bool(context.scene.NTRZ_vertgroup_list)

    def execute(self, context):
        scene = context.scene
        for i in reversed(self.find_duplicates(context)):
            scene.NTRZ_vertgroup_list.remove(i)
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
