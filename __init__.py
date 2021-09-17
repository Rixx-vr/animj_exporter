bl_info = {
    "name": "AnimJ exporter",
    "description": "Writes Animation to AnimJ",
    "author": "Rixx",
    "version": (0, 1),
    "blender": (2, 93, 2),
    "location": "File > Export > AnimJ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/Rixx-vr/animj_exporter/issues",
    "support": 'TESTING',
    "category": "Import-Export"
}

import bpy
import bmesh
from bpy import context
from collections import Counter
import json

class JsonSerializable:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Animation(JsonSerializable):
    def __init__(self, name, globalDuration=0):
        self.name = name
        self.globalDuration = globalDuration
        self.tracks = list()


    def add_track(self, track):
        self.tracks.append(track)


class Tack(JsonSerializable):
    def __init__(self, trackType="Discrete", valueType="float"):
        self.trackType = trackType
        self.valueType = valueType
        self.data = None


class Data(JsonSerializable):
    def __init__(self, node, property):
        self.node = node
        self.property = property
        self.keyframes = list()


    def add_keyframe(self, keyframe):
        self.keyframes.append(keyframe)


class Keyframe(JsonSerializable):
    def __init__(self, time, value):
        self.time = time
        self.value = value

def __create_amimation(name, objects):
    NAME = ['x', 'y', 'z', 'w']
    TIME_INDEX = 0
    VALUE_INDEX = 1

    animation = Animation(name)

    for obj in objects:
        curves = obj.animation_data.action.fcurves
        property_name = [x.data_path for x in curves]
        properties = Counter(property_name)
        chanel = {}
        i = 0

        for property, dimention in properties.items():
            track = Tack(valueType='float{}'.format(dimention))
            data = Data(obj.name_full, property)
            track.data = data


            for key_index in range(len(curves[i].keyframe_points)):
                keyframe = {}
                time = curves[i].keyframe_points[key_index].co[TIME_INDEX]

                for dim_index in range(dimention):
                    keyframe[NAME[dim_index]] = curves[i + dim_index].keyframe_points[key_index].co[VALUE_INDEX]
                    print(keyframe[NAME[dim_index]])

                data.add_keyframe(Keyframe(time, keyframe))
            animation.add_track(track)
            i += dimention

    return animation


def writeAnimJ(self, pathani):
    file_path = self.filepath

    if self.selected:
        objects = bpy.context.selected_objects
    else:
        objects = bpy.data.objects

    animation = __create_amimation(file_path, objects)

    with open(file_path, 'w') as export_file:
        export_file.write(animation.toJSON())
        export_file.close()
    return {'FINISHED'}


class AnimJExport(bpy.types.Operator):
    bl_idname = "object.export_animj"
    bl_label = "AnimJ Export"
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = ".animj"

    filter_glob = bpy.props.StringProperty(default="*.animj", options={'HIDDEN'}, maxlen=255)
    selected: bpy.props.BoolProperty(name="Selected only", description="Export selected mesh items only", default=True)

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        if(context.active_object.mode == 'EDIT'):
            bpy.ops.object.mode_set(mode='OBJECT')

        writeAnimJ(self, context);
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_func_export(self, context):
    self.layout.operator(AnimJExport.bl_idname, text="Animation JSON (.AnimJ)")


def register():
    bpy.utils.register_class(AnimJExport)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(AnimJExport)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
