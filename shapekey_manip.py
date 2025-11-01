"""/// ANTARES AVATAR MANIUPLATION ASSIST: VERTGROUP_MANIP /////////////////////
 ///
//    HELLO!
//
//    COPYRIGHT (C) 2022 ANTARES HUSKY (HUSKY@ANTARES.DOG)
//
////////////////////////////////////////////////////////////////////////////"""

import bpy


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
