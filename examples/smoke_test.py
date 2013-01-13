# -*- coding: utf-8 -*-

import argparse
import os
import unittest

import vuzixwrapdev

#import calibration  # can't be tested yet
import display
import recording
import transmission


class BaseDeviceTestCase(unittest.TestCase):

    record_file = 'test_record.vzrec'
    address = ('localhost', 8080)  # for UDP testing, server is unnecessary

    def setUp(self):
        #self.device = #  override and implement open process
        pass

    def tearDown(self):
        self.device.close()

    def test_display(self):
        display.display_angles(self.device)
        self.assertTrue(True)

    def test_recording(self):
        recording.record_angles(self.device, self.record_file, 1)
        if os.path.exists(self.record_file):
            self.assertTrue(True)
            os.remove(self.record_file)

    def test_transmission(self):
        sender = transmission.build_sender_func(self.address)
        transmission.send_angles(self.device, sender, 1)
        self.assertTrue(True)


class MockDeviceTestCase(BaseDeviceTestCase):

    def setUp(self):
        self.device = vuzixwrapdev.mock.open()


class RealDeviceTestCase(BaseDeviceTestCase):

    dll = None  # use default

    def setUp(self):
        if self.dll:
            self.device = vuzixwrapdev.open(self.dll)
        else:
            self.device = vuzixwrapdev.open()


class ReaderDeviceTestCase(BaseDeviceTestCase):

    input_file = 'test_input_record.vzrec'

    def setUp(self):
        with vuzixwrapdev.mock.opening() as device:
            recording.record_angles(device, self.input_file, 1)
        self.device = vuzixwrapdev.helper.ReaderDevice(self.input_file).open()

    def tearDown(self):
        BaseDeviceTestCase.tearDown(self)
        os.remove(self.input_file)


def suite_and_loader():
    return unittest.TestSuite(), unittest.TestLoader()


def suite(dll_file=None):
    suite, loader = suite_and_loader()
    RealDeviceTestCase.dll = dll_file
    suite.addTests(loader.loadTestsFromTestCase(RealDeviceTestCase))
    suite.addTests(loader.loadTestsFromTestCase(MockDeviceTestCase))
    suite.addTests(loader.loadTestsFromTestCase(ReaderDeviceTestCase))
    return suite


def suite_mock():
    print('Use mock device only (not the real device).')
    suite, loader = suite_and_loader()
    suite.addTests(loader.loadTestsFromTestCase(MockDeviceTestCase))
    suite.addTests(loader.loadTestsFromTestCase(ReaderDeviceTestCase))
    return suite


def main():
    description = 'Run smoke test'
    parser = argparse.ArgumentParser(description)
    parser.add_argument('-m', '--mock', dest='mock_only',
                        action='store_true', help='use mock device only')
    parser.add_argument('-d', '--dll', dest='dll_file',
                        help='specify dll file path for using real device')
    args = parser.parse_args()

    runner = unittest.TextTestRunner(verbosity=2)
    if args.mock_only:
        runner.run(suite_mock())
    else:
        runner.run(suite(args.dll_file))


if __name__ == '__main__':
    main()
