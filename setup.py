"""Minimal setup file for DcentralLab."""

from setuptools import find_packages, setup
from pathlib import Path

req_location = Path().absolute().joinpath('requirements.txt')

with open(req_location) as f:
    required = f.read().splitlines()

setup(
    name='DcentralLab',
    version='0.1.0',
    description='DcentralLab testing',
    packages=find_packages('tests'),
    package_dir={'': 'tests'},
    package_data={
        "cfg.cfg_global": ["*.json"],
        "cfg.cfg_tests": ["*.json"]
    },

    # metadata
    author='Efi Ovadia',
    author_email='efovadia@gmail.com',
    license='proprietary',
    install_requires=required
)
