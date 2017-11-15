import unittest

import data_logger
import config
import data_input

class DataLoggerTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedCfgFile = "data_logger_test_cfg.json"
		self.expectedCfg = config.Config()
		self.expectedCfg.load_file(self.expectedCfgFile)
		self.dl = data_logger.DataLogger(self.expectedCfg)

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

if __name__ == "__main__":
	unittest.main()
