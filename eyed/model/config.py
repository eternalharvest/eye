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
	key	= Column('KEY', String, primary_key=True)	# 鍵
	value	= Column('VALUE', String)			# 値

	#
	# コンストラクタ
	#
	def __init__(self, key, value):
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
			'key'	: self.key,
			'value'	: self.value,
		}

