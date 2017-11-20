import unittest
import time

import data_record

class DataRecordTestCase(unittest.TestCase):

	def setUp(self):
		self.now = time.strftime("%Y-%m-%dT%H:%M:%S")
		self.dr = data_record.DataRecord()

	def testTimestampIsNow(self):
		self.assertEqual(self.now, self.dr.timestamp)
