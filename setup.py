#!/usr/bin/env python3

import shutil
from pathlib import Path

from setuptools import setup, find_packages


def _copy_assemblers():

    assemblers = Path(__file__) / 'assemblers/'
    config_dir = Path.home() / '.local' / 'share' / 'qanda'

    config_dir.mkdir(parents=True, exist_ok=True)

    for assembler_config in assemblers.glob("*.json"):

        shutil.copy(str(assembler_config),
                    str(config_dir))


setup(
    name='qanda',
    version='0.1',
    packages=find_packages(),
    install_requires=['pandas'],
    package_data={
        'assemblers': ['*.json']
    },
    url='https://github.com/dorbarker/qanda',
    license='GPL-3+',
    author='Dillon O.R. Barker',
    author_email='dillon.barker@canada.ca',
    description='Query NCBI, Download, and Assemble',
    entry_points={
        'console_scripts': [
            'qanda = qanda.qanda:main'
        ]
    }
)

_copy_assemblers()
