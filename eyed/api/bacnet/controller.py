#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound, HTTPOk
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPRequestTimeout
from driver.bacnet import BACnetSimpleClient
import jsonschema

#
# BACnet
#
@view_config(route_name='api::bacnet:index', renderer='json')
def index(request):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = request.registry.bacnetd.application
	bacnet = BACnetSimpleClient(app)
	return None

#
# BACnet デバイスのスキャン
#
@view_config(route_name='api::bacnet:scan', request_method = 'GET', renderer='json')
def scan(request):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = request.registry.bacnetd.application
	bacnet = BACnetSimpleClient(app)

	#
	# Timeout の 取得
	#
	timeout = 10
	if 'timeout' in request.GET and request.GET['timeout'].isdigit():
		timeout = int(request.GET['timeout'])

	#
	# WhoIsRequest の 送信
	#
	bacnet.WhoIsRequest()

	#
	# WhoIsRequest を 投げてから最初の IAmRequestを受け取るまで待つ
	#
	try:
		device_id = app.iamr_responses.get(timeout = timeout)
		return HTTPOk(json_body = { 'device_id' : device_id })
	except Exception:
		return HTTPRequestTimeout()

#
# BACnet デバイスリストの取得
#
@view_config(route_name='api::bacnet:devices', renderer='json')
def devices(request):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = request.registry.bacnetd.application

	#
	# デバイスリストの作成
	#
	devices = []
	for key, value in app.device_map.items():
		devices.append({ 'device_id' : key, 'ip' : str(value) })

	#
	# デバイスリストを返却
	#
	return HTTPOk(json_body = devices)

#
# BACnet デバイスリストの取得
#
@view_config(route_name='api::bacnet:device', renderer='json')
def device(request):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = request.registry.bacnetd.application
	bacnet = BACnetSimpleClient(app)

	#
	# デバイスID の 取得
	#
	device_id = request.matchdict['device_id']

	#
	# 型の確認とキャスト
	#
	if str(device_id).isdigit() == False:
		return HTTPBadRequest()
	device_id = int(device_id)

	#
	# デバイスID が あるかを確認
	#
	if not device_id in app.device_map:
		return HTTPNotFound()

	#
	# オブジェクトリスト
	#
	object_list = [
		'vendor-name',
		'vendor-identifier',
		'model-name',
		'firmware-revision',
		'application-software-version',
		'protocol-version',
		'protocol-revision',
		'protocol-services-supported',
		'protocol-object-types-supported',
		'object_list'
	]

	#
	# 各プロパティの取得
	#
	r = {}
	for object_name in object_list:
		r[object_name] = bacnet.getDeviceProperty(object_name, 123)

	#
	# プロパティを返却
	#
	return HTTPOk(json_body = r)

