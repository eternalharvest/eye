#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rpyc

#
# Entry Point
#
if __name__ == '__main__':
	client = rpyc.connect("localhost", 12345)
	#config = client.root.SystemService().getNetworkInterfaces()
	#print config

	#
	# BACnet Daemon への 操作
	#
	#bacnetd = client.root.BACnetdService()
	#print bacnetd.start('en1')
	#print bacnetd.stop()
	#print bacnetd.start('en0')

	#
	# BACnet の 操作
	#
	bacnet = client.root.BACnetService()
	#print bacnet.doWhoIsRequest()
	print bacnet.getDevices()
	for i in range(10):
		print bacnet.doReadPropertyRequest(1234, 2, 6, 85)
	print bacnet.getDevices()

	#test = client.root.ICMPService('8.8.8.8')
	#print test.ping()

