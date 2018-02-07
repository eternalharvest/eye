#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eyed.model import ProxyPoint
from eyed.db import createSession

#
# Job Scheduler
#
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

#
# Singletone Proxyd
#
class SingleProxyd:
	_instance = None

	#
	# Initialize
	#
	def __init__(self):
		self.device_id = 0
		self.bacnetd = None
		self.cache = {}
		#self.scheduler = BackgroundScheduler()
		self.scheduler = BlockingScheduler()

	#
	# get instance
	#
	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	#
	# Measure
	#
	def measure(self):
		session = createSession()
		for point in session.query(ProxyPoint).all():
			print point
		session.close()
		print 'OK'
		pass

	#
	# start
	#
	def start(self, interval = 10, device_id = 1234):
		#
		# スケジューラにメソッドを登録
		#
		self.device_id = device_id
		self.scheduler.add_job(
			self.measure,
			'interval',
			seconds=interval,
			max_instances=1
		)

		#
		# スケジューラの開始
		#
		self.scheduler.start()

#
# Entry Point
#
if __name__ == '__main__':
	SingleProxyd.getInstance().start(5)

