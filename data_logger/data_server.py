import httplib

class DataServer():

	def __init__(self, addr, user, password):
		self.addr = addr
		self.user = user
		self.password = password
		self.httpconn = httplib.HTTPConnection(self.addr)

	def upload(self):
		method = "POST"
		url = ""
		body = None
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		self.httpconn.request(method, url, body, headers)
