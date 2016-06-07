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


void main(void) {
    vec2 uv = v_tex_coord;
    vec2 center = vec2(.5, .5);
    vec3 color = vec3(1.0, 1.0, 1.0);
    float radius = length(uv - center);
    if (radius < .4) {
        color = vec3(1.0, 0.0, 0.0);
    };
    gl_FragColor = vec4(color, 1.0);
}

"""

from PIL import Image

class MyScene(scene.Scene):
    def setup(self):
        '''im1 = Image.open('kitten.jpg').convert('RGBA')
        im2 = im1.resize((64, 64))
        im = scene.pil_image_to_pyglet_image(im2)'''
        '''im = scene.load_image_file('kitten.jpg')
        pil_im = scene.pyglet_image_to_pil_image(im)
        out = pil_im.resize((64, 64))
        out.save('kitt.png')'''
        im = scene.load_image_file('white_rectangle_512_512.png')
        self.sprite_node = scene.SpriteNode(im, position=(400,400),
            size=(512, 512),
            parent=self)
        self.sprite_node.shader = scene.Shader(fragment_shader_text)

    def key_down(self, key):
        if key.key_val == pyglet.window.key.RIGHT:
            self.sprite_node.position = ((self.sprite_node.position[0]+10)%self.size[0],
                                    self.sprite_node.position[1])
        elif key.key_val == pyglet.window.key.LEFT:
            self.sprite_node.position = ((self.size[0]+self.sprite_node.position[0]-10)%self.size[0],
                                    self.sprite_node.position[1])
        elif key.key_val == pyglet.window.key.UP:
            self.sprite_node.position = (self.sprite_node.position[0],
                                    (self.sprite_node.position[1]+10)%self.size[1])
        elif key.key_val == pyglet.window.key.DOWN:
            self.sprite_node.position = (self.sprite_node.position[0],
                                    (self.size[0]+self.sprite_node.position[1]-10)%self.size[1])
        #else:
        #    self.label.text = "Key pressed %s" % chr(key.key_val)

    def touch_began(self, touch):
        self.sprite_node.position = touch.location

    def touch_moved(self, touch):
        self.sprite_node.position = touch.location

scene.run(MyScene(screen_width=800, screen_height=800))
