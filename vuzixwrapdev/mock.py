# -*- coding: utf-8 -*-

"""
Provides mock object for vuzixwrapdev module.
"""

from contextlib import contextmanager
from random import randint
from time import sleep


def open(dll=None):
    device = VuzixWrapDevice(dll)
    device.open()
    return device


@contextmanager
def opening(dll=None):
    device = open(dll)
    try:
        yield device
    finally:
        device.close()


class VuzixWrapDevice(object):

    def __init__(self, _):
        self.yaw = RandomAngle(-180, 180)
        self.pitch = RandomAngle(-90, 90)
        self.roll = RandomAngle(-180, 180)

    def open(self):
        pass

    def close(self):
        pass

    def get_angles(self):
        sleep(0.01)
        return self.yaw.next(), self.pitch.next(), self.roll.next()

    def zero_set(self):
        pass

    def begin_calibrate(self):
        pass

    def end_calibrate(self, save=True):
        pass


class RandomAngle(object):

    def __init__(self, min=-180, max=180, start=0, step_min=-2, step_max=2):
        self.min = min
        self.max = max
        self.angle = start
        self.step_min = step_min
        self.step_max = step_max

    def next(self):
        value = self.angle + randint(self.step_min, self.step_max)
        self.angle = max(self.min, min(value, self.max))
        return self.angle
