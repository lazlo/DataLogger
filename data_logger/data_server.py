import httplib
import urllib
import urlparse

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
		self.httpconn = httplib.HTTPConnection(self.host, self.port)
		self.error = None

	def upload(self, body):
		try:
			self.httpconn.request(self.req_method, self.path, urllib.urlencode(body), self.req_headers)
			# FIXME get response (via self.httpconn.getresponse()) and check .status and .reason
		except Exception as ex:
			self.error = ex.message
			return False
		self.error = None
		return True
