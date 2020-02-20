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
        'nltk >= 3.2.5',
        'spacy == 2.0.11',
        'tqdm == 4.36.1'
    ]
)
