import unittest
import time
import json

import data_record

json_loads_arg = None
json_loads_value = None
def fake_json_loads(arg):
	global json_loads_arg
	json_loads_arg = arg
	return json_loads_value

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

	def testToJSON(self):
		self.assertEqual(json.dumps(self.dr.__dict__), self.dr.to_json())

	def testFromJSON(self):
		expected = data_record.DataRecord(self.expectedTimestamp, self.expectedMeasurements)
		input_str = json.dumps(expected.__dict__)
		self.assertEqual(expected.__dict__, data_record.DataRecord.from_json(input_str).__dict__)
