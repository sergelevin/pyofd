from setuptools import setup, find_packages
from os.path import join, dirname
import codecs

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
]

with codecs.open('README.rst', 'r', 'utf-8') as readme:
    long_description = readme.read()

setup(
    name='pyofd',
    description='OFD providers interface',
    version='0.0.1',
    license='MIT',
    author='Serge A. Levin',
    author_email='serge.levin.spb@gmail.com',
    platforms="Posix; MacOS X; Windows",
    packages=[
        'pyofd',
        'pyofd.providers'
    ],
    long_description=long_description,
    classifiers=classifiers,
    install_requires=[
        "lxml >= 3.7.0"
    ],
    test_suite='test',
    zip_safe=False,
)