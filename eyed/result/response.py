#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Response
#
class Response:
	def __init__(self, result):
		self.result = result

#
# Success
#
class Success(Response)
	def __init__(self, response):
		Response.__init__(True)
		self.result = result
		self.response = response

#
# Error
#
class Error(Response)
	def __init__(self, error):
		Response.__init__(True)
		self.result = result
		self.error = error

