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

	config = client.root.BACnetdService()
	#print config.start('en0')
	print config.stop()
	print config.start('en1')

	#test = client.root.ICMPService('8.8.8.8')
	#print test.ping()

