#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from eyed.client.rpc import RPCClient
from eyed.client.rpc import BACnetRPCClient
from eyed.client.rpc import BACnetdRPCClient

#########################################################################
# 引数処理
#########################################################################
@click.group()
@click.option('--host', '-h', default = '127.0.0.1')
@click.option('--port', '-p', default = 1413)
@click.pass_context
def cmd(ctx, host, port):
	ctx.obj['host'] = host
	ctx.obj['port'] = port

#########################################################################
# 情報確認用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def show(ctx):
	pass

#
# NIC の 情報取得
#
@show.command()
@click.pass_context
def interfaces(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = RPCClient(host, port)

	#
	# 接続した Eyed の NIC 情報取得
	#
	interfaces = client.getNetworkInterfaces()
	for interface in interfaces:
		name = interface['name']
		ipv4 = interface['ipv4']
		click.echo('%s %s' %(name, ipv4))

#########################################################################
# BACnet 関連の情報取得
#########################################################################
@show.group()
@click.pass_context
def bacnet(ctx):
	pass

#
# BACnet Device の スキャン
#
@bacnet.command()
@click.pass_context
def scan(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	click.echo(client.scan())

#
# BACnet Device の 情報取得
#
@bacnet.command()
@click.pass_context
def devices(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	click.echo(client.getDevices())

#########################################################################
# デーモン起動用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def start(ctx):
	pass

#
# BACNETD の起動
#
@start.command()
@click.pass_context
@click.argument('interface')
def bacnetd(ctx, interface):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# EYED に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	click.echo(client.start(interface, 65535))

#
# BACNET PROXYD の起動
#
@start.command()
@click.pass_context
def bacnet_proxyd(ctx):
	click.echo('STARTING BACNET PROXYD...')

#########################################################################
# デーモン停止用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def stop(ctx):
	pass

#
# BACNETD の 停止
#
@stop.command()
@click.pass_context
def bacnetd(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# EYED に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	click.echo(client.stop())

#
# START
#
def start_cli():
	cmd(obj = {})

#
# Entry Point
#
if __name__ == '__main__':
	start_cli()

