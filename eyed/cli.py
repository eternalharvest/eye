#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from eyed.client.rpc import RPCClient
from eyed.client.rpc import BACnetRPCClient
from eyed.client.rpc import BACnetdRPCClient
from eyed.client.rpc import BACnetProxyRPCClient

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
# パラメータ の 追加
#########################################################################
@cmd.group()
@click.pass_context
def add(ctx):
	pass

#########################################################################
# エミュレーションパラメータ の 定義
#########################################################################
@add.group(name = 'emulation')
@click.pass_context
def add_emulation(ctx):
	pass

#########################################################################
# プロトコル の 定義
#########################################################################
@add_emulation.group(name = 'bacnet')
@click.pass_context
def add_emulation_bacnet(ctx):
	pass

#########################################################################
# BACnet オブジェクト の 定義
#########################################################################
@add_emulation_bacnet.command(name = 'object')
@click.pass_context
@click.argument('name')
@click.argument('object_id')
@click.argument('instance_id')
def add_emulation_bacnet_object(ctx, name, object_id, instance_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)

	#
	# オブジェクトの登録
	#
	click.echo(client.addObject(
		name,
		int(object_id),
		int(instance_id),
	))

#########################################################################
# パラメータ の 定義
#########################################################################
@add_emulation_bacnet.command(name = 'property')
@click.pass_context
@click.argument('name')
@click.argument('property_id')
def add_emulation_bacnet_property(ctx, name, property_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)

	#
	# オブジェクトの登録
	#
	click.echo(client.addProperty(
		name,
		int(property_id)
	))

#########################################################################
# パラメータ の 設定
#########################################################################
@cmd.group()
@click.pass_context
def set(ctx):
	pass

#########################################################################
# エミュレーションパラメータ の 設定
#########################################################################
@set.group(name = 'emulation')
@click.pass_context
def set_emulation(ctx):
	pass

#########################################################################
# プロトコル の 設定
#########################################################################
@set_emulation.group(name = 'bacnet')
@click.pass_context
def set_emulation_bacnet(ctx):
	pass

#########################################################################
# パラメータ の 定義
#########################################################################
@set_emulation_bacnet.command(name = 'property')
@click.pass_context
@click.argument('name')
@click.argument('property_id')
@click.argument('value')
def set_emulation_bacnet_property(ctx, name, property_id, value):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)

	#
	# オブジェクトの登録
	#
	click.echo(client.setProperty(
		name,
		int(property_id),
		float(value)
	))

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
@show.command(name = 'interfaces')
@click.pass_context
def show_interfaces(ctx):
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
@show.group(name = 'bacnet')
@click.pass_context
def show_bacnet(ctx):
	pass

#
# BACnet Device の スキャン
#
@show_bacnet.command(name = 'scan')
@click.pass_context
def show_bacnet_scan(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	if client.getStatus() == False:
		click.echo('BACnetd is not running...')
		return

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	click.echo(client.scan())

#
# BACnet Device の 情報取得
#
@show_bacnet.command(name = 'devices')
@click.pass_context
def show_bacnet_devices(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	if client.getStatus() == False:
		click.echo('BACnetd is not running...')
		return

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	click.echo(client.getDevices())

#########################################################################
# データ取得用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def run(ctx):
	pass

#
# BACEPICS の起動
#
@run.command(name = 'bacepics')
@click.pass_context
@click.argument('device_id')
def run_bacepics(ctx, device_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	if client.getStatus() == False:
		click.echo('BACnetd is not running...')
		return

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	click.echo(client.getEpics(int(device_id)))

#
# BACRP の起動
#
@run.command(name = 'bacrp')
@click.pass_context
@click.argument('device_id')
@click.argument('object_id')
@click.argument('instance_id')
@click.argument('property_id')
def run_bacrp(ctx, device_id, object_id, instance_id, property_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	if client.getStatus() == False:
		click.echo('BACnetd is not running...')
		return

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	click.echo(client.doReadPropertyRequest(
		int(device_id),
		int(object_id),
		int(instance_id),
		int(property_id)
	))

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
@start.command(name = 'bacnetd')
@click.pass_context
@click.argument('interface')
def start_bacnetd(ctx, interface):
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
@start.command(name = 'proxyd')
@click.pass_context
@click.argument('interval')
def start_proxyd(ctx, interval):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# BACnetd の 起動確認
	#
	client = BACnetdRPCClient(host, port)
	if client.getStatus() == False:
		click.echo('BACnetd is not running...')
		return

	#
	# 同期処理実行
	#
	client = BACnetRPCClient(host, port)
	client.scan()

	#
	# EYED に RPC接続
	#
	client = BACnetProxyRPCClient(host, port)
	click.echo(client.start(interval = int(interval)))

#########################################################################
# デーモン状態取得用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def status(ctx):
	pass

#
# BACNETD の 状態確認
#
@status.command(name = 'bacnetd')
@click.pass_context
def status_bacnetd(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	click.echo(client.getStatus())

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
@stop.command(name = 'bacnetd')
@click.pass_context
def stop_bacnetd(ctx):
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

