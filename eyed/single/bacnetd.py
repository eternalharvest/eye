#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Singletone BACnetd
#
class SingleBACnetd:
	_instance = None

	#
	# Initialize
	#
	def __init__(self):
		self.bacnetd = None

	#
	# get instance
	#
	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

