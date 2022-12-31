"""/// ANTARES AVATAR MANIUPLATION ASSIST: VERTGROUP_MANIP /////////////////////
 ///
//    HELLO!
//
//    COPYRIGHT (C) 2022 ANTARES HUSKY (HUSKY@ANTARES.DOG)
//
////////////////////////////////////////////////////////////////////////////"""

import bpy

class NTRZ_PG_vertgroup_manip_settings(bpy.types.PropertyGroup):
    """ PROPERTYGROUP: contains settings for vertgroup manipulation
    attr:
        > properties
            -vertgroup_manip_start_index: start index on the vertex group panel
            -vertgroup_manip_end_index: end index on the vertex group panel
            -vertgroup_manip_regex: regex text for searching vertex group
    """
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
    """ PROPERTYGROUP: contains list of vertex groups
    attr:
        > properties
            -name: name of the vertex group
            -obj_type: type of the vertex group
            -vertgroup_index: index of the vertex group on the list
    """
    #name: StringProperty() -> instantiated by default
    obj_type: bpy.props.StringProperty()
    index: bpy.props.IntProperty()


class NTRZ_OT_vertgroup_manip_list_bulk_add_actions(bpy.types.Operator):
    """ OPERATOR: holds actions related to bulk add vertex groups
    attr:
        > action
            -SET_START: sets vertgroup_manip_start_index to the active vertex group's index
            -SET_END: sets vertgroup_manip_end_index to the active vertex group's index
            -BULK_ADD_INDEXES: adds vertex groups between and including the indexes to the end of vertgroup_manip_list
            -BULK_INSERT_INDEXES: same as above but inserts it above the active index
            -BULK_ADD_REGEX: adds vertex groups that matches the regex text set forth in vertgroup_manip_regex
            -BULK_INSERT_REGEX: same as above but inserts it above the active index
    """
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
        index = scene.NTRZ_vertgroup_manip_list_index

        match self.action:
            case 'SET_START':
                scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_start_index = context.object.vertex_groups.active_index
            case 'SET_END':
                scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_end_index = context.object.vertex_groups.active_index
            case 'BULK_ADD_INDEXES':
                for vertgroup_index in range(scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_start_index, scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_end_index+1):
                    vertgroup_name = context.object.vertex_groups[vertgroup_index].name
                    print('adding %s' % vertgroup_name)
                    item = scene.NTRZ_vertgroup_manip_list.add()
                    item.name = vertgroup_name
                    item.obj_type = 'STRING'
                    item.index = vertgroup_index
                    scene.NTRZ_vertgroup_manip_list_index = len(scene.NTRZ_vertgroup_manip_list)-1
            case 'BULK_INSERT_INDEXES':
                for vertgroup_index in reversed(range(scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_start_index, scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_end_index+1)):
                    vertgroup_name = context.object.vertex_groups[vertgroup_index].name
                    print('adding %s' % vertgroup_name)
                    item = scene.NTRZ_vertgroup_manip_list.add()
                    item.name = vertgroup_name
                    item.obj_type = 'STRING'
                    item.index = vertgroup_index
                    scene.NTRZ_vertgroup_manip_list.move(len(scene.NTRZ_vertgroup_manip_list)-1, scene.NTRZ_vertgroup_manip_list_index)
                scene.NTRZ_vertgroup_manip_list_index += scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_end_index - scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_start_index - 1
            case 'BULK_ADD_REGEX':
                import re
                text_regex = scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_regex
                match_vertgroups = []
                for x in range(0,len(bpy.context.object.vertex_groups)):
                    vertgroup_name = bpy.context.object.vertex_groups[x].name
                    if re.search(text_regex, vertgroup_name, re.IGNORECASE):
                        match_vertgroups.append(x)

                for vertgroup_index in match_vertgroups:
                    item = scene.NTRZ_vertgroup_manip_list.add()
                    item.name = context.object.vertex_groups[vertgroup_index].name
                    item.obj_type = 'STRING'
                    item.index = vertgroup_index
                scene.NTRZ_vertgroup_manip_list_index = len(scene.NTRZ_vertgroup_manip_list)-1
            case 'BULK_INSERT_REGEX':
                import re
                text_regex = scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_regex
                match_vertgroups = []
                for x in range(0,len(bpy.context.object.vertex_groups)):
                    vertgroup_name = bpy.context.object.vertex_groups[x].name
                    if re.search(text_regex, vertgroup_name, re.IGNORECASE):
                        match_vertgroups.append(x)

                for vertgroup_index in reversed(match_vertgroups):
                    item = scene.NTRZ_vertgroup_manip_list.add()
                    item.name = context.object.vertex_groups[vertgroup_index].name
                    item.obj_type = 'STRING'
                    item.index = vertgroup_index
                    scene.NTRZ_vertgroup_manip_list.move(len(scene.NTRZ_vertgroup_manip_list)-1, scene.NTRZ_vertgroup_manip_list_index)
                scene.NTRZ_vertgroup_manip_list_index += len(match_vertgroups) - 1
            case _:
                pass
        return {'FINISHED'}

class NTRZ_OT_vertgroup_manip_list_actions(bpy.types.Operator):
    """ OPERATOR: holds actions related to adding/removing/moving data within vertgroup_manip_list
    attr:
        > action
            -UP: moves active selection in vertgroup_manip_list up one spot
            -DOWN: moves active selection in vertgroup_manip_list down one spot
            -REMOVE: removes active selection in vertgroup_manip_list from the list
            -ADD: adds the active selection in the object's vertex group list to the end of vertgroup_manip_list
            -INSERT: same as above but inserts it above the active selection in vertgroup_manip_list
    """
    bl_idname = 'ntrz.vertgroup_manip_list_actions'
    bl_label = 'Vertgroup List Actions'
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
        index = scene.NTRZ_vertgroup_manip_list_index

        try:
            item = scene.NTRZ_vertgroup_manip_list[index]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and index < len(scene.NTRZ_vertgroup_manip_list)-1:
                scene.NTRZ_vertgroup_manip_list.move(index, index+1)
                scene.NTRZ_vertgroup_manip_list_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.NTRZ_vertgroup_manip_list_index+1)
                self.report({'INFO'}, info)
            elif self.action == 'UP' and index >= 1:
                scene.NTRZ_vertgroup_manip_list.move(index, index-1)
                scene.NTRZ_vertgroup_manip_list_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.NTRZ_vertgroup_manip_list_index+1)
                self.report({'INFO'}, info)
            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scene.NTRZ_vertgroup_manip_list[index].name)
                scene.NTRZ_vertgroup_manip_list.remove(index)
                if index > 0:
                    scene.NTRZ_vertgroup_manip_list_index -= 1
                else:
                    scene.NTRZ_vertgroup_manip_list_index = 0
                self.report({'INFO'}, info)

        if self.action == 'ADD' or self.action == 'INSERT':
            if context.object.vertex_groups.active_index >= 0:
                active_vertgroup_index = context.object.vertex_groups.active_index
                active_vertgroup_name = context.object.vertex_groups[active_vertgroup_index].name
                item = scene.NTRZ_vertgroup_manip_list.add()
                item.name = active_vertgroup_name
                item.obj_type = 'STRING'
                item.index = active_vertgroup_index
                if self.action == 'ADD':
                    scene.NTRZ_vertgroup_manip_list_index = len(scene.NTRZ_vertgroup_manip_list)-1
                else:
                    scene.NTRZ_vertgroup_manip_list.move(len(scene.NTRZ_vertgroup_manip_list)-1, scene.NTRZ_vertgroup_manip_list_index)
                info = '"%s" added to list' % (active_vertgroup_name)
                self.report({'INFO'}, info)
        return {'FINISHED'}

class NTRZ_OT_vertgroup_manip_clear_list(bpy.types.Operator):
    """ OPERATOR: clears vertgroup_manip_list
    attr:
        > None
    """
    bl_idname = 'ntrz.vertgroup_manip_clear_list'
    bl_label = 'Clear List'
    bl_description = ''
    bl_options = {"INTERNAL", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.NTRZ_vertgroup_manip_list)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.NTRZ_vertgroup_manip_list):
            context.scene.NTRZ_vertgroup_manip_list.clear()
            self.report({'INFO'}, 'List cleared')
        else:
            self.report({'INFO'}, 'Nothing to clear')
        return{'FINISHED'}

class NTRZ_OT_vertgroup_manip_list_remove_duplicates(bpy.types.Operator):
    """ OPERATOR: removes duplicates from vertgroup_manip_list
    attr:
        > None
    """
    bl_idname = 'ntrz.vertgroup_manip_list_remove_duplicates'
    bl_label = 'Remove Duplicates'
    bl_description = ''
    bl_options = {"INTERNAL", "UNDO"}

    def find_duplicates(self, context):
        name_lookup = {}
        for c, i in enumerate(context.scene.NTRZ_vertgroup_manip_list):
            name_lookup.setdefault(i.name, []).append(c)
        duplicates = set()
        for name, indexes in name_lookup.items():
            for i in indexes[1:]:
                duplicates.add(i)
        return sorted(list(duplicates))

    @classmethod
    def poll(cls, context):
        return bool(context.scene.NTRZ_vertgroup_manip_list)

    def execute(self, context):
        scene = context.scene
        for i in reversed(self.find_duplicates(context)):
            scene.NTRZ_vertgroup_manip_list.remove(i)
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
