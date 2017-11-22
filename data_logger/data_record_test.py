import unittest
import time

import data_record

class DataRecordTestCase(unittest.TestCase):

	def setUp(self):
		self.now = time.strftime("%Y-%m-%dT%H:%M:%S")
		self.dr = data_record.DataRecord()

	def testInit_timestampIsNow(self):
		self.assertEqual(self.now, self.dr.timestamp)

	def testInit_measurementsIsOfTypeList(self):
		self.assertEqual(True, isinstance(self.dr.measurements, list))
