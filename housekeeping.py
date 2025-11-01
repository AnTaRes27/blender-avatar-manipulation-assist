"""/// ANTARES AVATAR MANIUPLATION ASSIST v0.1.0 //////////////////////////////
 ///
//    HELLO!
//
//    COPYRIGHT (C) 2022 ANTARES HUSKY (HUSKY@ANTARES.DOG)
//
////////////////////////////////////////////////////////////////////////////"""

import bpy

class NTRZ_OT_housekeeping_actions(bpy.types.Operator):
    """ OPERATOR: holds various housekeeping actions
    attr:
        > action
            -RENAME_MESH_TO_OBJECT: rename meshes to their corresponding objects' names
            -LIST_ORPHANS: list orphaned datablocks
            -PURGE_ORPHANS: purge orphaned datablocks
    """
    bl_idname = 'ntrz.housekeeping_actions'
    bl_label = 'Housekeeping Actions'
    bl_description = ''
    bl_options = {"REGISTER", "UNDO"}

    action: bpy.props.EnumProperty(
        items=(
            ('RENAME_MESH_TO_OBJECT', 'Rename mesh to its objects name', ''),
            ('LIST_ORPHANS', 'List', ''),
            ('PURGE_ORPHANS', 'Purge', '')
        )
    )

    def find_orphaned_datablocks(self, datablocks):
        """ find datablocks without a user
        args:
            > datablocks: list of datablock
        return:
            > orphaned_datablocks: list of orphaned datablock
        """
        orphaned_datablocks = []
        for datablock in datablocks:
            if not datablock.users:
                orphaned_datablocks.append(datablock)
        return orphaned_datablocks

    def list_users_of_datablock(self, datablock_id):
        """ lists the users of a datablock, sorted by user type
        args:
            > datablock_id: datablock in question
        return:
            > users_of_datablock: list of the users of datablock
        """
        def find_users_of_datablock(datablock_id):
            def users(datablock_types):
                ret = tuple(datablock.id_data for datablock in datablock_types if datablock.user_of_id(datablock_id))
                return ret if ret else None
            return filter(
                None, (
                    users(getattr(bpy.data, attributes))
                    for attributes in dir(bpy.data)
                    if isinstance( #check if isntance of prop
                            getattr(bpy.data, attributes, None),
                            bpy.types.bpy_prop_collection
                            )
                    )
                )
        users_of_datablock = []
        for user in find_users_of_datablock(datablock_id):
            users_of_datablock.append(user)
        return users_of_datablock if users_of_datablock else None


    def execute(self, context):
        scene = context.scene

        match self.action:
            case 'RENAME_MESH_TO_OBJECT':
                #get list of objects
                objects = list(obj for obj in bpy.data.objects if obj.type == 'MESH')
                meshes_multiple_users = []
                for obj in objects:
                    #for every object, get their corresponding meshes
                    mesh = obj.data

                    #checks: make sure each mesh only has one object user   
                    mesh_users = self.list_users_of_datablock(mesh)
                    for collection_of_datablock in mesh_users:
                        try:
                            datablock_type = collection_of_datablock[0].type
                        except:
                            mesh_users.remove(collection_of_datablock)
                        else:
                            if datablock_type != 'MESH':
                                mesh_users.remove(collection_of_datablock)
                    mesh_users = list(mesh_users[0])
                    #
                    if len(mesh_users) > 1:
                        #multiple user mesh
                        meshes_multiple_users.append(mesh)
                    else:
                        #rename mesh to object
                        print('rename %s to %s' % (mesh.name, obj.name))
                        mesh.name = obj.name
            case _:
                pass


        return {'FINISHED'}
    
