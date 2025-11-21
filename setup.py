from setuptools import setup, find_packages

setup(
    name='axpm',
    version='0.4.9',
    packages=find_packages(),
    requires=['requests'],
    entry_points={
        'console_scripts':[
            'axpm=_axpm.main:work'
        ]
    }
)
