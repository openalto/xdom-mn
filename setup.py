#!/usr/bin/env python2

from setuptools import setup
from os import path, listdir


def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


def files(dirname):
    return [path.join(dirname, filename) for filename in listdir(dirname)]


setup(
    name='xdommn',
    version='0.2',
    description='Mininet extension for cross-domain simulation.',
    url='https://github.com/openalto/xdom-mn',
    author='Y.Jace Liu, Jensen Zhang',
    author_email='yang.jace.liu@linux.com, hack@jensen-zhang.site',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Emulators",
    ],
    license='MIT',
    long_description=read('README.rst'),
    packages=['xdommn'],
    scripts=files('bin'),
    zip_safe=False,
)
