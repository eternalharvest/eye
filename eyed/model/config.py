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
	json	= Column('JSON', String)			# 設定

	#
	# コンストラクタ
	#
	def __init__(self, json):
		self.id = str(uuid.uuid4())
		self.json = json

	#
	# 文字列化
	#
	def __str__(self):
		return '<Config json=%s>' %(self.json)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'	: self.id,
			'json'	: self.json,
		}

