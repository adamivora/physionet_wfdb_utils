import setuptools

setuptools.setup(
    name='physionet_wfdb_utils',
    version='0.0.1',
    description='Utilities for working with Physionet databases',
    python_requires='>=3.7',
    packages=['physionet_wfdb_utils'],
    package_dir={'physionet_wfdb_utils': 'physionet_wfdb_utils'},
    install_requires=[
        'numpy',
        'wfdb',
        'torch',
    ]
)
