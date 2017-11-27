import unittest

import data_server
import httplib

create_http_conn_called = False
create_http_conn_value = None
def fake_create_http_conn():
	global create_http_conn_called
	create_http_conn_called = True
	return create_http_conn_value

class FakeHTTPResponse():

	def __init__(self):
		self.status = None
		self.reason = None

class FakeHTTPConnection():

	def __init__(self, host, port):
		self.request_called = False
		self.request_exception = None
		self.getresponse_called = False
		self.getresponse_value = FakeHTTPResponse()
		self.host = host
		self.port = port

	def request(self, method, path, body, headers):
		self.request_called = True
		self.request_method = method
		self.request_path = path
		self.request_body = body
		self.request_headers = headers
		if self.request_exception:
			raise self.request_exception

	def getresponse(self):
		self.getresponse_called = True
		return self.getresponse_value

class DataServerTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedHost = "192.168.0.1"
		self.expectedPort = 8081
		self.expectedUrl = "/db/req/type/json/store"
		self.expectedAddr = "http://%s:%d%s" % (self.expectedHost, self.expectedPort, self.expectedUrl)
		self.expectedUser = "eris"
		self.expectedPassword = "fnord2342"
		self.expectedRequestMethod = "POST"
		self.expectedRequestBody = {"@station": 1234, "@type": "foo"}
		self.expectedRequestHeaders = {"Content-type": "application/json;charset=utf-8", "Accept": "application/json"}
		self.srv = data_server.DataServer(self.expectedAddr, self.expectedUser, self.expectedPassword)

	#
	# __init__()
	#

	def testInit_addrIsSetToHost(self):
		self.assertEqual(self.expectedHost, self.srv.host)

	def testInit_userIsSet(self):
		self.assertEqual(self.expectedUser, self.srv.user)

	def testInit_passwordIsSet(self):
		self.assertEqual(self.expectedPassword, self.srv.password)

	def testInit_httpConnIsNone(self):
		self.assertEqual(None, self.srv.httpconn)

	def testInit_errorIsNone(self):
		self.assertEqual(None, self.srv.error)

	#
	# _create_http_conn()
	#

	def testCreateHttpConn_returnsLibHttpHttpConnectionObject(self):
		self.assertEqual(True, isinstance(self.srv._create_http_conn(), httplib.HTTPConnection))

	def testCreateHttpConn_returnsObjWithHostSetToHostPartOfAddressConfigValue(self):
		conn = self.srv._create_http_conn()
		self.assertEqual(self.expectedHost, conn.host)

	def testCreateHttpConnt_returnsObjWithPortSetToPortPartOfAddressConfigValue(self):
		conn = self.srv._create_http_conn()
		self.assertEqual(self.expectedPort, conn.port)

	#
	# upload()
	#

	def testUpload_callsCreateHttpConn(self):
		global create_http_conn_called
		create_http_conn_called = False
		self.srv._create_http_conn = fake_create_http_conn
		self.srv.upload(self.expectedRequestBody)
		self.assertEqual(True, create_http_conn_called)

	def _mock_http_conn_via_create_http_conn(self, raise_exception_on_request=None):
		global create_http_conn_value
		create_http_conn_value = FakeHTTPConnection(self.expectedHost, self.expectedPort)
		if raise_exception_on_request:
			create_http_conn_value.request_exception = raise_exception_on_request
		self.srv._create_http_conn = fake_create_http_conn

	def testUpload_callsRequest(self):
		self._mock_http_conn_via_create_http_conn()
		self.srv.upload(self.expectedRequestBody)
		self.assertEqual(True, create_http_conn_value.request_called)

	def testUpload_callsRequestWithFirstArgumentMethodPost(self):
		self._mock_http_conn_via_create_http_conn()
		self.srv.upload(self.expectedRequestBody)
		self.assertEqual(self.expectedRequestMethod, create_http_conn_value.request_method)

	def testUpload_callsRequestWithSecondArgumentUrl(self):
		self._mock_http_conn_via_create_http_conn()
		self.srv.upload(self.expectedRequestBody)
		self.assertEqual(self.expectedUrl, create_http_conn_value.request_path)

	def testUpload_callsRequestWithThirdArgumentBody(self):
		self._mock_http_conn_via_create_http_conn()
		self.srv.upload(self.expectedRequestBody)
		self.assertEqual(self.expectedRequestBody, create_http_conn_value.request_body)

	def testUpload_callsRequestWithFourthArgumentHeaders(self):
		self._mock_http_conn_via_create_http_conn()
		self.srv.upload(self.expectedRequestBody)
		self.assertEqual(self.expectedRequestHeaders, create_http_conn_value.request_headers)

	def testUpload_callsGetResponse(self):
		self._mock_http_conn_via_create_http_conn()
		self.srv.upload(self.expectedRequestBody)
		self.assertEqual(True, create_http_conn_value.getresponse_called)

	def testUpload_returnFalseWhenGetResponseStatusIsNot200(self):
		self._mock_http_conn_via_create_http_conn()
		create_http_conn_value.getresponse_value.status = 404
		self.assertEqual(False, self.srv.upload(self.expectedRequestBody))

	def testUpload_returnsTrue(self):
		self._mock_http_conn_via_create_http_conn()
		create_http_conn_value.getresponse_value.status = 200
		rv = self.srv.upload(self.expectedRequestBody)
		self.assertEqual(True, rv)

	def testUpload_returnsFalseOnException(self):
		raise_exception_on_request = Exception()
		self._mock_http_conn_via_create_http_conn(raise_exception_on_request)
		rv = self.srv.upload(self.expectedRequestBody)
		self.assertEqual(False, rv)

	def testUpload_setsErrorOnException(self):
		expectedErrorMsg = "Connection refused"
		raise_exception_on_request = Exception(expectedErrorMsg)
		self._mock_http_conn_via_create_http_conn(raise_exception_on_request)
		self.srv.upload(self.expectedRequestBody)
		self.assertEqual(expectedErrorMsg, self.srv.error)

	def testUpload_setsErrorToNoneOnSuccess(self):
		expectedErrorMsg = "Forbidden"
		raise_exception_on_request = Exception(expectedErrorMsg)
		self._mock_http_conn_via_create_http_conn(raise_exception_on_request)
		self.srv.upload(self.expectedRequestBody)
		# as this point self.srv.error should be set
		self.assertEqual(expectedErrorMsg, self.srv.error)
		# now do a successful request
		self._mock_http_conn_via_create_http_conn()
		self.srv.upload(self.expectedRequestBody)
		self.assertEqual(None, self.srv.error)
