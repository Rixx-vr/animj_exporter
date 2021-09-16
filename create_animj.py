import json

class JsonSerializable:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Animation(JsonSerializable):
    def __init__(self, name, globalDuration=0):
        self.name = name
        self.globalDuration = globalDuration
        self.track = list()


    def add_track(self, track):
        self.track.append(track)


class Tack(JsonSerializable):
    def __init__(self, trackType="Discrete", valueType="float"):
        self.trackType = trackType
        self.valueType = valueType
        self.data = None


class Data(JsonSerializable):
    def __init__(self, node, property):
        self.node = node
        self.property = property
        self.keyframe = list()


    def add_keyframe(self, keyframe):
        self.keyframe.append(keyframe)


class Keyframe(JsonSerializable):
    def __init__(self, time, **kwargs):
        self.time = time
        self.__dict__.update(kwargs)
