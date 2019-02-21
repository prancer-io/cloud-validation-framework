"""A setup module for prancer-basic."""


# setuptools for distribution
from setuptools import find_packages, setup
import os

def package_data_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        fpaths = []  # All files in this path.
        for filename in filenames:
            fpaths.append(os.path.join(path, filename))
        paths.append((path, fpaths))
    return paths

extra_files = package_data_files('realm')
# print(extra_files)



with open('requirements.txt') as f:
    required = f.read().splitlines()

LONG_DESCRIPTION = """
 Prancer Basic allows to users to run cloud validation.
 The supported cloud frameworks are azure, aws and git.
"""

setup(
    name='Prancer-Basic',
    version='0.1.0',
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
    packages=find_packages(where="src",
                           exclude=['log', 'rundata', 'utilities', 'tests']),
    scripts=['utilities/populate_json', 'utilities/terraform_to_json',  'utilities/validator'],
    include_package_data=True,
    package_dir={'': 'src'},
    data_files=extra_files,
    setup_requires=['ply==3.10'],
    install_requires=required,
    python_requires='>=3.0'
)

