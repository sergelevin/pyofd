from setuptools import setup, find_packages
from os.path import join, dirname
import codecs
from aiopyofd import __version__

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]

with codecs.open('README.rst', 'r', 'utf-8') as readme:
    long_description = readme.read()

setup(
    name='aiopyofd',
    description='OFD providers interface with asyncio support',
    version=__version__,
    license='MIT',
    author='Serge A. Levin',
    author_email='serge.levin.spb@gmail.com',
    platforms="Posix; MacOS X; Windows",
    packages=[
        'aiopyofd',
        'aiopyofd.providers'
    ],
    long_description=long_description,
    classifiers=classifiers,
    install_requires=[
        "lxml >= 3.7.0",
        "aiohttp"
    ],
    test_suite='test',
    zip_safe=False,
)
