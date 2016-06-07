# coding: utf-8
from __future__ import division
import scene
import pyglet

fragment_shader_text = """
varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
uniform float u_scale;
uniform float u_shader_state;


void main(void) {
    vec2 uv = v_tex_coord;
    vec3 color = vec3(1.0, 1.0, 1.0);
    if (u_shader_state == 1.0)
        if (uv.x > abs(sin(u_time)))
            color = vec3(1.0, 0.0, 0.0);
    gl_FragColor = vec4(color, 1.0);
}
"""
white_rectangle = scene.load_image_file('white_rectangle_512_512.png')

class Block(scene.SpriteNode):
    def __init__(self, text, value, position=(0,0),
            size=(96, 96), parent=None, **kwargs):
        super(Block, self).__init__(white_rectangle,
            position=position, size=size, parent=parent)
        self.shader = scene.Shader(fragment_shader_text)
        self.label = scene.LabelNode(text, position=position,
             parent=self, **kwargs)
        self.value = value
        self.enable_touch = True
        self.toggle = True # attribute for testing

    def hide(self):
        self.label.text = ""

    def reveal(self):
        self.label.text = u'♛'

    def select(self):
        self.shader_state = 1.0

    def deselect(self):
        self.shader_state = 0.0

    def block_action(self):
        if self.toggle:
            self.hide()
        else:
            self.reveal()
        self.toggle = not self.toggle

    def touch_began(self, touch):
        def contains(position, size, anchor_point, loc_position):
            pos = (position[0] - anchor_point[0]*size[0],
                position[1] - anchor_point[0]*size[1])
            if ((pos[0] <= loc_position[0] <= pos[0]+size[0]) and
                (pos[1] <= loc_position[1] <= pos[1]+size[1])):
                return True
            else:
                return False
        if contains(self.position, self.size, self.anchor_point,
                touch.location) and self.enable_touch:
            self.block_action()

class MyScene(scene.Scene):
    def setup(self):
        self.block =  Block(u'♛', 0,
                position=(self.size[0]/2, self.size[1]/2),
                size=(256, 256),
                parent=self,
                font_name='arialms',
                color=(0, 255, 0, 255))

    def touch_began(self, touch):
        self.block.touch_began(touch)

    def key_down(self, key):
        if key.key_val == pyglet.window.key.S:
            self.block.select()
        elif key.key_val == pyglet.window.key.D:
            self.block.deselect()

scene.run(MyScene(), show_fps=True)
