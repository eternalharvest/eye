#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

#
# BACnet
#
@view_config(route_name='API::BACNET:INDEX', renderer='json')
def index(request):
	from driver.bacnet import BACnetClient
	bacnet = BACnetClient(request.registry.bacnetd.application)

	bacnet.WhoIsRequest()
	#return bacnet.ReadPropertyRequest('10.2.10.24')

	#
	# WhoIsRequest を 投げてから最初の IAmRequestを受け取るまで待つ
	#
	app = request.registry.bacnetd.application
	print app.iamr_responses.get(timeout=10)
	return None

