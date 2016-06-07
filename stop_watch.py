from __future__ import division
import scene
from time import localtime

class StopWatch(scene.LabelNode):
    def __init__(self, text, *args, **kwargs):
        super(StopWatch, self).__init__(text, *args, **kwargs)
        self.value = 0

    def update(self):
        if scene.scene_obj.state == 'run':
            self.value += 1
            v = (self.value//(3600*60), self.value//3600, self.value//60)
            t = (v[0], v[1]%60, v[2]%60)
            self.text = "{:02}:{:02}:{:02}".format(*t)

class MyScene(scene.Scene):
    def setup(self):
        self.stop_watch = StopWatch("", parent=self)
        self.state = 'run'

    def update(self):
        self.stop_watch.update()
        
    def touch_began(self, touch):
        if self.state == 'run':
            self.state = 'stop'
        elif self.state == 'stop':
            self.state = 'run'
            self.stop_watch.value = 0

scene.run(MyScene())
