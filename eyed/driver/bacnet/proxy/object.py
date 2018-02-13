#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.object import AnalogValueObject, AnalogInputObject
from bacpypes.object import register_object_type
from property import ProxyValueProperty

#
# Proxy Analog Value Object Type
#
class ProxyAnalogValueObject(AnalogValueObject):
	properties = [
		ProxyValueProperty('presentValue')
	]

	def __init__(self, **kwargs):
		AnalogValueObject.__init__(self, **kwargs)

#
# Proxy Analog Input Object Type
#
class ProxyAnalogInputObject(AnalogInputObject):
	properties = [
		ProxyValueProperty('presentValue')
	]

	def __init__(self, **kwargs):
		AnalogInputObject.__init__(self, **kwargs)

#
# オブジェクトを登録
#
register_object_type(ProxyAnalogValueObject)
register_object_type(ProxyAnalogInputObject)

