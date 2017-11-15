import unittest

import data_logger
import config

class DataLoggerTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedCfgFile = "data_logger_test_cfg.json"
		self.expectedCfg = config.Config()
		self.expectedCfg.load_file(self.expectedCfgFile)
		self.dl = data_logger.DataLogger(self.expectedCfg)

	def testInit_populatesDataInputsAccordingToConfig(self):
		self.assertEqual(len(self.expectedCfg.data_inputs), len(self.dl.data_inputs))

if __name__ == "__main__":
	unittest.main()
