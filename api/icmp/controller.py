#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

#
# BACnet
#
@view_config(route_name='API::ICMP:INDEX', renderer='json')
def index(request):
	from driver.icmp import ICMP

	icmp = ICMP('10.2.10.24')
	return icmp.ping()

