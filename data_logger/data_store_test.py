import unittest
import os

import data_store

class DataStoreTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedDataDir = "test-datadir"
		os.mkdir(self.expectedDataDir)
		self.ds = data_store.DataStore(self.expectedDataDir)

	def tearDown(self):
		os.rmdir(self.expectedDataDir)

	def testInit_dataDirIsSet(self):
		self.assertEqual(self.expectedDataDir, self.ds.data_dir)

	def testInit_dataDirDefaultAppliedWhenNoneIsSpecified(self):
		s = data_store.DataStore()
		self.assertEqual(data_store.DataStore.DEFAULT_DATA_DIR, s.data_dir)

	def testSave_createsFileInDataDir(self):
		expectedFile = os.path.join(self.expectedDataDir, "foo.txt")
		self.ds.save()
		self.assertEqual(True, os.path.exists(expectedFile))
		os.remove(expectedFile)
