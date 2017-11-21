import unittest

import data_upload_req

class DataUploadRequestTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "station23"
		self.req = data_upload_req.DataUploadRequest(self.expectedName)

	def testInit_loggerNameIsSet(self):
		self.assertEqual(self.expectedName, self.req.logger_name)

	def testInit_recordsIsTypeList(self):
		self.assertEqual(True, isinstance(self.req.records, list))
