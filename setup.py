"""A setup module for prancer-enterprise."""


# setuptools for distribution
from setuptools import find_packages, setup
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

LONG_DESCRIPTION = """
 Prancer Enterprise allows to users to run cloud validation using
 web APIs and allows notifications to be posted to the user as configured.
 The supported cloud frameworks are azure, aws and git.
"""

setup(
    name='prancer-enterprise',
    version='0.1.0',
    description='Prancer Enterprie, http://prancer.io/',
    long_description=LONG_DESCRIPTION,
    license = "Propietary",
    # The project's main homepage.
    url='https://ebizframework.visualstudio.com/whitekite',
    # Author(s) details
    author='Farshid M/Ajey Khanapuri',
    author_email='ajey.khanapuri@liquware.com',
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "License :: OSI Approved :: BSD License",
    ],
    packages=find_packages(where="enterprise",
                           exclude=['log', 'rundata', 'utilities', 'tests']),
    include_package_data=True,
    package_dir={'': 'enterprise'},
    setup_requires=['ply==3.10'],
    install_requires=required,
    python_requires='>=3.0'
)

