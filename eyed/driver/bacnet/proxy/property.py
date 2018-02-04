#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.primitivedata import Real
from bacpypes.object import Property

#
# Proxy Value Property
#
class ProxyValueProperty(Property):
	#
	# コンストラクタ
	#
	def __init__(self, identifier):
		Property.__init__(self, identifier, Real, default=0.0, optional=True, mutable=False)

	#
	# 読み込み
	#
	def ReadProperty(self, obj, arrayIndex=None):
		#
		# access an array
		#
		if arrayIndex is not None:
			raise ExecutionError(errorClass='property', errorCode='propertyIsNotAnArray')
		return 0.0

	#
	# 書き込み
	#
	def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
		raise ExecutionError(errorClass='property', errorCode='writeAccessDenied')

