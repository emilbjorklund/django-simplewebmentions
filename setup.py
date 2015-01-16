# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
    long_description = f.read().strip()
    f.close()
except IOError:
    long_description = None

setup(
    name='django-simplewebmentions',
    url='http://github.com/emilbjorklund/django-simplewebmentions',
    version='0.1.0',
    description='A simple django app to help you send and receive Webmentions.',
    author='Emil Björklund',
    author_email='bjorklund.emil@gmail.com',
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    test_suite='tests.runtests.main',
    install_requires=['Django>=1.7', 'webmentiontools>=0.4.0']
    )