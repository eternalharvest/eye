#!/usr/bin/env python
# -*- coding: utf-8 -*-
from client import BACnetClient
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

def test():
	#
	# BACnet 通信の実行
	#
	client = BACnetClient('localhost', '8888')
	print client.ReadPropertyRequest()
	#print client.ReadPropertyRequest()
	#print client.ReadPropertyRequest()

#
# Entry Point
#
if __name__ == '__main__':
	#
	# スケジューラ
	#
	schduler = BlockingScheduler({
		#
		# スレッドプールの設定
		#
		'apscheduler.executors.default' : {
			'class'		: 'apscheduler.executors.pool:ThreadPoolExecutor',
			'max_workers'	: '20'
		},
		'apscheduler.job_defaults.coalesce'		: 'false',
		'apscheduler.job_defaults.max_instances'	: '3',
		'apscheduler.timezone'				: 'UTC',
	})

	#
	# BACnet 通信の実行
	#
	client = BACnetClient('localhost', '8888')

	schduler.add_job(client.ReadPropertyRequest, 'interval', seconds = 1)

	schduler.start()

