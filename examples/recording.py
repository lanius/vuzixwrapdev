# -*- coding: utf-8 -*-

import argparse
from datetime import datetime

import vuzixwrapdev


def record_angles(device, filepath, duration_sec=0):
    # if duration_sec is 0, it run forever
    with vuzixwrapdev.helper.writer(filepath).opening() as writer:
        start = datetime.now()
        previous = start
        while (1):
            angles = device.get_angles()  # yaw, pitch, roll

            current = datetime.now()
            delta = (current - previous)
            interval = delta.seconds + (delta.microseconds / 1000000.)

            writer.write(angles, interval)

            previous = current

            if duration_sec and ((current - start).seconds > duration_sec):
                break


def record_mock_device_angles(filepath, duration_sec=0):
    with vuzixwrapdev.mock.opening() as device:
        record_angles(device, filepath, duration_sec)


def record_device_angles(filepath, duration_sec=0):
    with vuzixwrapdev.opening() as device:
        record_angles(device, filepath, duration_sec)


def main():
    description = 'Record angles to vzrec format file'
    parser = argparse.ArgumentParser(description)
    parser.add_argument('-f', '--file', dest='filepath',
                        help='specify file path for saving records')
    parser.add_argument('-d', '--duration', dest='duration_sec',
                        help='specify duration seconds to record')
    parser.add_argument('-r', '--real', dest='use_real_device',
                        action='store_true', help='use the real device')
    parser.add_argument('-m', '--mock', dest='use_mock',
                        action='store_true', help='use the mock device')
    args = parser.parse_args()

    filepath = args.filepath or datetime.now().strftime('%Y%m%d%H%M%S.vzrec')
    duration_sec = int(args.duration_sec) if args.duration_sec else 0

    print('Record to {0}'.format(filepath))

    if duration_sec:
        print('{0} seconds'.format(duration_sec))
    else:
        print('Forever.')

    if args.use_real_device:
        print('Use the real device.')
        record_device_angles(filepath, duration_sec)
    elif args.use_mock:
        print('Use the mock device.')
        record_mock_device_angles(filepath, duration_sec)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
