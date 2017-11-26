#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Bootstrap Code
#
def bootstrap(config):
	#
	# Scan controller
	#
	config.add_route('API::BACNET:INDEX', '/')
	config.scan('.controller')

#
# Make bootstrap attribute
#
__all__	= [bootstrap]

