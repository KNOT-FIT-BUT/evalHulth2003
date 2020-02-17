#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""""
Created on 17.02.20
Script for evaluation of your results on Hulth 2003 (inspec) keywords dataset.

:author:     Martin Dočekal
"""

from distutils.core import setup

setup(name='evalHulth2003',
    version='1.0.0',
    description='Script for evaluation of your results on Hulth 2003 (inspec) keywords dataset.',
    author='Martin Dočekal',
    packages=['evalhulth2003', 'tests'],
    entry_points={
        'console_scripts': [
            'evalhulth2003 = evalhulth2003.__main__:main'
        ]
    },
    install_requires=[
        #TODO
        'pandas>=0.23',
        'scikit_image>=0.15',
        'setuptools>=39.0',
        'scipy>=1.2',
        'numpy>=1.16',
        'typing>=3.6',
        'PySide2>=5.12',
        'scikit_learn>=0.20'
    ]
)
