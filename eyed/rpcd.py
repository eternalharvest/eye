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
from eyed.rpc.system import SystemService
from eyed.rpc.bacnet import BACnetService
from eyed.rpc.bacnetd import BACnetdService, start_bacnetd

#
# RPCService
#
class RPCService(rpyc.Service):
	exposed_SystemService = SystemService
	exposed_BACnetdService = BACnetdService
	exposed_BACnetService = BACnetService

#
# デーモンの起動
#
def start():
	#
	# BACnet Daemon の 起動
	#
	start_bacnetd()

	#
	# RPCサーバ の 起動
	#
	server = ThreadedServer(RPCService, port = 12345)
	server.start()

#
# Entry Point
#
if __name__ == "__main__":
	start()

