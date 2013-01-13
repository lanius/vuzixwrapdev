# -*- coding: utf-8 -*-

import argparse

import vuzixwrapdev


def display_angles(device):
    angles = device.get_angles()  # yaw, pitch, roll
    print('yaw: {0:3}, pitch: {1:3}, roll: {2:3}'.format(*angles))


def display_angles_forever(device):
    while (1):
        display_angles(device)


def display_recorded_angles(filepath):
    with vuzixwrapdev.helper.reader(filepath).opening() as device:
        display_angles_forever(device)


def display_mock_device_angles():
    with vuzixwrapdev.mock.opening() as device:
        display_angles_forever(device)


def display_device_angles():
    with vuzixwrapdev.opening() as device:
        display_angles_forever(device)


def main():
    description = 'Display angles received from a device'
    parser = argparse.ArgumentParser(description)
    parser.add_argument('-r', '--real', dest='use_real_device',
                        action='store_true', help='use the real device')
    parser.add_argument('-m', '--mock', dest='use_mock',
                        action='store_true', help='use the mock device')
    parser.add_argument('-f', '--file', dest='filepath',
                        help='use the file')
    parser.add_argument('-d', '--duration', dest='duration_sec',
                        help='specify duration seconds to send data')
    args = parser.parse_args()

    if args.use_real_device:
        print('Use the real device.')
        display_device_angles()
    elif args.use_mock:
        print('Use the mock device.')
        display_mock_device_angles()
    elif args.filepath:
        print('Use file: {0}'.format(args.filepath))
        display_recorded_angles(args.filepath)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
