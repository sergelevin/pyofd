from setuptools import setup, find_packages
from os.path import join, dirname
import codecs
from pyofd import __version__

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]

with codecs.open('README.rst', 'r', 'utf-8') as readme:
    long_description = readme.read()

setup(
    name='pyofd',
    description='OFD providers interface',
    version=__version__,
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
