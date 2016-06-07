# coding: utf-8
from __future__ import division
import scene
import pyglet

white_rectangle = scene.load_image_file('white_rectangle_512_512.png')

class Block(scene.SpriteNode):
    def __init__(self, text, value, position=(0,0),
            size=(96, 96), parent=None, **kwargs):
        super(Block, self).__init__(white_rectangle,
            position=position, size=size, parent=parent)
        self.label = scene.LabelNode(text, position=position,
             parent=self, **kwargs)
        self.value = value
        self.enable_touch = True
        self.toggle = True # attribute for testing

    def hide(self):
        self.label.text = "."

    def reveal(self):
        self.label.text = u'♛'

class GridOfBlocks(object):
    def __init__(self, m, n,
                 position=(0,0),
                 size=(400, 400),
                 marginx=2,
                 marginy=2,
                 parent=None,
                 text_list=None,
                 value_list=None,
                 **kwargs):
        self.m = m
        self.n = n
        self.position = (self.x, self.y) = position
        self.size = (self.w, self.h) = size
        self.text_list = [u'♛']*(m*n)
        self.value_list = [0]*(m*n)
        self.parent = parent
        self.wb = self.w/m
        self.hb = self.h/n
        self.wbm = self.wb -2*marginx
        self.whm = self.hb -2*marginy
        start_pos = (self.x-self.w/2, self.y-self.h/2)
        self.grid = {}
        for i in range(self.m):
            for j in range(self.n):
                y1 = start_pos[1] + (m-1-i)*self.wb+marginy + self.hb/2
                x1 = start_pos[0] + (j)*self.hb+marginx+self.wb/2
                t =  self.text_list[i*self.n+(j)] # utf8.char(i*self.n+j+9812)
                v =  self.value_list[i*self.n+(j)] # utf8.char(i*self.n+j+9812)
                b = Block(t, v, position=(x1, y1),
                        size=(self.wbm, self.whm),
                        parent=parent, **kwargs)
                self.grid[i,j] = b

    def block_action(self, i, j):
        if self.grid[i, j].toggle:
            self.grid[i, j].hide()
        else:
            self.grid[i, j].reveal()
        self.grid[i, j].toggle = not self.grid[i, j].toggle

    def touch_began(self, touch):
        def contains(position, size, anchor_point, loc_position):
            pos = (position[0] - anchor_point[0]*size[0],
                position[1] - anchor_point[0]*size[1])
            if ((pos[0] <= loc_position[0] <= pos[0]+size[0]) and
                (pos[1] <= loc_position[1] <= pos[1]+size[1])):
                return True
            else:
                return False
        for i,j in self.grid:
            if contains(self.grid[i,j].position, self.grid[i,j].size,
                    self.grid[i,j].anchor_point, touch.location
                    )  and self.grid[i,j].enable_touch:
                self.block_action(i, j)
                return

class MyScene(scene.Scene):
    def setup(self):
        self.gridofblocks = GridOfBlocks(8, 8,
            position=(self.size[0]/2, self.size[1]/2),
            size=(8*64, 8*64),
            parent=self,
            font_name='arialms',
            color=(0, 255, 0, 255))

    def touch_began(self, touch):
        self.gridofblocks.touch_began(touch)

scene.run(MyScene(), show_fps=True)
