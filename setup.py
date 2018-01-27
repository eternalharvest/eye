#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def _load_requires_from_file(filepath):
	return [pkg_name.rstrip('\n') for pkg_name in open(filepath).readlines()]

def _install_requires():
	return _load_requires_from_file('requirements.txt')

#
# Entry point
#
if __name__ == '__main__':
	setup(
		#
		# Software Information
		#
		name		= 'eyed',
		version		= '0.2.5',

		#
		# Author Information
		#
		author		= 'Naoya Sawada',
		author_email	= 'naoya@tuntunkun.com',

		#
		# Package Information
		#
		packages		= find_packages(),
		install_requires	= _install_requires(),

		data_files = [('eyed/config', ['alembic.ini'])],
		#
		# Console Scripts
		#
		#entry_points		= '''
		#[console_scripts]
		#eyed = eyed.httpd:start
		#'''
	)

