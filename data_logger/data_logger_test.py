import unittest
import os
import time

import data_logger
import config
import data_store
import data_server
import data_input
import data_record

di_get_data_called = False
di_get_data_called_ntimes = 0
def fake_di_get_data():
	global di_get_data_called
	global di_get_data_called_ntimes
	di_get_data_called = True
	di_get_data_called_ntimes += 1

dl_get_data_called = False
def fake_dl_get_data():
	global dl_get_data_called
	dl_get_data_called = True

st_save_called = False
st_save_arg_line = None
def fake_st_save(line):
	global st_save_called
	global st_save_arg_line
	st_save_called = True
	st_save_arg_line = line

ds_upload_called = False
def fake_ds_upload(body):
	global ds_upload_called
	ds_upload_called = True

class DataLoggerTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedCfgFile = "../example/data_logger_test_cfg.json"
		self.expectedCfg = config.Config()
		self.expectedCfg.load_file(self.expectedCfgFile)
		os.mkdir(self.expectedCfg.data_dir)
		self.dl = data_logger.DataLogger(self.expectedCfg)

	def tearDown(self):
		os.rmdir(self.expectedCfg.data_dir)

	def testInit_startUpTimestampIsSetToNow(self):
		expectedTime = int(time.time())
		dl = data_logger.DataLogger(self.expectedCfg)
		self.assertEqual(expectedTime, dl.startup_time)

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

	def testGetData_dataRecordIsPopulatedWithValuesFromDataInputGetData(self):
		"""
		NOTE Even though this test is about checking that the value in the data record that
		get passed to the data store save() are comming from the get_data() of the respective
		data input, for now we start by only checking the number of entries in the measurments
		list of the data record is correct.
		"""
		self.assertEqual(len(self.expectedCfg.data_record_format), len(st_save_arg_line["measurements"]))

	def testGetData_callsDataStoreSave(self):
		global st_save_called
		st_save_called = False
		self.dl.data_store.save = fake_st_save
		self.dl.get_data()
		self.assertEqual(True, st_save_called)

	def testGetData_callsDataStoreSaveWithDataRecordDictAsArgument(self):
		"""
		NOTE We only check that the type of argument is a dict, not its contents.
		"""
		global st_save_arg_line
		st_save_arg_line = None
		self.dl.data_store.save = fake_st_save
		self.dl.get_data()
		self.assertEqual(True, isinstance(st_save_arg_line, dict))

	def testUpdate_callsGetData(self):
		global dl_get_data_called
		dl_get_data_called = False
		self.dl.get_data = fake_dl_get_data
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(True, dl_get_data_called)

	def testUpdate_callsDataServerUpload(self):
		global ds_upload_called
		ds_upload_called = False
		self.dl.data_server.upload = fake_ds_upload
		self.dl.data_store.save = fake_st_save # override save() so no file will be created
		self.dl.update()
		self.assertEqual(True, ds_upload_called)

if __name__ == "__main__":
	unittest.main()
