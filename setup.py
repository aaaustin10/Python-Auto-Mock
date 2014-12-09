import os

from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='pythonAutoMock',
    version='0.1.0',
    description='A module to easily mock code.',
    long_description=(read('README.rst') + '\n\n' +
                      read('HISTORY.rst')),
    url='https://github.com/aaaustin10/Python-Easy-Mock',
    license='MIT',
    author='Austin Stewart',
    py_modules=['auto_mock'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
