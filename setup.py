#!/usr/bin/env python

from distutils.core import setup

setup(name='fabric-ec2',
      version='0.1.2',
      author='Mike Ryan',
      author_email='mike@fadedink.co.uk',
      url='https://github.com/mikery/fabric-ec2',
      packages=['fabric_ec2', ],
      requires=['boto', 'fabric'],
      )
