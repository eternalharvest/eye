#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
from bacpypes.pdu import Address
from bacpypes.app import BIPSimpleApplication, BIPForeignApplication
from bacpypes.service.device import LocalDeviceObject
from bacpypes.core import run, stop

class App(BIPSimpleApplication):
	def __init__(self, *args):
		BIPSimpleApplication.__init__(self, *args)
		self._request = None

	def request(self, apdu):
		self._request = apdu
		BIPSimpleApplication.request(self, apdu)

	def confirmation(self, apdu):
		BIPSimpleApplication.confirmation(self, apdu)

	def indication(self, apdu):
		print apdu
		print apdu.pduSource
		if (isinstance(self._request, WhoIsRequest)) and (isinstance(apdu, IAmRequest)):
			device_type, device_instance = apdu.iAmDeviceIdentifier

			print device_type, device_instance

