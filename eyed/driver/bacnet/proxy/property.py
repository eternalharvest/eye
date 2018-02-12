#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.primitivedata import Real
from bacpypes.object import Property

from eyed.single import SingleProxyd

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
		# Access an array
		#
		if arrayIndex is not None:
			raise ExecutionError(errorClass='property', errorCode='propertyIsNotAnArray')

		single = SingleProxyd.getInstance()
		print single
		print obj.objectIdentifier
		#bacnet = BACnetClient(obj._app)
		#print bacnet.WhoIsRequest()
		#print bacnet.ReadPropertyRequest(1234, 2, 1, 85)
		#print 'START READ'
		#result = self.client.doReadPropertyRequest(1234, 2, 1, 85)
		#print 'STOP READ'

		return 0.0

	#
	# 書き込み
	#
	def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
		raise ExecutionError(errorClass='property', errorCode='writeAccessDenied')

