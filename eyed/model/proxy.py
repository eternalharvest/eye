#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship, backref
from base import BaseObject

#
# プロキシ設定
#
class ProxyPoint(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_PROXY_POINT'

	#
	# カラム定義
	#
	id		= Column('ID', Integer, primary_key=True)

	#
	# プロキシ先
	#
	des_device_id	= Column('DES_DEVICE_ID', Integer)
	des_object_id	= Column('DES_OBJECT_ID', Integer)
	des_instance_id	= Column('DES_INSTANCE_ID', Integer)
	des_property_id	= Column('DES_PROPERTY_ID', Integer)

	#
	# プロキシ元
	#
	src_device_id	= Column('SRC_DEVICE_ID', Integer)
	src_object_id	= Column('SRC_OBJECT_ID', Integer)
	src_instance_id	= Column('SRC_INSTANCE_ID', Integer)
	src_property_id	= Column('SRC_PROPERTY_ID', Integer)

	#
	# コンストラクタ
	#
	def __init__(self,
		des_device_id, des_object_id, des_instance_id, des_property_id,
		src_device_id, src_object_id, src_instance_id, src_property_id):
		#
		# プロキシ先情報取得
		#
		self.des_device_id = des_device_id
		self.des_object_id = des_object_id
		self.des_instance_id = des_instance_id
		self.des_property_id = des_property_id

		#
		# プロキシ元情報取得
		#
		self.src_device_id = src_device_id
		self.src_object_id = src_object_id
		self.src_instance_id = src_instance_id
		self.src_property_id = src_property_id

	#
	# 文字列化
	#
	def __str__(self):
		return '<Proxy des_device_id=%s>' %(self.des_device_id)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			#
			# 宛先
			#
			'des_device_id'		: self.des_device_id,
			'des_object_id'		: self.des_object_id,
			'des_instance_id'	: self.des_instance_id,
			'des_property_id'	: self.des_property_id,
			#
			# 送信元
			#
			'src_device_id'		: self.src_device_id,
			'src_object_id'		: self.src_object_id,
			'src_instance_id'	: self.src_instance_id,
			'src_property_id'	: self.src_property_id,
		}

