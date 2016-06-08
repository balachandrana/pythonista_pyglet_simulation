from __future__ import division
import scene
import pyglet

fragment_shader_text1 = """
varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
uniform float u_scale;

void main(void) {
    vec2 uv = v_tex_coord;
    vec3 color = vec3(0.0, 0.0, 0.0);
    vec2 center = vec2(.5, .5);
    // set center based on time
    center -= 0.2*vec2(sin(u_time), cos(u_time));
    vec4 pixel_color = texture2D(u_texture, uv);
    float radius = length(uv - center);
    if (radius < .4) {
        color = pixel_color.xyz;
    };
    //Covert to gray image
    //color = vec4(vec3(color.r+color.g+color.b/3.0), 1.0);
    gl_FragColor = vec4(vec3(color), 1.0);
}

"""

fragment_shader_text2 = """
varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
uniform float u_scale;

void main(void) {
    vec2 uv = v_tex_coord;
    vec3 color = vec3(0.0, 0.0, 0.0);
    vec2 center = vec2(.5, .5);
    // set center based on touch position
    center -= (u_offset -vec2(.5, .5));
    vec4 pixel_color = texture2D(u_texture, uv);
    float radius = length(uv - center);
    if (radius < .4) {
        color = pixel_color.xyz;
    };
    //Covert to gray image
    //color = vec4(vec3(color.r+color.g+color.b/3.0), 1.0);
    gl_FragColor = vec4(vec3(color), 1.0);
}

"""

class MyScene(scene.Scene):
    def setup(self):
        im1 = scene.load_image_file('snake.png')
        self.sprite_node1 = scene.SpriteNode(im1, position=(200,200),
            size=(256, 256),
            parent=self)
        self.sprite_node1.shader = scene.Shader(fragment_shader_text1)
        im2 = scene.load_image_file('kitten.jpg')
        self.sprite_node2 = scene.SpriteNode(im2, position=(400,400),
            size=(256, 256),
            parent=self )
        self.sprite_node2.shader = scene.Shader(fragment_shader_text2)
        self.u_offset = (0.5, 0.5)

    def key_down(self, key):
        if key.key_val == pyglet.window.key.RIGHT:
            self.sprite_node1.position = ((self.sprite_node1.position[0]+10)%self.size[0],
                                    self.sprite_node1.position[1])
        elif key.key_val == pyglet.window.key.LEFT:
            self.sprite_node1.position = ((self.size[0]+self.sprite_node1.position[0]-10)%self.size[0],
                                    self.sprite_node1.position[1])
        elif key.key_val == pyglet.window.key.UP:
            self.sprite_node2.position = (self.sprite_node2.position[0],
                                    (self.sprite_node2.position[1]+10)%self.size[1])
        elif key.key_val == pyglet.window.key.DOWN:
            self.sprite_node2.position = (self.sprite_node2.position[0],
                                    (self.size[0]+self.sprite_node2.position[1]-10)%self.size[1])
        #else:
        #    self.label.text = "Key pressed %s" % chr(key.key_val)

    def compute_offset(self, touch):
        def clamp(v):
            if (v < 0):
                return 0
            elif v > 1.0:
                return 1.0
            else:
                return v
        return (clamp((touch.location[0]-self.sprite_node2.position[0]
                + self.sprite_node2.anchor_point[0]*self.sprite_node2.size[0])/self.sprite_node2.size[0]),
                clamp((touch.location[1]-self.sprite_node2.position[1]
                + self.sprite_node2.anchor_point[1]*self.sprite_node2.size[1])/self.sprite_node2.size[1]))

    def touch_began(self, touch):
        offset = self.compute_offset(touch)
        self.u_offset = (offset[0], 1.0-offset[1])

    def touch_moved(self, touch):
        offset = self.compute_offset(touch)
        self.u_offset =  (offset[0], 1.0-offset[1])

scene.run(MyScene(screen_width=800, screen_height=800))
