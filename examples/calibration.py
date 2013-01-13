# -*- coding: utf-8 -*-

import argparse
from time import sleep

import vuzixwrapdev


def calibrate():
    with vuzixwrapdev.opening() as device:
        print('Calibration start presently. Move your head.')
        device.begin_calibrate()
        sleep(8)
        device.end_calibrate()
        print('Finished.')


def set_zero():
    with vuzixwrapdev.opening() as device:
        print('Set zero. Look forward.')
        sleep(3)
        device.zero_set()
        print('Finished.')


def main():
    description = 'Calibrate Vuzix Wrap device'
    parser = argparse.ArgumentParser(description)
    parser.add_argument('-c', '--calibrate', dest='calibrate',
                        action='store_true', help='run calibration')
    parser.add_argument('-z', '--setzero', dest='set_zero',
                        action='store_true', help='run set zero')
    args = parser.parse_args()

    if args.calibrate:
        calibrate()
    elif args.set_zero:
        set_zero()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
