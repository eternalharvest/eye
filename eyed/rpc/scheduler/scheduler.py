#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
		print interval

