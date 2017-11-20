import unittest
import os

import data_store

class DataStoreTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedDataDir = "test-datadir"
		self.expectedFile = os.path.join(self.expectedDataDir, "foo.txt")
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
		self.ds.save("record23")
		self.assertEqual(True, os.path.exists(self.expectedFile))
		os.remove(self.expectedFile)

	def testSave_appendsToFileInDataDir(self):
		self.ds.save("record1") # create file with one line
		self.ds.save("record2") # append to file
		try:
			self.assertEqual(2, len(open(self.expectedFile).readlines()))
		finally:
			os.remove(self.expectedFile)
	def testSave_wrtiesArgumentAsLine(self):
		expectedLine = "some-record"
		self.ds.save(expectedLine)
		try:
			self.assertEqual(expectedLine, open(self.expectedFile).readlines()[0].rstrip())
		finally:
			os.remove(self.expectedFile)
