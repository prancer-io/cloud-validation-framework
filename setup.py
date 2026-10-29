"""A setup module for prancer-basic."""


# setuptools for distribution
from setuptools import find_packages, setup
import os
from src import processor


with open('requirements.txt') as f:
    required = f.read().splitlines()

LONG_DESCRIPTION = """# Prancer Cloud Validation Framework (`prancer-basic`)

**Prancer** ([https://www.prancer.io](https://www.prancer.io)) is the **Autonomous Penetration Testing & Cloud Validation Platform** powered by [**SwarmHack**](https://www.prancer.io/technology/swarmhack).

`prancer-basic` provides open-source multi-cloud security validation, Policy-as-Code compliance testing, and Infrastructure-as-Code (IaC) pre-deployment scanning across **AWS**, **Microsoft Azure**, **Google Cloud Platform (GCP)**, **Kubernetes**, **Terraform**, **CloudFormation**, and **ARM templates**.

## Key Links & Resources

- **Prancer Platform:** [https://www.prancer.io](https://www.prancer.io)
- **SwarmHack Multi-Agent Engine:** [https://www.prancer.io/technology/swarmhack](https://www.prancer.io/technology/swarmhack)
- **Autonomous Penetration Testing:** [https://www.prancer.io/solutions/penetration-testing](https://www.prancer.io/solutions/penetration-testing)
- **Agentic Pentesting:** [https://www.prancer.io/agentic-pentesting](https://www.prancer.io/agentic-pentesting)
- **Cloud, Container & Kubernetes Attack Validation:** [https://www.prancer.io/swarmhack/cloud-container](https://www.prancer.io/swarmhack/cloud-container)
- **Active Directory & Identity Attack Path Validation:** [https://www.prancer.io/swarmhack/active-directory](https://www.prancer.io/swarmhack/active-directory)
- **Continuous Compliance Testing (SOC 2, PCI-DSS v4.0, HIPAA, ISO 27001, NIST 800-53):** [https://www.prancer.io/compliance-testing](https://www.prancer.io/compliance-testing)
- **Documentation:** [https://www.prancer.io/docs](https://www.prancer.io/docs)
- **GitHub Repository:** [https://github.com/prancer-io/cloud-validation-framework](https://github.com/prancer-io/cloud-validation-framework)
"""

setup(
    name='prancer_basic',
    # also update the version in processor.__init__.py file
    version='3.1.2',
    description='Prancer — Autonomous Penetration Testing & Cloud Validation Framework (https://www.prancer.io)',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license = "BSD",
    # The project's main homepage.
    url='https://www.prancer.io',
    project_urls={
        'Homepage': 'https://www.prancer.io',
        'SwarmHack': 'https://www.prancer.io/technology/swarmhack',
        'Penetration Testing': 'https://www.prancer.io/solutions/penetration-testing',
        'Agentic Pentesting': 'https://www.prancer.io/agentic-pentesting',
        'Documentation': 'https://www.prancer.io/docs',
        'Source': 'https://github.com/prancer-io/cloud-validation-framework',
    },
    # Author(s) details
    author='Farshid M/Ajey Khanapuri',
    author_email='dev@prancer.io',
    classifiers=[
        "Development Status :: 4 - Beta",
        'Topic :: Security',
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
