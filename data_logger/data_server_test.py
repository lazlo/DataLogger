import unittest

import data_server
import httplib
import urllib

httpconn_request_called = False
httpconn_request_arg_method = None
httpconn_request_arg_url = None
httpconn_request_arg_body = None
httpconn_request_arg_headers = None

def fake_httpconn_request(method, url, body=None, headers=None):
	global httpconn_request_called
	global httpconn_request_arg_method
	global httpconn_request_arg_url
	global httpconn_request_arg_body
	global httpconn_request_arg_headers
	httpconn_request_called = True
	httpconn_request_arg_method = method
	httpconn_request_arg_url = url
	httpconn_request_arg_body = body
	httpconn_request_arg_headers = headers

class DataServerTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedHost = "192.168.0.1"
		self.expectedPort = 8081
		self.expectedUrl = "/db/req/type/json/store"
		self.expectedAddr = "http://%s:%d%s" % (self.expectedHost, self.expectedPort, self.expectedUrl)
		self.expectedUser = "eris"
		self.expectedPassword = "fnord2342"
		self.requestMethod = "POST"
		self.requestBody = {"@station": 1234, "@type": "foo"}
		self.requestHeaders = {"Content-type": "application/json;charset=utf-8", "Accept": "application/json"}
		self.srv = data_server.DataServer(self.expectedAddr, self.expectedUser, self.expectedPassword)

	def testInit_addrIsSetToHost(self):
		self.assertEqual(self.expectedHost, self.srv.host)

	def testInit_userIsSet(self):
		self.assertEqual(self.expectedUser, self.srv.user)

	def testInit_passwordIsSet(self):
		self.assertEqual(self.expectedPassword, self.srv.password)

	def testInit_httpConnIsInstanceOfHTTPConnection(self):
		self.assertEqual(True, isinstance(self.srv.httpconn, httplib.HTTPConnection))

	def testInit_httpConnHostIsSetToHostPartOfAddressConfigValue(self):
		self.assertEqual(self.expectedHost, self.srv.httpconn.host)

	def testInit_httpConnPortIsSetToPortPartOfAddressConfigValue(self):
		self.assertEqual(self.expectedPort, self.srv.httpconn.port)

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

	def testUpload_callsHttpConnRequestWithSecondArgumentUrl(self):
		global httpconn_request_arg_url
		httpconn_request_arg_url = None
		self.srv.httpconn.request = fake_httpconn_request
		self.srv.upload(self.requestBody)
		self.assertEqual(self.expectedUrl, httpconn_request_arg_url)

	def testUpload_callsHttpConnRequestWithThirdArgumentBodyUrlEncoded(self):
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
