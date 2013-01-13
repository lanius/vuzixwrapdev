# -*- coding: utf-8 -*-

"""
Provides wrapper for Vuzix SDK C APIs.
"""

from contextlib import contextmanager
from ctypes import cdll, CDLL, c_long, c_int, c_bool, byref
from functools import wraps


ERROR_SUCCESS = 0
ERROR_DEV_NOT_EXIST = 55
#ERROR_NOT_ENOUGH_MEMORY =
#ERROR_NOT_SUPPORTED =

ERRORS = {
    ERROR_DEV_NOT_EXIST: 'A device does not exist.'
}

DLL = 'iweardrv'


def open(dll=DLL):
    device = VuzixWrapDevice(load_dll(dll))
    device.open()
    return device


@contextmanager
def opening(dll=DLL):
    device = open(dll)
    try:
        yield device
    finally:
        device.close()


def load_dll(dll):
    try:
        cdll.LoadLibrary(dll)
    except WindowsError:
        raise VuzixWrapError('A dll file is not found.')
    return CDLL(dll)


class VuzixWrapDevice(object):

    def __init__(self, lib):
        self.lib = lib
        self.lib.IWRGetFilterState.restype = c_bool

    def open(self):
        self.open_tracker()

    def close(self):
        self.close_tracker()

    def get_angles(self):
        yaw, pitch, roll = self.get_tracking()
        return yaw * 180 / 32768, pitch * 90 / 16384, roll * 180 / 32768

    def open_tracker(self):
        rc = self.lib.IWROpenTracker()
        self._check_error(rc)

    def close_tracker(self):
        self.lib.IWRCloseTracker()

    def zero_set(self):
        self.lib.IWRZeroSet()

    def set_filter_state(self, on):
        on_int = 1 if on else 0
        self.lib.IWRSetFilterSate(c_int(on_int))

    def get_filter_state(self):
        return self.lib.IWRGetFilterState()

    def begin_calibrate(self):
        rc = self.lib.IWRBeginCalibrate()
        self._check_error(rc)

    def end_calibrate(self, save=True):
        save_int = 1 if save else 0
        self.lib.IWREndCalibrate(c_int(save_int))

    def get_tracking(self):
        yaw = c_long()
        pitch = c_long()
        roll = c_long()
        rc = self.lib.IWRGetTracking(byref(yaw), byref(pitch), byref(roll))
        self._check_error(rc)
        return yaw.value, pitch.value, roll.value

    def get_6d_tracking(self):
        yaw = c_long()
        pitch = c_long()
        roll = c_long()
        xtrn = c_long()
        ytrn = c_long()
        ztrn = c_long()
        rc = self.lib.IWRGet6DTracking(
            byref(yaw), byref(pitch), byref(roll),
            byref(xtrn), byref(ytrn), byref(ztrn)
        )
        self._check_error(rc)
        return (
            yaw.value, pitch.value, roll.value,
            xtrn.value, ytrn.value, ztrn.value
        )

    def set_mag_auto_correct(self, on):
        on_int = 1 if on else 0
        self.lib.IWRSetMagAutoCorrect(c_int(on_int))

    def get_mag_yaw(self):
        myaw = c_long()
        rc = self.lib.IWRGetMagYaw(byref(myaw))
        self._check_error(rc)
        return myaw.value

    def get_sensor_data(self):
        #self.lib.IWRGetSensorData
        raise NotImplementedError()

    def get_filtered_sensor_data(self):
        ax = c_long()
        ay = c_long()
        az = c_long()
        lgx = c_long()
        lgy = c_long()
        lgz = c_long()
        gx = c_long()
        gy = c_long()
        gz = c_long()
        mx = c_long()
        my = c_long()
        mz = c_long()
        rc = self.lib.IWRGetFilteredSensorData(
            byref(ax), byref(ay), byref(az),
            byref(lgx), byref(lgy), byref(lgz),
            byref(gx), byref(gy), byref(gz),
            byref(mx), byref(my), byref(mz)
        )
        self._check_error(rc)
        return (
            ax.value, ay.value, az.value,
            lgx.value, lgy.value, lgz.value,
            gx.value, gy.value, gz.value,
            mx.value, my.value, mz.value
        )

    def _check_error(self, return_code):
        if return_code in ERRORS:
            raise VuzixWrapError(ERRORS[return_code])


class VuzixWrapError(Exception):
    pass
