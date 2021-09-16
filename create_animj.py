import json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class Animation(Object):
    def __init__(self, name, globalDuration=0):
        self.name = name
        self.globalDuration = globalDuration
        self.track = list()


    def add_track(self, track):
        self.track.append(track)


class Tack(Object):
    def __init__(self, trackType="Discrete", valueType="float"):
        self.trackType = trackType
        self.valueType = valueType
        self.data = None


class Data(Object):
    def __init__(self, node, property):
        self.node = node
        self.property = property
        self.keyframe = list()

    def add_keyframe(self, keyframe):
        self.keyframe.append(keyframe)

class Keyframe(Object):
    def __init__(self, time, value):
        self.time = time
        self.value = value


a = Animation("Test")
t = Tack()
d = Data("Box", "Position")

d.add_keyframe(Keyframe(0, 1))
d.add_keyframe(Keyframe(1, 3))
d.add_keyframe(Keyframe(2, -3))

t.data = d
a.add_track(t)
