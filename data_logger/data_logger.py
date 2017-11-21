import data_store
import data_server
import data_input
import data_record

import time

class DataLogger():

	def __init__(self, config):
		self.startup_time_sec = self._time()
		self.config = config
		self.data_store = data_store.DataStore(self.config.data_dir)
		self.data_server = data_server.DataServer(self.config.server_addr, self.config.server_user, self.config.server_password)
		self.data_inputs = []
		self._populate_data_inputs()
		# scheduling related variables
		self.next_data_inputs_sample_time_sec	= self.startup_time_sec + self.config.data_inputs_sample_period_sec
		self.next_server_upload_time_sec	= self.startup_time_sec + self.config.server_upload_period_sec
		self.next_server_poll_time_sec		= self.startup_time_sec + self.config.server_poll_period_sec

	def _time(self):
		"""
		This method exists only so we can mock time.time() in our unit tests
		"""
		return int(time.time())

	def _populate_data_inputs(self):
		for di_cfg in self.config.data_inputs:
			di_class = getattr(data_input, di_cfg["class"])
			di_obj = di_class(di_cfg["name"])
			self.data_inputs.append(di_obj)

	def _get_data_input(self, name):
		for di in self.data_inputs:
			if di.name != name:
				continue
			return di

	def get_data(self):
		rec = data_record.DataRecord()
		for di_name in self.config.data_record_format:
			di = self._get_data_input(di_name)
			data = di.get_data()
			rec.measurements.append(data)
		self.data_store.save(rec.__dict__)

	def update(self):
		now = self._time()
		if now >= self.next_data_inputs_sample_time_sec:
			self.next_data_inputs_sample_time_sec = now + self.config.data_inputs_sample_period_sec
		if now >= self.next_server_upload_time_sec:
			self.next_server_upload_time_sec = now + self.config.server_upload_period_sec
		if now >= self.next_server_poll_time_sec:
			self.next_server_poll_time_sec = now + self.config.server_poll_period_sec

		self.get_data()
		body = {}
		self.data_server.upload(body)
		# FIXME check return value of upload
		# FIXME on success, delete serialized version of data_record from data_store
