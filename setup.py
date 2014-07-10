#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2014 Jonathan Delvaux <apdu@djoproject.net>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#http://docs.python.org/2/distutils/setupscript.html
from distutils.core import setup

setup(name='apdu',
      version='1.0',
      description='Framework to generate smartcard apdu',
      author='Jonathan Delvaux',
      author_email='apdu@djoproject.net',
      url='https://github.com/djo938/apdu_builder',
      packages=['apdu', 'apdu.misc', 'apdu.readers', 'apdu.library', 'apdu.standard', 'apdu.tag'],
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities'
      ]
     )
