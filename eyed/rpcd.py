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
from rpc.bacnetd import BACnetdService

#
# SQLAlchemy
#
from database import Session

#
# MyService
#
class MyService(rpyc.Service):
	exposed_SystemService = SystemService
	exposed_BACnetdService = BACnetdService

	def __init__(self, *args, **kwargs):
		super(MyService, self).__init__(*args, **kwargs)

if __name__ == "__main__":
	server = ThreadedServer(MyService, port = 12345)
	server.start()

