"""
fantasyreport python package configuration.

"""

from setuptools import setup

setup(
    name='fantasyReport',
    version='0.1.0',
    packages=['fantasyReport'],
    include_package_data=True,
    install_requires=[
        'bs4==0.0.1',
        'Flask==1.1.1',
        'html5validator==0.3.1',
        'pycodestyle==2.5.0',
        'pydocstyle==4.0.1',
        'pylint==2.3.1',
        'pytest==5.1.2',
        'requests==2.22.0',
        'sh==1.12.14',
    ],
)
