from setuptools import setup, find_packages

setup(
    name='EM-TEST',  # Replace with your project name
    version='0.1.0',  # Replace with your current project version
    description='Data validation for EM-DAT datasets.',
    # Short description about your project
    url='https://github.com/em-dat/EM-TEST',
    # Replace with the url of your project
    author='Damien Delforge',  # Replace with your name
    author_email='damien.delforge@uclouvain.be',
    # Replace with your email address
    classifiers=[  # Optional, refer to: https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    packages=find_packages(exclude=['tests']),
    # Using find_packages to discover project packages automatically
    python_requires='>=3.11, <4',
    # You can specify the python version your project supports
    install_requires=[  # List your project dependencies here
        'openpyxl~=3.1',
        'pandas~=2.2',
        'pandera~=0.20',
    ],
)