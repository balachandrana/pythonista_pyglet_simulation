# coding: utf-8
# slider puzzle  - https://en.wikipedia.org/wiki/Sliding_puzzle
#

from __future__ import division
import scene
import pyglet
import random

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
        self.text = str(self.value) if value else ' '

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

class SliderGridOfBlocks(GridOfBlocks):
    def __init__(self, m, n,
                 position=(0,0),
                 size=(400, 400),
                 marginx=2,
                 marginy=2,
                 parent=None,
                 **kwargs):
        self.text_list = [str(i*n+j+1) for i in range(m)  for j in range(n)]
        self.value_list = [i*n+j+1 for i in  range(m)  for j in range(n)]
        ''' neighbor table help
          0  1  2  3
          4  5  6  7
          8  9 10 11
         12 13 14 15'''
        self.neighbors_table = [[(1,4),(0,2,5),(1,3,6),(2,7)],
            [(0,5,8), (1,4,6,9), (2,5,7,10), (3,6,11)],
            [(4,9,12), (5,8,10,13), (6,9,11,14), (7,10,15)],
            [(8,13), (9,12,14), (10,13,15), (11,14)]]
        super(SliderGridOfBlocks, self).__init__(m, n,
                         position=position,
                         size=size,
                         marginx=marginx,
                         marginy=marginy,
                         parent=parent,
                         text_list=self.text_list,
                         value_list=self.value_list,
                         **kwargs);
        self.grid[3,3].value = 0
        self.grid[3,3].label.text = ''

    def initialize(self):
        pass
        p1, q1 = (3, 3)
        for r in range(self.m * self.n*10):
            r = random.choice(self.neighbors_table[p1][q1])
            p2, q2 = divmod(r, self.n)
            self.exchange(p1, q1, p2, q2)
            p1, q1 = p2, q2

    def check_win(self):
        count = 1
        for i in range(self.m):
            for j in range(self.n):
                if (i == 3) and(j == 3):
                    # no need to check this value (blank value)
                    break
                if self.grid[i, j].value != count:
                    return False
                else:
                    count += 1
        return True

    def exchange(self, i, j, p, q):
        self.grid[i, j].label.text, self.grid[p, q].label.text = self.grid[p, q].label.text, self.grid[i, j].label.text
        self.grid[i, j].value, self.grid[p, q].value = self.grid[p, q].value, self.grid[i, j].value

    def block_action(self, i, j):
        for r in self.neighbors_table[i][j]:
            p, q = divmod(r, self.n)
            if self.grid[p, q].value == 0:
                self.exchange(i, j, p, q)
                if self.check_win():
                    self.parent.state.set_win_state()
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
        self.state = State(position=(self.size[0]/2, 100), parent=self)
        self.gridofblocks = SliderGridOfBlocks(4, 4,
            position=(self.size[0]/2, self.size[1]/2),
            size=(96*4, 96*4),
            parent=self,
            color=(0,255,0,255))
        self.initialize()

    def touch_began(self, touch):
        if self.state.value == 'win':
            self.initialize()
            return
        self.gridofblocks.touch_began(touch)

scene.run(MyScene(), show_fps=True)
