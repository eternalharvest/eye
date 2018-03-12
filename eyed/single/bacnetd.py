#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Datastore for BACnetd
#
class Datastore:
	#
	# コンストラクタ
	#
	def __init__(self):
		self.hashmap = dict()

	#
	# 鍵の作成
	#
	def __generateKey(self, object_id, instance_id, property_id):
		#
		# 鍵の作成
		#
		return '%d:%d:%d' %(object_id, instance_id, property_id)

	#
	# 値の設定
	#
	def set(self, object_id, instance_id, property_id, value):
		#
		# 鍵を生成しハッシュマップに登録
		#
		key = self.__generateKey(object_id, instance_id, property_id)
		self.hashmap[key] = value

	#
	# 値の検索
	#
	def get(self, object_id, instance_id, property_id):
		#
		# ハッシュマップ内から鍵を検索
		#
		key = self.__generateKey(object_id, instance_id, property_id)
		if not key in self.hashmap:
			return None
		return self.hashmap[key]

#
# Singletone BACnetd
#
class SingleBACnetd:
	#
	# インスタンス保持用変数
	#
	_instance = None

	#
	# Initialize
	#
	def __init__(self):
		self.bacnetd = None
		self.datastore = Datastore()

	#
	# get Instance
	#
	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	#
	# get Application
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

	#
	# get Datastore
	#
	@classmethod
	def getDatastore(cls):
		#
		# Datastore の 返却
		#
		self = SingleBACnetd().getInstance()
		return self.datastore

#
# Test Case
#
if __name__ == '__main__':
	datastore = SingleBACnetd().getDatastore()
	print datastore.set(0, 1, 2, 3, 'Hello')
	print datastore.get(0, 1, 2, 3)

