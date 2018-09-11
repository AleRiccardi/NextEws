# coding=UTF-8
from setuptools import find_packages, setup

"""
*************************
    To be fixed
*****************

Setup configuration.
To install your application (ideally into a virtualenv) just run 
the setup.py script with the install parameter. It will install 
your application into the virtualenv’s site-packages folder and 
also download and install all dependencies.

$ python setup.py install

If you are developing on the package and also want the requirements 
to be installed, you can use the develop command instead:

$ python setup.py develop

@author:    Alericcardi
@version:   1.0.0
"""

setup(
    name='nextews',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'sqlalchemy',
        'tensorflow',
        'keras',
        'nltk',
        'pandas',
        'numpy',
        'newsapi-python',
        'requests',
        'click'
    ],
)
