import json

class Config():

	def __init__(self):
		self.system_name = None
		self.server_addr = None
		self.server_login = None
		self.server_password = None
		self.data_inputs = None

	def is_valid(self):
		if not self.system_name:
			return False
		if not self.server_addr:
			return False
		if not self.server_login:
			return False
		if not self.server_password:
			return False
		if not self.data_inputs:
			return False
		data_input_names = []
		for di in self.data_inputs:
			if not "name" in di.keys():
				return False
			if not di["name"]:
				return False
			if di["name"] in data_input_names:
				return False
			data_input_names.append(di["name"])
			if not "class" in di.keys():
				return False
		return True

	def load_file(self, cfgfile):
		d = json.loads(open(cfgfile).read())
		self.system_name = d["system_name"]
		self.server_addr = d["server_addr"]
		self.server_login = d["server_login"]
		self.server_password = d["server_password"]
		self.data_inputs = d["data_inputs"]
