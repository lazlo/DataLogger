import httplib

class DataServer():

	def __init__(self, addr, user, password):
		self.addr = addr
		self.user = user
		self.password = password
		self.httpconn = httplib.HTTPConnection("localhost")
