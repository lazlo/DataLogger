import httplib
import urlparse
import json

class DataServer():

	def __init__(self, addr, user, password):
		url = urlparse.urlparse(addr)
		self.host = url.hostname
		self.port = url.port
		self.path = url.path
		self.user = user
		self.password = password
		self.req_method = "POST"
		self.req_headers = {"Content-type": "application/json;charset=utf-8", "Accept": "application/json"}
		self.httpconn = None
		self.error = None

	def _create_http_conn(self):
		return httplib.HTTPConnection(self.host, self.port)

	def upload(self, body):
		try:
			self.httpconn = self._create_http_conn()
			self.httpconn.request(self.req_method, self.path, body, self.req_headers)
			res = self.httpconn.getresponse()
			# check for HTTP error
			if res.status != httplib.OK:
				raise Exception(res.status)
			json_res = json.loads(res.read())
			# check for database server error
			if json_res["IsError"]:
				raise Exception(json_res["Message"])
		except Exception as ex:
			self.error = ex.message
			return False
		self.error = None
		return True
