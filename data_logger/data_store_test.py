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

	def testInit_raisesExceptionWhenDataDirDoesNotExist(self):
		expectedDir = "/some/dir/that/does/not/exist"
		with self.assertRaises(IOError) as ex:
			data_store.DataStore(expectedDir)
		self.assertEqual("No such file or directory \"%s\"" % expectedDir, ex.exception.message)

	def testInit_raiseExceptionWhenDataDirIsNotWritable(self):
		expectedDir = "/root"
		with self.assertRaises(IOError) as ex:
			# NOTE The test should never be run as root in the first
			# place. Otherwise this test will fail.
			data_store.DataStore(expectedDir)
		self.assertEqual("Permission denied \"%s\"" % expectedDir, ex.exception.message)

	def testInit_dataDirIsSet(self):
		self.assertEqual(self.expectedDataDir, self.ds.data_dir)

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

	def testRecords_returnsNumberOfLines(self):
		self.ds.save("foo")
		self.ds.save("bar")
		self.ds.save("blub")
		try:
			self.assertEqual(3, self.ds.records())
		finally:
			os.remove(self.expectedFile)
