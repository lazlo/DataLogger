import data_store
import data_server
import data_input
import data_record
import data_logger_sched
import data_upload_req

import time
import json

class DataLogger():

	DEFAULT_SCHED_UPDATE_PERIOD_SEC = 1

	def __init__(self, config):
		self.startup_time_sec = self._time()
		self.config = config
		self.data_store = data_store.DataStore(self.config.data_dir)
		self.data_server = data_server.DataServer(self.config.server_addr, self.config.server_user, self.config.server_password)
		self.data_inputs = []
		self._populate_data_inputs()
		# scheduling related variables
		self.sch_update_period_sec = self.DEFAULT_SCHED_UPDATE_PERIOD_SEC
		self.sch = data_logger_sched.DataLoggerScheduler()
		self.next_sched_update_time_sec		= self.startup_time_sec + self.sch_update_period_sec
		self._init_sched_tasks()

	def _init_sched_tasks(self):
		period = self.config.data_inputs_sample_period_sec
		delay = 0
		self.sch.add(self.get_data, period, delay)

		period = self.config.data_inputs_storage_period_sec
		delay = 0
		self.sch.add(self.save_data, period, delay)

		period = self.config.server_upload_period_sec
		delay = 0
		self.sch.add(self.upload, period, delay)

		period = self.config.server_poll_period_sec
		delay = 0
		self.sch.add(self.poll, period, delay)

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
		self.data_store.data_records.append(rec)

	def save_data(self):
		self.data_store.save_latest()

	def _build_data_upload_request(self):
		ur = data_upload_req.DataUploadRequest(self.config.system_name)
		for json_rec in self.data_store.read():
			rec = data_record.DataRecord.from_json(json_rec)
			ur.records.append(rec)
		return ur

	def upload(self):
		ur = self._build_data_upload_request()
		self.data_server.upload(ur.to_json())
		# FIXME check return value of upload
		# FIXME on success, delete serialized version of data_record from data_store
		return

	def poll(self):
		return

	def update(self):
		do_sch_update = False

		now = self._time()
		if now >= self.next_sched_update_time_sec:
			self.next_sched_update_time_sec = now + self.sch_update_period_sec
			do_sch_update = True

		if do_sch_update:
			self.sch.update()
		self.sch.dispatch()
