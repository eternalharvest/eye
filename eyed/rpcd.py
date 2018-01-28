#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

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
def start(port = 1413):
	#
	# スクリプトを実行するディレクトリ設定
	#
	base_path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(base_path)

	#
	# DB を 最新のスキーマ へ アップデート
	#
	command = ['alembic upgrade head']
	subprocess.check_call(command, shell=True)

	#
	# BACnet Daemon の 起動
	#
	start_bacnetd()

	#
	# RPCサーバ の 起動
	#
	server = ThreadedServer(RPCService, port = port)
	server.start()

#
# Entry Point
#
if __name__ == "__main__":
	start()

