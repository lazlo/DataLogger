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
		self.httpconn = httplib.HTTPConnection(self.host, self.port)
		self.error = None

	def upload(self, body):
		method = "POST"
		url = self.path
		body = urllib.urlencode(body)
		headers = {"Content-type": "application/json;charset=utf-8", "Accept": "application/json"}
		try:
			self.httpconn.request(method, url, body, headers)
		except Exception as ex:
			self.error = ex.message
			return False
		self.error = None
		return True
