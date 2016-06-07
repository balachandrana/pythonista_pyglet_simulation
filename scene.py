from __future__ import division
import pyglet
from pyglet.gl import *
from shader import Shader as ShaderCreate
from datetime import datetime
from StringIO import StringIO
from PIL import Image

scene_obj = None
bounds = None
root_node = None
size = None
t = 0
dt = 1
DEFAULT_ORIENTATION = "PORTRAIT"

# Todo:
#  1. Currently position, size, color are plain tuples. May be we need
#     to implement pythoista like classes that can do vector operations
#  2. Currently position attribute of a child node is absolute and
#     it needs to be made relative to parent node
#  3. z_position -  not implemented
#  4. rotation - user can implement this in shader
#  5. action not implemented - user can implement this in shader
#  6. optimization in pyglet like "batches" to be implemeted
#  7. shape node not implemented - user can implement this in shader
#      - some examples given
#  8. effectnode not implemented

class Node(object):
    def __init__(self, position=None, size=None, parent=None):
        if position:
            self.position = position
        else:
            self.position = (scene_obj.size[0]/2, scene_obj.size[1]/2)
        self.size = size
        self.anchor_point = (0.5, 0.5)
        self.z_position = 0.0
        self.alpha = 255
        self.children = []
        self.parent = parent
        if self.parent:
            self.parent.add_child(self)

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def remove_from_parent(self):
        self.parent.children.remove(self)
        self.parent = None

    def draw(self):
        pass

    def draw_internal(self, nodes=None):
        self.draw()
        for ch in self.children:
            ch.draw_internal()

    def action(self):
        pass

    def action_internal(self):
        self.action()
        for ch in self.children:
            ch.action_internal()

class LabelNode(Node):
    def __init__(self, text, position=None, size=None,
            font_name='Times New Roman',
            font_size=36,
            color=(255, 255, 255, 255),
            anchor_x='center', anchor_y='center', parent=None):
        super(LabelNode, self).__init__(position, size, parent)
        if not size:
            self.size = (None, None)
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.label =  pyglet.text.Label(self.text,
                    x=self.position[0],
                    y=self.position[1],
                    font_name=self.font_name,
                    font_size=self.font_size,
                    color=self.color,
                    width=self.size[0],
                    height=self.size[1],
                    anchor_x=self.anchor_x,
                    anchor_y=self.anchor_y)

    def draw(self):
        self.label =  pyglet.text.Label(self.text,
                    x=self.position[0],
                    y=self.position[1],
                    font_name=self.font_name,
                    font_size=self.font_size,
                    color=self.color,
                    width=self.size[0],
                    height=self.size[1],
                    anchor_x=self.anchor_x,
                    anchor_y=self.anchor_y)
        self.label.draw()

class SpriteNode(Node):
    def __init__(self, image, position=None, size=None,
            anchor_point=(.5, .5), parent=None):
        super(SpriteNode, self).__init__(position, size, parent)
        self.sprite = image
        self.shader_state = 0.0
        self.shader = None
        if not size:
            self.size = (self.sprite.width, self.sprite.height)
        self.anchor_point = anchor_point

    def draw(self):
        global scene_obj
        self.high_x = self.position[0]+self.anchor_point[0]*self.size[0]
        self.low_x = self.position[0]-self.anchor_point[0]*self.size[0]
        self.high_y = self.position[1]+self.anchor_point[1]*self.size[1]
        self.low_y = self.position[1]-self.anchor_point[1]*self.size[1]
        if True:
            if self.shader:
                self.shader.bind()
                self.shader.uniformf('u_offset', *scene_obj.u_offset)
                self.shader.uniformf('u_shader_state', self.shader_state)
                self.shader.uniformf('u_time', scene_obj.u_delta_time)
                self.shader.uniformf('u_scale', 1.0)
                self.shader.uniformf('u_sprite_size', *self.size)
                glEnable(GL_TEXTURE_2D)
                self.texture = self.sprite.get_texture()
                gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
                self.texture.width = self.size[0]
                self.texture.height = self.size[1]
                glBindTexture(self.texture.target, self.texture.id)
                glDisable(GL_TEXTURE_2D)
                glActiveTexture(GL_TEXTURE0)
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texture.id)
                self.shader.uniformi('u_texture', 0)
                glDisable(GL_TEXTURE_2D)

                glBegin(GL_QUADS)
                glVertex2f(self.high_x, self.high_y)
                glTexCoord2i(1, 1)
                glVertex2f(self.low_x, self.high_y)
                glTexCoord2i(1, 0)
                glVertex2f(self.low_x,  self.low_y)
                glTexCoord2i(0, 0)
                glVertex2f(self.high_x,  self.low_y)
                glTexCoord2i(0, 1)
                glEnd()
                self.shader.unbind()
            else:
                position = (self.position[0]-self.anchor_point[0]*self.size[0],
                            self.position[1]-self.anchor_point[1]*self.size[1])
                self.sprite.blit(*position, width=self.size[0], height=self.size[1])

class Touch(object):
    def __init__(self, x, y, prev_x, prev_y, touch_id):
        self.location = (x,y)
        self.prev_location = (prev_x, prev_y)
        self.touch_id = touch_id

class Key(object):
    def __init__(self, key_val, key_modifiers, key_id):
        self.key_val = key_val
        self.key_modifiers = key_modifiers
        self.key_id = key_id

class Scene(pyglet.window.Window):
    def __init__(self, screen_width=800, screen_height=800):
        global scene_obj
        super(Scene, self).__init__(screen_width, screen_height)
        scene_obj = self
        self.size = (screen_width, screen_height)
        self.parent = None
        self.root_node = root_node = Node()
        self.bounds = bounds = (0, 0, self.size[0], self.size[1])
        self.current_touch = self.first_touch = Touch(0,0,0,0,0)
        self.touch_count = 0
        self.keys = {}
        self.touches = {}
        self.u_time = 0.0
        self.u_offset = (0.0, 0.0)
        self.texture = None
        self.shader = None
        self.background_color = self.prev_background_color = None
        self.orientation = DEFAULT_ORIENTATION
        self.frame_interval = 1.0
        self.anti_alias = False
        self.show_fps = False
        self.position = (self.size[0]/2, self.size[1]/2)
        self.anchor_point = (0.5, 0.5)
        self.z_position = 0.0
        self.alpha = 255

    def setup(self):
        pass

    def add_child(self, node):
        self.root_node.children.append(node)
        node.parent = self

    def remove_from_parent(self):
        pass

    def draw_internal(self, nodes=None):
        for ch in self.root_node.children:
            ch.draw_internal()

    def update(self):
        pass

    def action(self):
        pass

    def action_internal(self):
        self.action()
        for ch in self.root_node.children:
            ch.action_internal()

    def run(self, orientation=DEFAULT_ORIENTATION, frame_interval=1, anti_alias=False, show_fps=False):
        global t, dt
        self.orientation = orientation
        self.frame_interval = frame_interval
        self.anti_alias = anti_alias
        self.show_fps = show_fps
        self.setup()
        self.u_start_time = datetime.now()
        ft = pyglet.font.load('Arial', 28)
        fps_text = pyglet.font.Text(ft, y=10)
        pyglet.clock.set_fps_limit(60.0/self.frame_interval)
        t = 0.0
        dt = 0.0
        while not self.has_exit:
            self.u_delta_time_tuple = [float(i) for i in str(
                datetime.now() -self.u_start_time).split(':')]
            self.u_delta_time = (self.u_delta_time_tuple[0]*3600
                + self.u_delta_time_tuple[1]*60 + self.u_delta_time_tuple[2])
            dt = self.u_delta_time - dt
            t =  self.u_delta_time
            self.dispatch_events()
            self.clear()
            if self.background_color and (
                    self.background_color != self.prev_background_color):
                self.prev_background_color = self.background_color
                pyglet.gl.glClearColor(*self.background_color)
            self.update()
            self.action_internal()
            self.draw_internal()
            pyglet.clock.tick()
            if self.show_fps:
                fps_text.text = ("fps: %d") % (pyglet.clock.get_fps())
                fps_text.draw()
            self.flip()

    def touch_began(self, touch):
        pass

    def touch_moved(self, touch):
        pass

    def touch_ended(self, touch):
        pass

    def key_down(self, key):
        pass

    def key_up(self, key):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.current_touch.location = (x, y)
        self.touch_moved(self.current_touch)

    def on_mouse_release(self, x, y, button, modifiers):
        self.current_touch.location = (x, y)
        self.touch_ended(self.current_touch)

    def on_mouse_press(self, x, y, button, modifiers):
        self.current_touch.location = (x, y)
        self.touch_began(self.current_touch)
        #self.touches[self.touch_count] = touch
        self.current_touch = self.first_touch
        self.touch_count += 1

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
            return pyglet.event.EVENT_HANDLED
        else:
            key_val = symbol
            key_modifiers = modifiers
            keyobj = Key(key_val, key_modifiers, self.touch_count)
            #self.keys[key_val] = self.touch_count
            self.touch_count += 1
            self.key_down(keyobj)

    def on_key_release(self, symbol, modifiers):
        key_val = symbol
        key_modifiers = modifiers
        keyobj = Key(key_val, key_modifiers, self.touch_count)
        #self.touch_count += 1
        self.key_up(keyobj)

def get_screen_size():
    return scene_obj.size

def get_screen_scale():
    return 1.0

def get_image_path(name):
    #todo
    return ""

def load_image_file(path):
    return pyglet.resource.image(path)

def pil_image_to_pyglet_image(pil_image):
    image_stream = StringIO()
    pil_image.save(image_stream, format='PNG')
    pyglet_image = pyglet.image.load('dummy_file.png', file=image_stream)
    return pyglet_image

def pyglet_image_to_pil_image(pyglet_image):
    image_stream = StringIO()
    pyglet_image.save('dummy_file.png', file=image_stream)
    pil_image = Image.open(image_stream)
    '''#from http://stackoverflow.com/questions/896548/how-to-convert-a-pyglet-image-to-a-pil-image
    w,h = im.width, im.height
    pitch = -(w * len('RGB'))
    data = im.get_data('RGB', pitch)
    pil_img = PIL.Image.fromstring('RGB', (w, h), data)'''
    return pil_image

vertex_shader_text = """
varying vec2 v_tex_coord;

void
main() {
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	v_tex_coord = vec2(gl_MultiTexCoord0);
}
"""

def Shader(fragment_shader_text):
    global vertex_shader_text
    return ShaderCreate(vertex_shader_text, fragment_shader_text)

def run(scene_obj_param, orientation=DEFAULT_ORIENTATION, frame_interval=1, anti_alias=False, show_fps=False):
    global scene_obj

    scene_obj.run(orientation=orientation, frame_interval=frame_interval, anti_alias=anti_alias, show_fps=show_fps)
