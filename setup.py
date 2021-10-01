"""A setup module for prancer-basic."""


# setuptools for distribution
from setuptools import find_packages, setup
import os
from src import processor


with open('requirements.txt') as f:
    required = f.read().splitlines()

LONG_DESCRIPTION = """
 Prancer Basic allows to users to run cloud validation.
 The supported cloud frameworks are azure, aws and git.
"""

setup(
    name='prancer-basic',
    # also update the version in processor.__init__.py file
    version='2.0.1',
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
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "License :: OSI Approved :: BSD License",
    ],
    packages=find_packages(where="src",
                           exclude=['log', 'rundata', 'utilities', 'tests']),
    include_package_data=True,
    package_dir={'': 'src'},
    setup_requires=['ply==3.10'],
    install_requires=required,
    python_requires='>=3.0',
    entry_points={
        'console_scripts': [
            'validator = processor.helper.utils.cli_validator:validator_main',
            'prancer = processor.helper.utils.cli_validator:validator_main',
            'populate_json = processor.helper.utils.cli_populate_json:populate_json_main',
            'terraform_to_json = processor.helper.utils.cli_terraform_to_json:terraform_to_json_main',
            'register_key_in_azure_vault = processor.helper.utils.cli_generate_azure_vault_key:generate_azure_vault_key'
        ],
    }
)

