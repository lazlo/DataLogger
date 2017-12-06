import unittest
import os
import time
import json
import logging

import data_logger
import config
import data_store
import data_server
import data_input
import data_record
import data_upload_req

#
# Time and Scheduler related fakes
#

time_value = None
def fake_time():
	return time_value

sch_update_called = False
def fake_sch_update():
	global sch_update_called
	sch_update_called = True

#
# DataInput fakes
#

di_get_data_called = False
di_get_data_called_ntimes = 0
def fake_di_get_data():
	global di_get_data_called
	global di_get_data_called_ntimes
	di_get_data_called = True
	di_get_data_called_ntimes += 1

#
# DataLogger fakes
#

dl_get_data_called = False
def fake_dl_get_data():
	global dl_get_data_called
	dl_get_data_called = True

dl_save_data_called = False
def fake_dl_save_data():
	global dl_save_data_called
	dl_save_data_called = True

dl_build_data_upload_request_called = False
dl_build_data_upload_request_value = None
def fake_dl_build_data_upload_request():
	global dl_build_data_upload_request_called
	dl_build_data_upload_request_called = True
	return dl_build_data_upload_request_value

dl_upload_called = False
def fake_dl_upload():
	global dl_upload_called
	dl_upload_called = True

dl_poll_called = False
def fake_dl_poll():
	global dl_poll_called
	dl_poll_called = True

#
# DataStore fakes
#

class FakeDataStore():

	def __init__(self):
		self.read_called = False
		self.read_value = None
		self.read_latest_called = False
		self.read_latest_value = None

	def read(self):
		self.read_called = True
		return self.read_value

	def read_latest(self, n=1):
		self.read_latest_called = True
		return self.read_latest_value

st_save_called = False
def fake_st_save():
	global st_save_called
	st_save_called = True

st_save_latest_called = False
def fake_st_save_latest():
	global st_save_latest_called
	st_save_latest_called = True

st_read_called = False
st_read_value = None
def fake_st_read():
	global st_read_called
	st_read_called = True
	return st_read_value

st_drop_by_called = False
st_drop_by_args = []
def fake_st_drop_by(filter_key, filter_value):
	global st_drop_by_called
	st_drop_by_called = True
	st_drop_by_args.append(filter_key)
	st_drop_by_args.append(filter_value)

#
# DataServer fakes
#

ds_upload_called = False
ds_upload_arg = None
ds_upload_value = None
def fake_ds_upload(body):
	global ds_upload_called
	global ds_upload_arg
	ds_upload_called = True
	ds_upload_arg = body
	return ds_upload_value

logging_basic_config_ptr_original = None
logging_basic_config_called = False
logging_basic_config_arg_format = None
def fake_logging_basic_config(format=None):
	global logging_basic_config_called
	global logging_basic_config_arg_format
	logging_basic_config_called = True
	logging_basic_config_arg_format = format

class FakeLogger():

	def __init__(self):
		self.error_called = False
		self.error_arg = None
		self.debug_called = False

	def error(self, msg):
		self.error_called = True
		self.error_arg = msg

	def debug(self, msg):
		self.debug_called = True

class DataLoggerTestCase(unittest.TestCase):

	def setUp(self):
		global logging_basic_config_called
		global logging_basic_config_arg_format
		global logging_basic_config_ptr_original
		logging_basic_config_called = False
		logging_basic_config_arg_format = None
		# Save ptr to logging.basicConfig
		logging_basic_config_ptr_original = logging.basicConfig
		logging.basicConfig = fake_logging_basic_config

		self.expectedStartupTimeSec = int(time.time())
		self.expectedCfgFile = "../example/data_logger_test_cfg.json"
		self.expectedCfg = config.Config()
		self.expectedCfg.load_file(self.expectedCfgFile)
		os.mkdir(self.expectedCfg.data_dir)
		self.dl = data_logger.DataLogger(self.expectedCfg)

	def tearDown(self):
		# Restore ptr to logging.basicConfig
		logging.basicConfig = logging_basic_config_ptr_original
		os.rmdir(self.expectedCfg.data_dir)

	#
	# __ini__()
	#

	def testInit_logIsLoggerInstance(self):
		self.assertEqual(True, isinstance(self.dl.log, logging.Logger))

	def testInit_callsLoggingBasicConfig(self):
		self.assertEqual(True, logging_basic_config_called)

	def testInit_callsLoggingBasicConfigWithArgumentFormat(self):
		expected = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s() %(message)s"
		self.assertEqual(expected, logging_basic_config_arg_format)

	def testInit_startupTimeSecIsSetToNow(self):
		dl = data_logger.DataLogger(self.expectedCfg)
		self.assertEqual(self.expectedStartupTimeSec, dl.startup_time_sec)

	def testInit_nextSchedUpdateTimeSecIsSetToNowPlusOneSecond(self):
		expected = self.expectedStartupTimeSec + self.dl.sch_update_period_sec
		self.assertEqual(expected, self.dl.next_sched_update_time_sec)

	def testInit_schedUpdatePeriodSecIsSetToDefault(self):
		self.assertEqual(data_logger.DataLogger.DEFAULT_SCHED_UPDATE_PERIOD_SEC, self.dl.sch_update_period_sec)

	def testInit_dataStoreIsObject(self):
		self.assertEqual(True, isinstance(self.dl.data_store, data_store.DataStore))

	def testInit_dataStoreDataDirIsSetToConfigValue(self):
		self.assertEqual(self.expectedCfg.data_dir, self.dl.data_store.data_dir)

	def testInit_serverIsDataServerObject(self):
		self.assertEqual(True, isinstance(self.dl.data_server, data_server.DataServer))

	def testInit_dataInputsIsPopulatedAccordingToConfig(self):
		self.assertEqual(len(self.expectedCfg.data_inputs), len(self.dl.data_inputs))

	def testInit_dataInputsIsListOfDataInputObjects(self):
		expectedType = data_input.DataInput
		ofExpectedType = True
		for obj in self.dl.data_inputs:
			if not isinstance(obj, expectedType):
				ofExpectedType = False
				break
		self.assertEqual(True, ofExpectedType)

	def testInit_dataInputsElementsAreOfClassAccordingToConfig(self):
		ofExpectedType = True
		for obj in self.dl.data_inputs:
			di_cfg = self.dl.config.get_data_input(obj.name)
			expectedType = getattr(data_input, di_cfg["class"])
			if not isinstance(obj, expectedType):
				ofExpectedType = False
				break
		self.assertEqual(True, ofExpectedType)

	#
	# get_data()
	#

	def testGetData_callsGetDataOnObjectsInDataInputsList(self):
		global di_get_data_called
		di_get_data_called = False
		for di in self.dl.data_inputs:
			di.get_data = fake_di_get_data
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.get_data()
		self.assertEqual(True, di_get_data_called)

	def testGetData_callsGetDataOnObjectsInDataInputListOnlyListedInDataRecordFormat(self):
		global di_get_data_called_ntimes
		di_get_data_called_ntimes = 0
		for di in self.dl.data_inputs:
			di.get_data = fake_di_get_data
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.get_data()
		self.assertEqual(len(self.dl.config.data_record_format), di_get_data_called_ntimes)

	def testGetData_appendsDataRecordToDataStoreDataRecords(self):
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.get_data()
		self.dl.get_data()
		self.dl.get_data()
		self.assertEqual(3, len(self.dl.data_store.data_records))

	def testGetData_callsLogDebug(self):
		self.dl.log = FakeLogger()
		self.dl.get_data()
		self.assertEqual(True, self.dl.log.debug_called)

	#
	# save_data()
	#

	def testSaveData_callsDataStoreSaveLatest(self):
		global st_save_latest_called
		st_save_latest_called = False
		self.dl.data_store.save = fake_st_save
		self.dl.data_store.save_latest = fake_st_save_latest
		self.dl.save_data()
		self.assertEqual(True, st_save_latest_called)

	def testSaveData_callsLogDebug(self):
		self.dl.data_store.save = fake_st_save
		self.dl.log = FakeLogger()
		self.dl.save_data()
		self.assertEqual(True, self.dl.log.debug_called)

	#
	# _build_data_upload_request()
	#

	def testBuildDataUploadRequest_returnsDataUploadRequestObj(self):
		self.dl.data_store.read = fake_st_read # fake DataStore.read() so no filesystem access is performed
		self.assertEqual(True, isinstance(self.dl._build_data_upload_request(), data_upload_req.DataUploadRequest))

	def testBuildDataUploadRequest_callsDataStoreRead(self):
		global st_read_called
		global st_read_value
		st_read_called = False
		st_read_value = ["{\"timestamp\": \"\", \"measurements\": \"\"}", "{\"timestamp\": \"\", \"measurements\": \"\"}"] # list of JSON strings
		self.dl.data_store.read = fake_st_read
		self.dl._build_data_upload_request()
		self.assertEqual(True, st_read_called)

	def testBuildDataUploadRequest_callsDataStoreReadLatestWhenConfigParamDataRecordsPerServerUploadIsNotNone(self):
		self.dl.config.data_records_per_server_upload = 5
		self.dl.data_store = FakeDataStore()
		self.dl.data_store.read_latest_value = [data_record.DataRecord().to_json()]
		self.dl._build_data_upload_request()
		self.assertEqual(True, self.dl.data_store.read_latest_called)

	def testBuildDataUploadRequest_populatesRecords(self):
		self.dl.data_store.read = fake_st_read # fake DataStore.read() so no filesystem access is performed
		self.assertEqual(True, len(self.dl._build_data_upload_request().records) > 0)

	def testBuildDataUploadRequest_recordsEntriesAreOfTypeDataRecord(self):
		global st_read_value
		st_read_value = ["{\"timestamp\": \"\", \"measurements\": \"\"}"] # list of JSON strings
		self.dl.data_store.read = fake_st_read # fake DataStore.read() so no filesystem access is performed
		self.assertEqual(True, isinstance(self.dl._build_data_upload_request().records[0], data_record.DataRecord))

	#
	# upload()
	#

	def testUpload_callsBuildDataUploadRequest(self):
		global dl_build_data_upload_request_called
		global dl_build_data_upload_request_value
		ur = data_upload_req.DataUploadRequest(self.expectedCfg.system_name)
		dl_build_data_upload_request_called = False
		dl_build_data_upload_request_value = ur
		self.dl.data_store.drop_by = fake_st_drop_by
		self.dl._build_data_upload_request = fake_dl_build_data_upload_request
		self.dl.upload()
		self.assertEqual(True, dl_build_data_upload_request_called)

	def testUpload_callsDataServerUpload(self):
		global ds_upload_called
		ds_upload_called = False
		self.dl.data_store.drop_by = fake_st_drop_by
		self.dl.data_store.read = fake_st_read
		self.dl.data_server.upload = fake_ds_upload
		self.dl.upload()
		self.assertEqual(True, ds_upload_called)

	def testUpload_callsDataServerUploadWithDataUploadRequestTransformedToJSONReturnedByBuildDataUploadRequest(self):
		global dl_build_data_upload_request_value
		global ds_upload_arg
		ur = data_upload_req.DataUploadRequest(self.expectedCfg.system_name)
		dl_build_data_upload_request_value = ur
		ds_upload_arg = None
		self.dl.data_store.drop_by = fake_st_drop_by
		self.dl._build_data_upload_request = fake_dl_build_data_upload_request
		self.dl.data_server.upload = fake_ds_upload
		self.dl.upload()
		self.assertEqual(dl_build_data_upload_request_value.to_json(), ds_upload_arg)

	# upload() calls DataStore.drop_by()

	def testUpload_callsDataStoreDropByWhenDataServerUploadReturnsTrue(self):
		global dl_build_data_upload_request_value
		global ds_upload_value
		global st_drop_by_called
		ur = data_upload_req.DataUploadRequest(self.expectedCfg.system_name)
		dl_build_data_upload_request_value = ur
		ds_upload_value = True
		st_drop_by_called = False
		self.dl._build_data_upload_request = fake_dl_build_data_upload_request
		self.dl.data_server.upload = fake_ds_upload
		self.dl.data_store.drop_by = fake_st_drop_by
		self.dl.upload()
		self.assertEqual(True, st_drop_by_called)

	def testUpload_doesNotCallDataStoreDropByWhenDataServerUploadReturnsFalse(self):
		global dl_build_data_upload_request_value
		global ds_upload_value
		global st_drop_by_called
		ur = data_upload_req.DataUploadRequest(self.expectedCfg.system_name)
		dl_build_data_upload_request_value = ur
		ds_upload_value = False
		st_drop_by_called = False
		self.dl._build_data_upload_request = fake_dl_build_data_upload_request
		self.dl.data_server.upload = fake_ds_upload
		self.dl.data_store.drop_by = fake_st_drop_by
		self.dl.upload()
		self.assertEqual(False, st_drop_by_called)

	def testUpload_callsLogErrorWhenDataServerUploadReturnsFalse(self):
		global ds_upload_value
		ds_upload_value = False
		self.dl._build_data_upload_request = fake_dl_build_data_upload_request
		self.dl.data_server.upload = fake_ds_upload
		self.dl.log = FakeLogger()
		self.dl.upload()
		self.assertEqual(True, self.dl.log.error_called)

	def testUpload_callsLogErrorWithArgMsgWhenDataServerUploadReturnsFalse(self):
		global ds_upload_value
		ds_upload_value = False
		self.dl._build_data_upload_request = fake_dl_build_data_upload_request
		self.dl.data_server.upload = fake_ds_upload
		self.dl.log = FakeLogger()
		self.dl.upload()
		self.assertEqual(True, self.dl.log.error_arg.startswith("upload failed"))

	def testUpload_callsDataStoreDropByWithTimestampOfDataRecordsFromUploadRequest(self):
		global dl_build_data_upload_request_value
		global ds_upload_value
		global st_drop_by_args
		expected_filter_values = []
		ur = data_upload_req.DataUploadRequest(self.expectedCfg.system_name)
		for i in range(0, 4):
			dr = data_record.DataRecord()
			ur.records.append(dr)
			expected_filter_values.append(dr.timestamp)
		dl_build_data_upload_request_value = ur
		ds_upload_value = True
		st_drop_by_args = []
		self.dl._build_data_upload_request = fake_dl_build_data_upload_request
		self.dl.data_server.upload = fake_ds_upload
		self.dl.data_store.drop_by = fake_st_drop_by
		self.dl.upload()
		self.assertEqual(["timestamp", expected_filter_values], st_drop_by_args)

	def testUpload_callsLogDebug(self):
		self.dl.log = FakeLogger()
		self.dl._build_data_upload_request = fake_dl_build_data_upload_request
		self.dl.upload()
		self.assertEqual(True, self.dl.log.debug_called)

	#
	# update()
	#

	def testUpdate_setsNextSchedUpdateTimeSec(self):
		global time_value
		time_value = self.expectedStartupTimeSec + self.dl.sch_update_period_sec
		expected = time_value + self.dl.sch_update_period_sec
		self.dl._time = fake_time
		self.dl.sch.tasks[2].fp = fake_dl_upload # fake upload so no file access is performed via _build_data_upload_request() and DataStore.read()
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(expected, self.dl.next_sched_update_time_sec)

	# update() calls get_data()

	def testUpdate_callsGetDataWhenScheduled(self):
		global time_value
		global dl_get_data_called
		time_value = self.expectedStartupTimeSec + self.expectedCfg.data_inputs_sample_period_sec
		dl_get_data_called = False
		self.dl._time = fake_time
		self.dl.sch.tasks[0].fp = fake_dl_get_data
		self.dl.sch.tasks[2].fp = fake_dl_upload # also fake upload as the scheduling period can be the same as for get data
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(True, dl_get_data_called)

	def testUpdate_doesNotCallGetDataWhenNotScheduled(self):
		global dl_get_data_called
		dl_get_data_called = False
		self.dl.sch.tasks[0].fp = fake_dl_get_data
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(False, dl_get_data_called)

	# update() calls save_data()

	def testUpdate_callsSaveDataWhenScheduled(self):
		global time_value
		global dl_save_data_called
		time_value = self.expectedStartupTimeSec + self.expectedCfg.data_inputs_storage_period_sec
		dl_save_data_called = False
		self.dl._time = fake_time
		self.dl.sch.tasks[1].fp = fake_dl_save_data
		self.dl.sch.tasks[2].fp = fake_dl_upload # also fake upload as the scheduling period can be the same as the task under test
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(True, dl_save_data_called)

	# update() calls upload()

	def testUpdate_callsUploadWhenScheduled(self):
		global time_value
		global dl_upload_called
		time_value = self.expectedStartupTimeSec + self.expectedCfg.server_upload_period_sec
		dl_upload_called = False
		self.dl._time = fake_time
		self.dl.sch.tasks[2].fp = fake_dl_upload
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(True, dl_upload_called)

	def testUpdate_doesNotCallUploadWhenNotScheduled(self):
		global dl_upload_called
		dl_upload_called = False
		self.dl.sch.tasks[2].fp = fake_dl_upload
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(False, dl_upload_called)

	# update() calls poll()

	def testUpdate_callsPollWhenScheduled(self):
		global time_value
		global dl_poll_called
		time_value = self.expectedStartupTimeSec + self.expectedCfg.server_poll_period_sec
		dl_poll_called = False
		self.dl._time = fake_time
		self.dl.sch.tasks[2].fp = fake_dl_upload # also fake upload as the scheduling period can be the same as for poll
		self.dl.sch.tasks[3].fp = fake_dl_poll
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(True, dl_poll_called)

	def testUpdate_doesNotCallPollWhenNotScheduled(self):
		global dl_poll_called
		dl_poll_called = False
		self.dl.sch.tasks[3].fp = fake_dl_poll
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(False, dl_poll_called)

	# update() calls sched.update()

	def testUpdate_callsSchedUpdateWhenScheduled(self):
		global time_value
		global sch_update_called
		time_value = self.expectedStartupTimeSec + self.dl.sch_update_period_sec
		sch_update_called = False
		self.dl._time = fake_time
		self.dl.sch.update = fake_sch_update
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(True, sch_update_called)

	def testUpdate_doesNotCallSchedUpdateWhenNotScheduled(self):
		global sch_update_called
		sch_update_called = False
		self.dl.sch.update = fake_sch_update
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(False, sch_update_called)

if __name__ == "__main__":
	unittest.main()
