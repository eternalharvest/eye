#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.primitivedata import Real
from bacpypes.object import Property
from bacpypes.errors import ExecutionError

from eyed.single import SingleBACnetd, DatastoreType

#
# Database 接続用
#
from eyed.model import BACnetSimulationLog
from eyed.db import SessionFactory

#
# Eyed Present Value
#
class EyedPresentValue(Property):
	#
	# コンストラクタ
	#
	def __init__(self, object_id, instance_id, default_value = 0, type = DatastoreType.STATIC):
		#
		# 各識別子の定義
		#
		self.type		= type
		self.object_id		= object_id
		self.instance_id	= instance_id
		self.property_id	= 85
		self.identifier		= 'presentValue'

		#
		# スーパクラスのコンストラクタ呼び出し
		#
		Property.__init__(
			self,
			self.identifier,
			Real,
			default=0.0,
			optional=True,
			mutable=False
		)

		#
		# 初期値のセットアップ
		#
		datastore = SingleBACnetd().getDatastore()
		datastore.setBACnetValue(
			DatastoreType.STATIC,
			self.object_id,
			self.instance_id,
			self.property_id,
			default_value
		)

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
		value = datastore.getBACnetValue(
			self.type,
			self.object_id,
			self.instance_id,
			self.property_id
		)
		print self.type, self.object_id, self.instance_id, self.property_id, value

		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# DBへの登録
			#
			session.add(BACnetSimulationLog(self.object_id, self.instance_id, self.property_id, value))
			session.commit()

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

	#
	# プロパティ種別の変更
	#
	def setType(self, type):
		self.type = type

