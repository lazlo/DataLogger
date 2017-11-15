import unittest

import data_store

class DataStoreTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedDataDir = "test-datadir"
		self.ds = data_store.DataStore(self.expectedDataDir)

	def testInit_dataDirIsSet(self):
		self.assertEqual(self.expectedDataDir, self.ds.data_dir)

	def testInit_dataDirDefaultAppliedWhenNoneIsSpecified(self):
		s = data_store.DataStore()
		self.assertEqual(data_store.DataStore.DEFAULT_DATA_DIR, s.data_dir)
