#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.object import AnalogValueObject
from bacpypes.object import register_object_type
from property import ProxyValueProperty

#
# Proxy Value Object Type
#
class ProxyAnalogValueObject(AnalogValueObject):
	properties = [
		ProxyValueProperty('presentValue')
	]

	def __init__(self, **kwargs):
		ProxyValueObject.__init__(self, **kwargs)

#
# オブジェクトを登録
#
register_object_type(ProxyAnalogValueObject)

