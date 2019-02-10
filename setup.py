"""A setup module for prancer-basic."""


# setuptools for distribution
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

LONG_DESCRIPTION = """
 Prancer Basic allows to users to run cloud validation.
 The supported cloud frameworks are azure, aws and git.
"""

setup(
    name='Prancer-Basic',
    version='1.0.0',
    description='Prancer Basic, http://prancer.io/',
    long_description=LONG_DESCRIPTION,
    license = "BSD",
    # The project's main homepage.
    url='https://github.com/prancer-io/cloud-validation-framework',
    # Author(s) details
    author='Farshid M/Ajey Khanapuri',
    author_email='ajey.khanapuri@liquware.com',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Cloud Validation Framework",
        "License :: OSI Approved :: BSD License",
    ],
    packages=find_packages(where="processor",
                           exclude=['realm', 'log', 'rundata', 'utilities', 'tests']),
    scripts=['validator.py'],
    package_dir={'': 'processor'},
    install_requires=required,
    python_requires='>=3.0'
)

