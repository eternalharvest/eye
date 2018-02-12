#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.primitivedata import Real
from bacpypes.object import Property

from eyed.single import SingleProxyd
from eyed.driver.bacnet.definition import findObjectByName

from eyed.model import ProxyPoint
from eyed.db import createSession

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

		object_type, instance_id = obj.objectIdentifier
		o = findObjectByName(object_type)
		if not o == None:
			session = createSession()
			p = session.query(ProxyPoint).filter_by(
				src_object_id	= o['id'],
				src_instance_id = instance_id
			).first()

			single = SingleProxyd.getInstance()
			if p.id in single.cache:
				return single.cache[p.id]
		raise ExecutionError(errorClass='property', errorCode='propertyIsNotAnArray')

	#
	# 書き込み
	#
	def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
		raise ExecutionError(errorClass='property', errorCode='writeAccessDenied')

