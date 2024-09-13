from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='EM-TEST',
    version='2024.09.13',
    description='Data validation for EM-DAT datasets.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/em-dat/EM-TEST',
    author='Damien Delforge',
    author_email='damien.delforge@uclouvain.be',
    classifiers=[  # Optional, refer to: https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='EM-DAT, data validation, disaster database',
    packages=find_packages(exclude=['tests', 'examples']),
    python_requires='>=3.11, <4',
    install_requires=[
        'openpyxl~=3.1',
        'pandas~=2.2',
        'pandera~=0.20',
    ],
)
