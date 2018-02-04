#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from eyed.client.rpc import RPCClient
from eyed.client.rpc import BACnetdRPCClient
from eyed.rpcd import start as start_eyed

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
# デーモン起動用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def start(ctx):
	pass

#
# RPC デーモンの起動
#
@start.command()
@click.pass_context
def rpcd(ctx):
	#
	# 引数の取得
	#
	port = ctx.obj['port']
	start_eyed(port)

#
# BACNET PROXYD の起動
#
@start.command()
@click.pass_context
def bacnet_proxyd(ctx):
	click.echo('STARTING BACNET PROXYD...')

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

