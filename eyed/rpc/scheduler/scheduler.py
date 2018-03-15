#!/usr/bin/env python
# -*- coding: utf-8 -*-
from initialize import addTaskGroup

#
# Database 接続用
#
from eyed.model import TaskGroup
from eyed.db import createSession

#
# SchedulerService
#
class SchedulerService(object):
	#
	# 測定周期の追加
	#
	def exposed_addTaskGroup(self, name, interval):
		#
		# グループ名が既に登録されていないかを確認
		#
		session = createSession()
		if not session.query(TaskGroup).filter_by(name = name).first() == None:
			return False

		#
		# タスクグループの追加
		#
		addTaskGroup(name, interval)

		#
		# タスクグループの登録
		#
		session.add(TaskGroup(name, interval))
		session.commit()
		return True

	#
	# 測定周期の追加
	#
	def exposed_addBACnetTask(self, device_id, object_id, property_id):
		pass

