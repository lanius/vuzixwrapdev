# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='vuzixwrapdev',
    version='0.0.1',
    url='https://github.com/lanius/vuzixwrapdev/',
    license='MIT',
    author='lanius',
    author_email='lanius@nirvake.org',
    description='vuzixwrapdev provides python APIs '
                'for the Vuzix Wrap devices.',
    long_description=open('README.rst').read(),
    packages=['vuzixwrapdev'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
