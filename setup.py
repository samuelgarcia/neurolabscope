# -*- coding: utf-8 -*-

from setuptools import setup
import os

long_description = open("README.rst").read()
import neurolabscope

setup(
    name = "neurolabscope",
    version = neurolabscope.__version__,
    packages = ['neurolabscope', ],
    install_requires=[
                    'numpy',
                    'pyzmq',
                    #~ 'gevent',
                    'msgpack-python',
                    ],
    author = "S.Garcia",
    author_email = "sgarcia at olfac.univ-lyon1.fr",
    description = "Acquisition for electrophysiological signals.",
    long_description = long_description,
    license = "BSD",
    url='https://github.com/samuelgarcia/neurolabscope',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering']
)



 
