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
    vertgroup_manip_selector: bpy.props.EnumProperty(
        name='Vertex Group to Manipulate',
        items=(
            ('ALL', 'All', ''),
            ('INCLUSION', 'Including Listed', ''),
            ('EXCLUSION', 'Excluding Listed', '')
        )
    )

    vertgroup_manip_start_index: bpy.props.IntProperty(
        name='Vertex Group Manipulation Start Index',
        default=0
    )

    vertgroup_manip_end_index: bpy.props.IntProperty(
        name='Vertex Group Manipulation End Index',
        default=0
    )

    vertgroup_manip_regex: bpy.props.StringProperty(
        name='Vertex Group Manipulation Regex Text',
        default='.*'
    )

    vertgroup_manip_rename_prefix: bpy.props.StringProperty(
        name='Vertex Group Manipulation Rename Prefix Text',
        default='DEF-'
    )

    vertgroup_manip_rename_suffix: bpy.props.StringProperty(
        name='Vertex Group Manipulation Rename Suffix Text'
    )

    vertgroup_manip_exclusion_regex: bpy.props.StringProperty(
        name='Vertex Group Manipulation Exclusion Regex Text'
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

def get_filtered_vgroups():
    context = bpy.context
    scene = context.scene
    if scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_selector == 'ALL':
        vgroups = bpy.context.active_object.vertex_groups
    elif scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_selector == 'INCLUSION':
        vgroups = []
        whitelist = [vgroup.name for vgroup in context.scene.NTRZ_vertgroup_manip_list]
        for vgroup in bpy.context.active_object.vertex_groups:
            if vgroup.name in whitelist:
                vgroups.append(vgroup)
    elif scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_selector == 'EXCLUSION':
        vgroups = []
        blacklist = [vgroup.name for vgroup in context.scene.NTRZ_vertgroup_manip_list]
        for vgroup in bpy.context.active_object.vertex_groups:
            if vgroup.name not in blacklist:
                vgroups.append(vgroup)
    return vgroups

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

class NTRZ_OT_vertgroup_manip_duplicate_and_rename(bpy.types.Operator):
    """ OPERATOR: duplicates vertgroups on the list and renames them according to pyregex
    attr:
        > None
    """
    bl_idname = 'ntrz.vertgroup_manip_duplicate_and_rename'
    bl_label = 'Duplicate to New Name'
    bl_description = ''
    bl_options = {"INTERNAL", "UNDO"}

    def execute(self, context):
        scene = context.scene
        # index = scene.NTRZ_vertgroup_manip_list_index

        rename_text_prefix = str(scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_rename_prefix)
        rename_text_suffix = str(scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_rename_suffix)

        # try:
        #     item = scene.NTRZ_vertgroup_manip_list[0] #check if there is something at all
        # except IndexError:
        #     info = 'List is empty. Nothing to manipulate.'
        #     self.report({'INFO'}, info)
        # else:
        
    # vertgroup_manip_selector: bpy.props.EnumProperty(
    #     name='Vertex Group to Manipulate',
    #     items=(
    #         ('ALL', 'All', ''),
    #         ('INCLUSION', 'Including Listed', ''),
    #         ('EXCLUSION', 'Excluding Listed', '')
    #     )
    # )

        # Get the active object
        obj = bpy.context.active_object

        # create list of vgroups
        vgroups = get_filtered_vgroups()

        # Iterate through the vertex groups in the object
        for vgroup in vgroups:
            # Check if the vertex group name does not start with desired prefix
            if not (vgroup.name.startswith(rename_text_prefix) and vgroup.name.endswith(rename_text_suffix)):
                try:
                    obj.vertex_groups.remove(obj.vertex_groups.get(rename_text_prefix+vgroup.name+rename_text_suffix))
                except:
                    print('cant find ' + rename_text_prefix+vgroup.name+rename_text_suffix)
                bpy.ops.object.vertex_group_set_active(group=vgroup.name)
                bpy.ops.object.vertex_group_copy()
                obj.vertex_groups.active.name = rename_text_prefix+vgroup.name+rename_text_suffix
                print('created %s' % obj.vertex_groups.active.name)
            
        # Update the object
        obj.update_from_editmode()
        
        return {'FINISHED'}

class NTRZ_OT_vertgroup_manip_remove_zero_weight_vertgroup(bpy.types.Operator):
    """ OPERATOR: removes vertex groups with no weights in any of the object's vertices
    attr:
        > None
    """
    bl_idname = 'ntrz.vertgroup_manip_remove_zero_weight_vertgroup'
    bl_label = 'Remove Zero Weight Vertex Groups'
    bl_description = ''
    bl_options = {"INTERNAL", "UNDO"}

    def execute(self, context):
        scene = context.scene
        # index = scene.NTRZ_vertgroup_manip_list_index

        exclusion_text_regex = str(scene.NTRZ_vertgroup_manip_settings.vertgroup_manip_exclusion_regex)

        # Get the active object
        obj = bpy.context.active_object
        if obj == None:
            info = 'Nothing is selected. Is object hidden?'
            print(info, end='\n\n')
            self.report({'INFO'}, info)
            return {'CANCELLED'}
        else:
            print('processing %s:' % obj.name)

        # import re
        # for vgroup in obj.vgroups:
        #     if not re.search(exclusion_text_regex, vgroup.name, re.IGNORECASE):
        #         for vert in obj.data.vertices:

        vgroups = get_filtered_vgroups()
        vgroup_indexes = [vgroup.index for vgroup in vgroups]
        for vert in obj.data.vertices:
            for vgroup in vert.groups:
                if vgroup.group in vgroup_indexes:
                    vgroup_indexes.remove(vgroup.group)
        print('%d empty vertex group(s) found.' % len(vgroup_indexes))

        count_removed = 0
        for vgroup_index in reversed(vgroup_indexes):
            print('removing %s...' % obj.vertex_groups[vgroup_index].name, end='')
            try:
                obj.vertex_groups.remove(obj.vertex_groups[vgroup_index])
            except:
                print('error')
            else:
                count_removed += 1
                print('ok')

        info = '%d vertex group(s) removed.' % (count_removed)
        print(info, end='\n\n')
        self.report({'INFO'}, info)

        return {'FINISHED'}

class NTRZ_OT_vertgroup_manip_transfer_vertex_weight(bpy.types.Operator):
    """ OPERATOR: transfer vertex weights from all selected object to active object
    attr:
        > None
    """
    bl_idname = 'ntrz.vertgroup_manip_transfer_vertex_weight'
    bl_label = 'Transfer Vertex Weight to Active Object'
    bl_description = ''
    bl_options = {"INTERNAL", "UNDO"}

    def execute(self, context):
        scene = context.scene

        bpy.ops.object.data_transfer(use_reverse_transfer=True, data_type='VGROUP_WEIGHTS', use_max_distance=True, max_distance=0.001, layers_select_src='NAME', layers_select_dst='ALL')

        return {'FINISHED'}