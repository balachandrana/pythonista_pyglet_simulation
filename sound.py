
import pyglet
import scene

'''
sound.load_effect(name)
Preload the sound effect with the given name to reduce latency when using play_effect().

sound.play_effect(name[, volume, pitch])
Play the sound effect with the given name.

Playback is asynchronous, i.e. the function returns before the sound has finished playing. The return value is an opaque identifier that can be used with the stop_effect() function. The volume and pitch arguments are optional, by default, the effect is played with the global volume, as set by set_volume().

sound.stop_effect(effect_id)
Stops playback of a sound effect. The effect_id is the return value of play_effect().

sound.set_volume(vol)
Sets the default volume for all sound effects (between 0.0 and 1.0, the default is 0.5).
'''

sound_objects = {}
_default_value = 0.5

def load_effect(name):
    if name.endswith('.wav') or name.endswith('.ogg'):
        sound_objects[name[:-4]] = pyglet.media.load(name, streaming=False)
    else:
        raise

def play_effect(name, volume=_default_value, pitch=None):
    sound_objects[name].volume = volume
    sound_objects[name].play()

def stop_effect(effect_id):
    sound_objects[name].pause()

#set default volume (not current volume)
def set_volume(vol):
    global _default_value
    _default_value = vol
