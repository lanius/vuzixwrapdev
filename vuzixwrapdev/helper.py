# -*- coding: utf-8 -*-

"""
Provides helpers that writes and reads records.

writer and reader handle vzrec format file.

vzrec format:

    int:yaw, int:pitch, int:roll, float:interval(seconds from previous)
"""

from contextlib import contextmanager
from os import path
from time import sleep


class writer(object):

    def __init__(self, filepath):
        @contextmanager
        def opening():
            device = WriterDevice(filepath)
            try:
                device.open()
                yield device
            finally:
                device.close()
        self.opening = opening


class reader(object):

    def __init__(self, filepath):
        @contextmanager
        def opening():
            if not path.exists(filepath):
                raise IOError('{0} does not exist.'.format(filepath))
            device = ReaderDevice(filepath)
            try:
                device.open()
                yield device
            finally:
                device.close()
        self.opening = opening


class AbstractDevice(object):

    mode = 'r'

    def __init__(self, filepath):
        self.filepath = filepath

    def open(self):
        self.f = open(self.filepath, self.mode)
        return self

    def close(self):
        self.f.close()


class WriterDevice(AbstractDevice):

    mode = 'w'

    def write(self, angles, interval):
        data = ','.join(map(str, list(angles) + [interval]))
        self.f.write('{0}\n'.format(data))


class ReaderDevice(AbstractDevice):

    def get_angles(self):
        record = self.f.readline().strip()
        if not record:
            raise IOError('EOF of {0}'.format(self.filepath))
        yaw, pitch, roll, interval = record.split(',')
        sleep(float(interval))
        return int(yaw), int(pitch), int(roll)
