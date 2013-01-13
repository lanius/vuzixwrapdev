# -*- coding: utf-8 -*-

import argparse
from socket import socket, AF_INET, SOCK_DGRAM
from datetime import datetime

import vuzixwrapdev


def build_sender_func(address):
    sock = socket(AF_INET, SOCK_DGRAM)

    def sender_func(data):
        sock.sendto(data, address)
    return sender_func


def send_angles(device, sender_func, duration_sec=0):
    start = datetime.now()
    while (1):
        angles = device.get_angles()
        data = ','.join(map(str, angles))  # data is yaw,pitch,roll
        sender_func(data)

        if duration_sec and ((datetime.now() - start).seconds > duration_sec):
            break


def send_recorded_angles(filepath, sender_func, duration_sec=0):
    with vuzixwrapdev.helper.reader(filepath).opening() as device:
        send_angles(device, sender_func, duration_sec)


def send_mock_device_angles(sender_func, duration_sec=0):
    with vuzixwrapdev.mock.opening() as device:
        send_angles(device, sender_func, duration_sec)


def send_device_angles(sender_func, duration_sec=0):
    with vuzixwrapdev.opening() as device:
        send_angles(device, sender_func, duration_sec)


def run(exec_func, hostname, port, duration_sec=0):
    address = (hostname, port)
    print('Send data to {0}...'.format(':'.join(map(str, address))))
    sender_func = build_sender_func(address)
    exec_func(sender_func, duration_sec)


def main():
    description = 'Send angles by UDP'
    parser = argparse.ArgumentParser(description)
    parser.add_argument('target', metavar='HOSTNAME:PORT', nargs='?',
                        default='localhost:8080',
                        help='specify the host name and the port number.')
    parser.add_argument('-r', '--real', dest='use_real_device',
                        action='store_true', help='use the real device')
    parser.add_argument('-m', '--mock', dest='use_mock',
                        action='store_true', help='use the mock device')
    parser.add_argument('-f', '--file', dest='filepath',
                        help='use the file')
    parser.add_argument('-d', '--duration', dest='duration_sec',
                        help='specify duration seconds to send data')
    args = parser.parse_args()

    hostname, port_str = args.target.split(':')
    port = int(port_str)
    duration_sec = int(args.duration_sec) if args.duration_sec else 0

    if args.use_real_device:
        print('Use the real device.')
        run(send_device_angles, hostname, port, duration_sec)
    elif args.use_mock:
        print('Use the mock device.')
        run(send_mock_device_angles, hostname, port, duration_sec)
    elif args.filepath:
        print('Use file: {0}'.format(args.filepath))

        def exec_with_file(sender_func, duration_sec):
            send_recorded_angles(args.filepath, sender_func, duration_sec)

        run(exec_with_file, hostname, port, duration_sec)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
