#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Database 接続用
#
from eyed.model import TaskGroup
from eyed.db import SessionFactory

#
# BACnet Daemon Instance
#
from eyed.single import SingleScheduler

#
# TaskGroup の 追加
#
def addTaskGroup(name, interval):
	#
	# タスクグループの追加
	#
	sched = SingleScheduler.getInstance()
	sched.addTaskGroup(name, interval)

#
# スケジューラの開始
#
def start_scheduler():
	#
	# DB への 接続
	#
	with SessionFactory() as session:
		#
		# 既に登録されているタスクグループの取得
		#
		taskGroups = session.query(TaskGroup).all()

		#
		# 登録されているタスクの呼び出し
		#
		for taskGroup in taskGroups:
			addTaskGroup(taskGroup.name, taskGroup.interval)

if __name__ == '__main__':
	start_scheduler()

