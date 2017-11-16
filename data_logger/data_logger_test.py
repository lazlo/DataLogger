import unittest

import data_logger
import config
import data_store
import data_input

di_get_data_called = False

def fake_di_get_data():
	global di_get_data_called
	di_get_data_called = True

class DataLoggerTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedCfgFile = "data_logger_test_cfg.json"
		self.expectedCfg = config.Config()
		self.expectedCfg.load_file(self.expectedCfgFile)
		self.dl = data_logger.DataLogger(self.expectedCfg)

	def testInit_dataStoreIsObject(self):
		self.assertEqual(True, isinstance(self.dl.data_store, data_store.DataStore))

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
		self.dl.get_data()
		self.assertEqual(True, di_get_data_called)

if __name__ == "__main__":
	unittest.main()
