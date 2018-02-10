#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eyed.model import ProxyPoint
from eyed.db import createSession

#
# BACnet Client
#
from eyed.client.rpc.client import BACnetRPCClient

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
		client = BACnetRPCClient('127.0.0.1')
		for p in session.query(ProxyPoint).all():
			r = client.doReadPropertyRequest(
				p.device_id,
				p.object_id,
				p.instance_id,
				p.property_id
			)

			key = '%s:%s:%s:%s' %(
				p.device_id,
				p.object_id,
				p.instance_id,
				p.property_id
			)
			self.cache[key] = r
		session.close()
		print self.cache
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

