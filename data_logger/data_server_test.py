import unittest

import data_server
import httplib
import urllib

httpconn_request_called = False
httpconn_request_arg_method = None
httpconn_request_arg_body = None
httpconn_request_arg_headers = None

def fake_httpconn_request(method, url, body=None, headers=None):
	global httpconn_request_called
	global httpconn_request_arg_method
	global httpconn_request_arg_body
	global httpconn_request_arg_headers
	httpconn_request_called = True
	httpconn_request_arg_method = method
	httpconn_request_arg_body = body
	httpconn_request_arg_headers = headers

class DataServerTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedAddr = "localhost"
		self.expectedUser = "eris"
		self.expectedPassword = "fnord2342"
		self.requestMethod = "POST"
		self.requestBody = {"@station": 1234, "@type": "foo"}
		self.requestHeaders = {"Content-type": "application/json;charset=utf-8", "Accept": "application/json"}
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
		self.srv.upload(self.requestBody)
		self.assertEqual(True, httpconn_request_called)

	def testUpload_callsHttpConnRequestWithFirstArgumentMethodPost(self):
		global httpconn_request_arg_method
		httpconn_request_arg_method = None
		self.srv.httpconn.request = fake_httpconn_request
		self.srv.upload(self.requestBody)
		self.assertEqual(self.requestMethod, httpconn_request_arg_method)

	def testUpload_callsHttpConnRequestWithSecondArgumentBodyUrlEncoded(self):
		global httpconn_request_arg_body
		httpconn_request_arg_body = None
		expected_body = urllib.urlencode(self.requestBody)
		self.srv.httpconn.request = fake_httpconn_request
		self.srv.upload(self.requestBody)
		self.assertEqual(expected_body, httpconn_request_arg_body)

	def testUpload_callsHttpConnRequestWithFourthArgumentHeadersContentTypeApplicationJSONCharsetUTF8AcceptApplicationJSON(self):
		global httpconn_request_arg_headers
		httpconn_request_arg_headers = None
		self.srv.httpconn.request = fake_httpconn_request
		self.srv.upload(self.requestBody)
		self.assertEqual(self.requestHeaders, httpconn_request_arg_headers)
