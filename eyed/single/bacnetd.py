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

	#
	# get allication
	#
	@classmethod
	def getApplication(cls):
		#
		# BACnetd が 起動しているかを確認
		#
		self = SingleBACnetd().getInstance()
		if self.bacnetd == None:
			return None

		#
		# application の インスタンスを返す
		#
		return self.bacnetd.application

