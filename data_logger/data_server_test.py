import unittest

import data_server
import httplib

httpconn_request_called = False
httpconn_request_arg_method = None
httpconn_request_arg_headers = None

def fake_httpconn_request(method, url, body=None, headers=None):
	global httpconn_request_called
	global httpconn_request_arg_method
	global httpconn_request_arg_headers
	httpconn_request_called = True
	httpconn_request_arg_method = method
	httpconn_request_arg_headers = headers

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

	def testUpload_callsHttpConnRequestWithFirstArgumentMethodPost(self):
		global httpconn_request_arg_method
		httpconn_request_arg_method = None
		self.srv.httpconn.request = fake_httpconn_request
		self.srv.upload()
		self.assertEqual("POST", httpconn_request_arg_method)

	def testUpload_callsHttpConnRequestWithFourthArgumentHeadersContentTypeXWwwFormUrlEncodedAcceptTextPlain(self):
		global httpconn_request_arg_headers
		httpconn_request_arg_headers = None
		self.srv.httpconn.request = fake_httpconn_request
		self.srv.upload()
		self.assertEqual({"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}, httpconn_request_arg_headers)
