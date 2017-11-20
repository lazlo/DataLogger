import httplib
import urllib

class DataServer():

	def __init__(self, addr, user, password):
		self.host = addr.split("/")[0]
		self.user = user
		self.password = password
		self.httpconn = httplib.HTTPConnection(self.host)

	def upload(self, body):
		method = "POST"
		url = ""
		body = urllib.urlencode(body)
		headers = {"Content-type": "application/json;charset=utf-8", "Accept": "application/json"}
		self.httpconn.request(method, url, body, headers)
