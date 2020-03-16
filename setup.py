import os
import sys
from setuptools import find_packages, setup

# Validate Python Version
CURRENT_PYTHON  = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of pytomation requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


setup(
    name='pytomation',
    version=1.0,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    author='Matheus Trevisan Moreira',
    author_email='matheus.trev@gmail.com',
    packages=find_packages(where=os.path.dirname(os.path.abspath(__file__))),
    install_requires = [ ]
)
