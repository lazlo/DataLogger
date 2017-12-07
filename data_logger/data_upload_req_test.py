import unittest
import json
import custom_json
import data_upload_req
import data_record

class DataUploadRequestTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "station23"
		self.req = data_upload_req.DataUploadRequest(self.expectedName)

	def testInit_loggerNameIsSet(self):
		self.assertEqual(self.expectedName, self.req.logger_name)

	def testInit_recordsIsTypeList(self):
		self.assertEqual(True, isinstance(self.req.records, list))

	def testToJSON(self):
		expected = json.dumps(self.req.__dict__)
		expected = expected.replace("logger_name", "LoggerName")
		expected = expected.replace(" ", "")
		self.assertEqual(expected, self.req.to_json())

	def testToJSON_worksOnRecordsToo(self):
		self.req.records.append(data_record.DataRecord())
		self.req.records.append(data_record.DataRecord())
		self.req.records.append(data_record.DataRecord())
		expected = json.dumps(self.req.__dict__, cls=custom_json.CustomJSONEncoder)
		expected = expected.replace("logger_name", "LoggerName")
		expected = expected.replace(" ", "")
		self.assertEqual(expected, self.req.to_json())

	def testToJSON_replacesLoggerNameWithCamleCase(self):
		self.assertEqual(True, "LoggerName" in self.req.to_json())

	def testToJSON_stripsWhitespaces(self):
		expected = json.dumps(self.req.__dict__).replace("logger_name", "LoggerName").replace(" ", "")
		self.assertEqual(expected, self.req.to_json())
