What is this?
=============
vuzixwrapdev provides python APIs for the Vuzix Wrap devices (Vuzix Wrap 920VR or 1200VR).

Getting started
===============

Download and istall Vuzix SDK. vuzixwrapdev module requires iweardrv.dll file.

Download the archive, unzip it and run install command::

    setup.py install

Connect Wrap device to your PC with USB.

Now, you can get angles data:

.. code:: python

    import vuzixwrapdev

    dll_path = 'iweardrv.dll'

    with vuzixwrapdev.opening(dll_path) as device:
        yaw, pitch, roll = device.get_angles()
        print(yaw, pitch, roll)

See examples, that contain calibration, recording and other samples.

License
=======
vuzixwrapdev is licensed under the MIT Licence. See LICENSE for more details.
