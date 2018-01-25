#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship, backref
from base import BaseObject
import uuid

#
# 設定
#
class Config(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_CONFIG'

	#
	# カラム定義
	#
	id	= Column('ID', String, primary_key=True)	# 識別子
	key	= Column('KEY', String)				# 鍵
	value	= Column('VALUE', String)			# 値

	#
	# コンストラクタ
	#
	def __init__(self, key, value):
		self.id = str(uuid.uuid4())
		self.key = key
		self.value = value

	#
	# 文字列化
	#
	def __str__(self):
		return '<Config key=%s, value=%s>' %(self.key, self.value)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'	: self.id,
			'key'	: self.key,
			'value'	: self.value,
		}

