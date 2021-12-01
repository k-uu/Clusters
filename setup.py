from setuptools import setup, find_packages


setup(
    name='clusters',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy~=1.20.3',
        'scipy~=1.7.1',
        'matplotlib~=3.4.3',
        'click~=8.0.3',
        'setuptools~=57.0.0'
    ],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'clusters = clusters.script:cli',
        ],
    },
)
