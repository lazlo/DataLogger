import json

class Config():

	def __init__(self):
		self.system_name = None
		self.server_addr = None
		self.server_login = None
		self.server_password = None

	def is_valid(self):
		if not self.system_name:
			return False
		if not self.server_addr:
			return False
		if not self.server_login:
			return False
		if not self.server_password:
			return False
		return True

	def load_file(self, cfgfile):
		d = json.loads(open(cfgfile).read())
		self.system_name = d["system_name"]
		self.server_addr = d["server_addr"]
		self.server_login = d["server_login"]
		self.server_password = d["server_password"]
