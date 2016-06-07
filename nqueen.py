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
        self.label.text = ""

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
                t =  text_list[i*self.n+(j)] # utf8.char(i*self.n+j+9812)
                v =  value_list[i*self.n+(j)] # utf8.char(i*self.n+j+9812)
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

class NQueenGridOfBlocks(GridOfBlocks):
    def __init__(self, m, n,
                 position=(0,0),
                 size=(400, 400),
                 marginx=2,
                 marginy=2,
                 parent=None,
                 **kwargs):
        self.text_list = [u'♛']*(m*n)
        self.value_list = [0]*(m*n)
        super(NQueenGridOfBlocks, self).__init__(m, n,
                         position=position,
                         size=size,
                         marginx=marginx,
                         marginy=marginy,
                         parent=parent,
                         text_list=self.text_list,
                         value_list=self.value_list,
                         **kwargs);

    def disable_attacking_positions(self, i, j):
        for p in range(self.m):
            self.grid[i, p].enable_touch = False
            self.grid[p, j].enable_touch = False
        for p in range(-7, 8):
            if (i+p, j+p) in self.grid:
                self.grid[i+p, j+p].enable_touch = False
            if (i+p, j-p) in  self.grid:
                self.grid[i+p, j-p].enable_touch = False

    def initialize(self):
        self.count = 0
        for i in range(self.m):
            for j in range(self.n):
                self.grid[i,j].enable_touch = True
                #self.grid[i,j].node.text = u'♛'
                self.grid[i,j].hide()

    def block_action(self, i, j):
        block = self.grid[i,j]
        block.reveal()
        self.disable_attacking_positions(i,j)
        self.count += 1
        if self.count == self.m:
            self.parent.state.set_win_state()
            return
        if not any(self.grid[p,q].enable_touch for p in range(self.m) for q in range(self.m)):
            self.parent.state.set_lose_state()
            return

class State(object):
    def __init__(self, position=(0, 0), parent=None):
        self.value = 'play'
        self.msg = 'Play'
        self.parent = parent
        self.label = scene.LabelNode(self.msg,
                    position=position,
                    parent=parent)

    def set_win_state(self):
        self.value = 'win'
        self.msg = 'You win'
        self.label.text = self.msg

    def set_lose_state(self):
        self.value = 'lose'
        self.msg = 'You lose'
        self.label.text = self.msg

    def initialize(self):
        self.set_play_state()

    def set_play_state(self):
        self.value = 'play'
        self.msg = 'Play '
        self.label.text = self.msg

class MyScene(scene.Scene):
    def initialize(self):
        self.state.initialize()
        self.gridofblocks.initialize()

    def setup(self):
        self.state = State(position=(self.size[0]/2, 50), parent=self)
        self.gridofblocks = NQueenGridOfBlocks(8, 8,
            position=(self.size[0]/2, self.size[1]/2),
            size=(8*64, 8*64),
            parent=self,
            font_name='arialms',
            color=(0, 255, 0, 255))
        self.initialize()

    def touch_began(self, touch):
        if self.state.value == 'win' or self.state.value == 'lose':
            self.initialize()
            return
        self.gridofblocks.touch_began(touch)

scene.run(MyScene(), show_fps=True)
