# -*- coding: utf-8 -*-

from setuptools import setup

long_desc = '''
This package contains the ER diagram Sphinx extension.

.. add description here ..
'''

requires = ['Sphinx>=1.4']

setup(
    name='sphinx_erdiagram',
    version='0.0.1',
    url='https://github.com/myyasuda/sphinx_erdiagram',
    download_url='http://pypi.python.org/pypi/sphinx_erdiagram',
    license='MIT',
    author='myasuda',
    author_email='myasuda@uchida.co.jp',
    description='Sphinx "ER diagram" extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Sphinx :: Extension',
        #'Framework :: Sphinx :: Theme',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=['myasuda.sphinx'],
    include_package_data=True,
    install_requires=requires
)
