import os
from setuptools import setup, find_packages


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='ConcurrentPandas',
    version='0.1.2',
    description='Download data using pandas with multi-threading and multi-processing.',
    long_description=(read('README.md') + '\n\n' +
                      read('AUTHORS.rst')) + '\n\n',
    url='https://github.com/briwilcox/Concurrent-Pandas',
    license='Apache Software License',
    author='Brian Wilcox',
    py_modules=['concurrentpandas'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],


    packages = find_packages(),
    scripts = ['concurrentpandas.py', 'benchmark.py', 'LICENSE', 'README.md', 'AUTHORS.rst'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [
        'Quandl',
        'pandas>=0.16.0',
        'BeautifulSoup4'
    ],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', 'LICENSE', 'README.md'],
    },

    # metadata for upload to PyPI
    keywords = "Panda, Pandas, DataFrame, Data Frame, Analysis, ",

)


