import unittest

import data_server
import httplib

httpconn_request_called = False

def fake_httpconn_request(method, url, body=None, headers=None):
	global httpconn_request_called
	httpconn_request_called = True

class DataServerTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedAddr = "localhost"
		self.expectedUser = "eris"
		self.expectedPassword = "fnord2342"
		self.srv = data_server.DataServer(self.expectedAddr, self.expectedUser, self.expectedPassword)

	def testInit_addrIsSet(self):
		self.assertEqual(self.expectedAddr, self.srv.addr)

	def testInit_userIsSet(self):
		self.assertEqual(self.expectedUser, self.srv.user)

	def testInit_passwordIsSet(self):
		self.assertEqual(self.expectedPassword, self.srv.password)

	def testInit_httpConnIsInstanceOfHTTPConnection(self):
		self.assertEqual(True, isinstance(self.srv.httpconn, httplib.HTTPConnection))

	def testInit_httpConnHostIsSetToConfigValue(self):
		self.assertEqual(self.expectedAddr, self.srv.httpconn.host)

	def testUpload_callsHttpConnRequest(self):
		global httpconn_request_called
		httpconn_request_called = False
		self.srv.httpconn.request = fake_httpconn_request
		self.srv.upload()
		self.assertEqual(True, httpconn_request_called)
