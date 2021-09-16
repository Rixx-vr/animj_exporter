# Blender AnimJSON exporter

This Blender plugin exports the animation data from a scene or from a selection of objects as an JSON object. This file can be used in NEOS VR as an animation assets.

## Limitations
- The plugin is currently in development and the animation data is currently limited to simple animation tracks (ie. Position, Rotation and Schale).
- only float3 or float4 is currently implemented
- Bones haven't been tested yes
- Independent keyframes for different dimensions of the same property are not supported

## installation
- Download this project as zip file (Code > Download ZIP)
- install the unextracted zip file with Blenders add-on manager.
- to enable the plugin you need to select testing when picking the add-on from the list.
