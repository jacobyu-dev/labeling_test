from setuptools import setup

import labeling_lib

setup(
    name='ypolaris_ai_labeling_tool',
    version='0.0.1',
    description='ypolaris image labeling tool',
    url='',
    packages=['labeling_lib'],
    install_require=[
        'opencv-python>=4.5.1.48'
    ]
)