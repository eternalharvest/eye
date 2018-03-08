#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship, backref
from base import BaseObject

#
# Emulation Point の 設定
#
class EmulationPoint(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_EMULATION_POINT'

	#
	# カラム定義
	#
	id	= Column('ID', Integer, primary_key=True)
	name	= Column('NAME', String)

	#
	# リレーション
	#
	bacnetEmulationProperties = relationship('BACnetEmulationProperty', backref = 'emulationPoint')

	#
	# コンストラクタ
	#
	def __init__(self, name):
		self.name = name

	#
	# 文字列化
	#
	def __str__(self):
		return '<EmulationPoint name=%s>' %(self.name)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'name' : self.name,
		}

#
# BACnet Emulation Property の 設定
#
class BACnetEmulationProperty(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_BACNET_EMULATION_PROPERTY'

	#
	# カラム定義
	#
	id		= Column('ID', Integer, primary_key=True)
	object_id	= Column('OBJECT_ID', Integer)
	instance_id	= Column('INSTACNE_ID', Integer)
	property_id	= Column('PROPERTY_ID', Integer)

	#
	# 外部キー
	#
	emulation_point_id = Column('M_EMULATION_POINT_ID', Integer, ForeignKey('M_EMULATION_POINT.ID'))

	#
	# コンストラクタ
	#
	def __init__(self, object_id, instance_id, property_id):
		self.object_id		= object_id
		self.instance_id	= instance_id
		self.property_id	= property_id

	#
	# 文字列化
	#
	def __str__(self):
		return '<BACnetProperty>'

