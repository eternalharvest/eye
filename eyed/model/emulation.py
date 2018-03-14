#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship, backref
from base import BaseObject

#
# BACnet Emulation Object の 設定
#
class BACnetEmulationObject(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_BACNET_EMULATION_OBJECT'

	#
	# カラム定義
	#
	id		= Column('ID', Integer, primary_key=True)
	name		= Column('NAME', String)
	object_id	= Column('OBJECT_ID', Integer)
	instance_id	= Column('INSTACNE_ID', Integer)

	#
	# リレーション
	#
	properties = relationship('BACnetEmulationProperty', lazy='dynamic', backref = 'object')

	#
	# コンストラクタ
	#
	def __init__(self, name, object_id, instance_id):
		self.name		= name
		self.object_id		= object_id
		self.instance_id	= instance_id

	#
	# 文字列化
	#
	def __str__(self):
		return '<EmulationObject name=%s, object_id=%d, instance_id=%d>' %(self.name, self.object_id, self.instance_id)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'		: self.id,
			'name'		: self.name,
			'object_id'	: self.object_id,
			'instance_id'	: self.instance_id,
			'properties'	: [prop.to_dict() for prop in self.properties]
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
	property_id	= Column('PROPERTY_ID', Integer)

	#
	# 外部キー
	#
	emulation_point_id = Column('M_EMULATION_POINT_ID', Integer, ForeignKey('M_BACNET_EMULATION_OBJECT.ID'))

	#
	# コンストラクタ
	#
	def __init__(self, property_id):
		self.property_id = property_id

	#
	# 文字列化
	#
	def __str__(self):
		return '<BACnetProperty property_id=%d>' %(self.property_id)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'		: self.id,
			'property_id'	: self.property_id,
		}

