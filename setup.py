from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='emtest',
    version='2024.12.0',
    description='Data validation for EM-DAT datasets.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/em-dat/em-test',
    author='Damien Delforge, Valentin Wathelet',
    author_email='damien.delforge@uclouvain.be',
    classifiers=[  # Optional, refer to: https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='EM-DAT, data validation, disaster database',
    packages=find_packages(exclude=['tests', 'examples']),
    include_package_data=True,
    python_requires='>=3.11, <4',
    install_requires=[
        'openpyxl~=3.1',
        'pandas~=2.2',
        'pandera~=0.20',
    ],
    package_data={
        'emtest': [
            'validation_data/*.csv',
            'validation_data/*.toml',
            'validation_data/*.txt',
            'validation_data/*.py'
        ],
    },
)
