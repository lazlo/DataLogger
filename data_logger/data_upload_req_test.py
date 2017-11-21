import unittest

import data_upload_req

class DataUploadRequestTestCase(unittest.TestCase):

	def setUp(self):
		self.req = data_upload_req.DataUploadRequest()

	def testFoo(self):
		self.assertEqual(True, True)
