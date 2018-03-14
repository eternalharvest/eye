#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship, backref
from base import BaseObject

#
# TaskGroup の 設定
#
class TaskGroup(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_TASK_GROUP'

	#
	# カラム定義
	#
	id		= Column('ID', Integer, primary_key=True)
	name		= Column('NAME', String)
	interval	= Column('INTERVAL', Integer)

	#
	# コンストラクタ
	#
	def __init__(self, name, interval):
		self.name	= name
		self.interval	= interval

	#
	# 文字列化
	#
	def __str__(self):
		return '<TaskGroup name=%s, interval=%d>' %(self.name, self.interval)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'		: self.id,
			'name'		: self.name,
			'interval'	: self.interval,
		}

