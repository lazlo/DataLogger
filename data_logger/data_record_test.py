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

	def testFromJSONString(self):
		expected = data_record.DataRecord(self.expectedTimestamp, self.expectedMeasurements)
		# NOTE python JSON parser seems to be able to only handle double qouted strings
		input_str = str(expected.__dict__).replace("'", "\"")
		self.assertEqual(expected.__dict__, data_record.DataRecord.from_json_string(input_str).__dict__)

	def testFromJSONString_replacesSingleWithDoubleQuotesInInputString(self):
		global json_loads_arg
		global json_loads_value

		dr = data_record.DataRecord(self.expectedTimestamp, self.expectedMeasurements)

		json_loads_arg = None
		json_loads_value = dr.__dict__

		# save original function pointer
		original_json_loads = json.loads
		# overwrite function pointer
		json.loads = fake_json_loads

		# prepare the string we expected to be passed to json.loads()
		expected_json_loads_arg = str(dr.__dict__).replace("'", "\"")
		# create the string that we will pass to DataRecord.from_json_string (that contains single qoutes)
		single_quoted_string = str(dr.__dict__)
		try:
			data_record.DataRecord.from_json_string(single_quoted_string)
			self.assertEqual(expected_json_loads_arg, json_loads_arg)
		finally:
			# restore original function pointer
			json.loads = original_json_loads
