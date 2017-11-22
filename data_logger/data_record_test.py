import unittest
import time

import data_record

class DataRecordTestCase(unittest.TestCase):

	def setUp(self):
		self.now = time.strftime("%Y-%m-%dT%H:%M:%S")
		self.expectedTimestamp = "2017-04-28T00:00:00"
		self.expectedMeasurements = [11.11, 22.22, 33.33]
		self.dr = data_record.DataRecord()

	def testInit_timestampIsNow(self):
		self.assertEqual(self.now, self.dr.timestamp)

	def testInit_measurementsIsOfTypeList(self):
		self.assertEqual(True, isinstance(self.dr.measurements, list))

	def testInit_timestampIsSetFromFirstArgument(self):
		self.assertEqual(self.expectedTimestamp, data_record.DataRecord(self.expectedTimestamp).timestamp)

	def testInit_measurementsIsSetFromSecondArgument(self):
		self.assertEqual(self.expectedMeasurements, data_record.DataRecord(self.expectedTimestamp, self.expectedMeasurements).measurements)

	def testFromJSONString(self):
		expected = data_record.DataRecord(self.expectedTimestamp, self.expectedMeasurements)
		# NOTE python JSON parser seems to be able to only handle double qouted strings
		input_str = str(expected.__dict__).replace("'", "\"")
		self.assertEqual(expected.__dict__, data_record.DataRecord.from_json_string(input_str).__dict__)
