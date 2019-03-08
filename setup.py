from setuptools import setup, find_packages
from ignore import __version__

setup(
    name='ignore-file',
    version=__version__,
    description='Ignore glob-style patterns similar to .gitignore and .dockerignore.',
    author='Simo Tumelius',
    author_email='simo.tumelius@gmail.com',
    url='https://github.com/smomni/ignore-file',
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'dev': [],
        'test': ['pytest', 'pytest-datadir'],
        'docs': []
    },
    scripts=[]
)