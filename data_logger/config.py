import json
import data_input

class Config():

	def __init__(self):
		self.system_name = None
		self.server_addr = None
		self.server_user = None
		self.server_password = None
		self.server_upload_period_sec = None
		self.server_poll_period_sec = None
		self.data_records_per_server_upload = None
		self.data_dir = None
		self.data_inputs_sample_period_sec = None
		self.data_inputs_storage_period_sec = None
		self.data_inputs = None
		self.data_record_format = None

	def _primary_required_fields_valid(self):
		if not self.system_name:
			return False
		if not self.server_addr:
			return False
		if not self.server_user:
			return False
		if not self.server_password:
			return False
		if not self.server_upload_period_sec:
			return False
		if not self.server_poll_period_sec:
			return False
		if not self.data_inputs_sample_period_sec:
			return False
		if not self.data_inputs_storage_period_sec:
			return False
		if not self.data_inputs:
			return False
		if not self.data_record_format:
			return False
		return True

	def _data_inputs_valid(self):
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
			if not di["class"]:
				return False
			try:
				getattr(data_input, di["class"])
			except AttributeError:
				return False
		return True

	def _data_record_format_valid(self):
		for di_name in self.data_record_format:
			if not self.data_input_exists(di_name):
				return False
		return True

	def is_valid(self):
		if not self._primary_required_fields_valid():
			return False
		if not self._data_inputs_valid():
			return False
		if not self._data_record_format_valid():
			return False
		return True

	def load_file(self, cfgfile):
		d = json.loads(open(cfgfile).read())
		self.system_name = d["system_name"]
		self.server_addr = d["server_addr"]
		self.server_user = d["server_user"]
		self.server_password = d["server_password"]
		self.server_upload_period_sec = d["server_upload_period_sec"]
		self.server_poll_period_sec = d["server_poll_period_sec"]
		if "data_records_per_server_upload" in d.keys():
			self.data_records_per_server_upload = d["data_records_per_server_upload"]
		if "data_dir" in d.keys():
			self.data_dir = d["data_dir"]
		self.data_inputs_sample_period_sec = d["data_inputs_sample_period_sec"]
		self.data_inputs_storage_period_sec = d["data_inputs_storage_period_sec"]
		self.data_inputs = d["data_inputs"]
		self.data_record_format = d["data_record_format"]

	def data_input_exists(self, name):
		for di in self.data_inputs:
			if di["name"] == name:
				return True
		return False

	def get_data_input(self, name):
		for di in self.data_inputs:
			if di["name"] == name:
				return di

	def get_data_inputs_by_class(self, class_name):
		di_list = []
		for di in self.data_inputs:
			if di["class"] == class_name:
				di_list.append(di)
		return di_list
