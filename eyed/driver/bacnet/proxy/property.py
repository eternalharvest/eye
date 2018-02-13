#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.primitivedata import Real
from bacpypes.object import Property
from bacpypes.errors import ExecutionError

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

		#
		# オブジェクト種別, インスタンスID の 取得
		#
		object_type, instance_id = obj.objectIdentifier
		o = findObjectByName(object_type)
		if not o == None:
			#
			# オブジェクト種別からIDを取得
			#
			src_object_id	= o['id']
			src_instance_id = instance_id

			#
			# キャッシュに値があれば、キャシュの値を返す
			#
			key = '%s:%s' %(src_object_id, src_instance_id)
			single = SingleProxyd.getInstance()
			if key in single.cache:
				return single.cache[key]
		raise ExecutionError(errorClass='property', errorCode='propertyIsNotAnArray')

	#
	# 書き込み
	#
	def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
		raise ExecutionError(errorClass='property', errorCode='writeAccessDenied')

