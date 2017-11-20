import data_store
import data_server
import data_input

class DataLogger():

	def __init__(self, config):
		self.config = config
		self.data_store = data_store.DataStore(self.config.data_dir)
		self.data_server = data_server.DataServer(self.config.server_addr, self.config.server_user, self.config.server_password)
		self.data_inputs = []
		self._populate_data_inputs()

	def _populate_data_inputs(self):
		for di_cfg in self.config.data_inputs:
			di_class = getattr(data_input, di_cfg["class"])
			di_obj = di_class(di_cfg["name"])
			self.data_inputs.append(di_obj)

	def get_data(self):
		# FIXME create a data_record object for each call
		for di in self.data_inputs:
			di.get_data()
		# FIXME pass data_record to data_store
		self.data_store.save()

	def update(self):
		self.get_data()
		body = {}
		self.data_server.upload(body)
		# FIXME check return value of upload
		# FIXME on success, delete serialized version of data_record from data_store
