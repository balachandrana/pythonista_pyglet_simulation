from __future__ import division
import scene
import pyglet
import sound

class MyScene(scene.Scene):
    def setup(self):
        sound.load_effect('beep1.ogg')
        self.label =  scene.LabelNode(
            "Hello World",
            font_name='Times New Roman',
            color=(255, 0, 0, 255),
            parent=self)

    def key_down(self, key):
        self.label.text = "Hello World"
        if key.key_val == pyglet.window.key.RIGHT:
            self.label.position = ((self.label.position[0]+10)%self.size[0],
                                    self.label.position[1])
        elif key.key_val == pyglet.window.key.LEFT:
            self.label.position = ((self.size[0]+self.label.position[0]-10)%self.size[0],
                                    self.label.position[1])
        elif key.key_val == pyglet.window.key.UP:
            self.label.position = (self.label.position[0],
                                    (self.label.position[1]+10)%self.size[1])
        elif key.key_val == pyglet.window.key.DOWN:
            self.label.position = (self.label.position[0],
                                    (self.size[0]+self.label.position[1]-10)%self.size[1])
        else:
            ch = chr(key.key_val) if key.key_val < 256 else ' '
            if (key.key_modifiers & pyglet.window.key.MOD_SHIFT
                    ) or (key.key_modifiers & pyglet.window.key.MOD_CAPSLOCK):
                if key.key_val in range(ord('a'), ord('a')+26):
                    ch = chr(key.key_val - 32)
            self.label.text = "Key pressed %s" % ch

    def touch_began(self, touch):
        #self.label.text = "mouse clicked %d %d" %  touch.location
        self.label.position = touch.location
        sound.play_effect('beep1')
        self.background_color = (255, 255,255, 255)


    def touch_moved(self, touch):
        #self.label.text = "mouse clicked %d %d" %  touch.location
        self.label.position = touch.location

scene.run(MyScene(), show_fps=True)
