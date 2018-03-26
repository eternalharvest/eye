#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.primitivedata import Real
from bacpypes.object import Property
from bacpypes.errors import ExecutionError

from eyed.single import SingleBACnetd

#
# Database 接続用
#
from eyed.model import BACnetEmulationLog
from eyed.db import SessionFactory

#
# Eyed Present Value
#
class EyedPresentValue(Property):
	#
	# コンストラクタ
	#
	def __init__(self, object_id, instance_id, default_value = 0.0):
		#
		# 各識別子の定義
		#
		self.object_id		= object_id
		self.instance_id	= instance_id
		self.property_id	= 85
		self.identifier		= 'presentValue'

		#
		# スーパクラスのコンストラクタ呼び出し
		#
		Property.__init__(self, self.identifier, Real, default=0.0, optional=True, mutable=False)

		#
		# 初期値のセットアップ
		#
		datastore = SingleBACnetd().getDatastore()
		datastore.set(self.object_id, self.instance_id, self.property_id, default_value)

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
		# キャッシュに値があれば、キャシュの値を返す
		#
		datastore = SingleBACnetd().getDatastore()
		value = datastore.get(self.object_id, self.instance_id, self.property_id)

		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# DBへの登録
			#
			session.add(BACnetEmulationLog(self.object_id, self.instance_id, self.property_id, value))
			sessuin.commit()

		#
		# 値の返却
		#
		if not value == None:
			return value
		raise ExecutionError(errorClass='property', errorCode='abortProprietary')

	#
	# 書き込み
	#
	def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
		raise ExecutionError(errorClass='property', errorCode='writeAccessDenied')

