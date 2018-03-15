#!/usr/bin/env python
# -*- coding: utf-8 -*-
from initialize import addTaskGroup

#
# Database 接続用
#
from eyed.model import TaskGroup, BACnetTask
from eyed.db import createSession

#
# BACnet Driver
#
from eyed.driver.bacnet import BACnetClient

#
# Single Instances
#
from eyed.single import SingleBACnetd

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
	def exposed_addBACnetTask(self, name, device_id, object_id, instance_id, property_id):
		#
		# グループ名が存在するかの確認
		#
		session = createSession()
		taskGroup = session.query(TaskGroup).filter_by(name = name).first()
		if taskGroup == None: return False

		#
		# タスクが登録済みであるかを確認
		#
		task = taskGroup.bacnetTasks.filter_by(
			device_id = device_id,
			object_id = object_id,
			instance_id = instance_id,
			property_id = property_id
		).first()
		if not task == None: return False

		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None: return False
		bacnet = BACnetClient(app)

		#
		# 値が取得できるかを確認
		#
		value = bacnet.ReadPropertyRequest(device_id, object_id, instance_id, property_id)
		if value == None: return False

		#
		# タスクの登録
		#
		taskGroup.bacnetTasks.append(BACnetTask(device_id, object_id, instance_id, property_id))
		session.commit()
		return True

