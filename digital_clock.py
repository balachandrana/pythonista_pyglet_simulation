from __future__ import division
import scene
from time import localtime

class DigitalClock(scene.LabelNode):
    def __init__(self, text, *args, **kwargs):
        super(DigitalClock, self).__init__(text, *args, **kwargs)

    def update(self):
        t = localtime()
        self.text = "{:02}:{:02}:{:02}".format(
                                 t.tm_hour, t.tm_min, t.tm_sec)

class MyScene(scene.Scene):
    def setup(self):
        self.digital_clock = DigitalClock("", parent=self)

    def update(self):
        self.digital_clock.update()

scene.run(MyScene())
