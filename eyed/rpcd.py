#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Remote Procedure Call
#
import rpyc
from rpyc.utils.server import ThreadedServer

#
# Services
#
from rpc.system import SystemService
from rpc.bacnetd import BACnetdService, start_bacnetd

#
# MyService
#
class MyService(rpyc.Service):
	exposed_SystemService = SystemService
	exposed_BACnetdService = BACnetdService

	def on_connect(self):
		pass

	def __init__(self, *args, **kwargs):
		super(MyService, self).__init__(*args, **kwargs)

#
# Entry Point
#
if __name__ == "__main__":
	#
	# BACnet Daemon の 起動
	#
	start_bacnetd()

	#
	# RPCサーバ の 起動
	#
	server = ThreadedServer(MyService, port = 12345)
	server.start()

