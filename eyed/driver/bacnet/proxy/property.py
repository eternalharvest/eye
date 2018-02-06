#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.primitivedata import Real
from bacpypes.object import Property

from eyed.driver.bacnet import BACnetClient
from eyed.client.rpc import BACnetRPCClient

#
# Proxy Value Property
#
class ProxyValueProperty(Property):
	#
	# コンストラクタ
	#
	def __init__(self, identifier):
		Property.__init__(self, identifier, Real, default=0.0, optional=True, mutable=False)
		self.client = BACnetRPCClient('10.2.10.29', 1413)

	#
	# 読み込み
	#
	def ReadProperty(self, obj, arrayIndex=None):
		#print obj
		#print obj.objectIdentifier
		#print obj.__dict__
		#bacnet = BACnetClient(obj._app)
		#print bacnet.WhoIsRequest()
		#print bacnet.ReadPropertyRequest(1234, 2, 1, 85)
		#print 'START READ'
		#result = self.client.doReadPropertyRequest(1234, 2, 1, 85)
		#print 'STOP READ'

		#
		# Access an array
		#
		if arrayIndex is not None:
			raise ExecutionError(errorClass='property', errorCode='propertyIsNotAnArray')
		return 0.0

	#
	# 書き込み
	#
	def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
		raise ExecutionError(errorClass='property', errorCode='writeAccessDenied')

