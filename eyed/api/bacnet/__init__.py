#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Bootstrap Code
#
def bootstrap(config):
	#
	# Scan controller
	#
	config.add_route('api::bacnet:index', '/')
	config.add_route('api::bacnet:scan', '/scan/')
	config.add_route('api::bacnet:devices', '/devices/')
	config.add_route('api::bacnet:device', '/devices/{device_id}')
	config.scan('.controller')

#
# Make bootstrap attribute
#
__all__	= [bootstrap]

