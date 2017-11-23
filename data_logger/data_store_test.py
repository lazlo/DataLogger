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
		self.assertEqual("No such file or directory: \"%s\"" % expectedDir, ex.exception.message)

	def testInit_raiseExceptionWhenDataDirIsNotWritable(self):
		expectedDir = "/root"
		with self.assertRaises(IOError) as ex:
			# NOTE The test should never be run as root in the first
			# place. Otherwise this test will fail.
			data_store.DataStore(expectedDir)
		self.assertEqual("Permission denied: \"%s\"" % expectedDir, ex.exception.message)

	def testInit_dataDirIsSet(self):
		self.assertEqual(self.expectedDataDir, self.ds.data_dir)

	def testInit_dataRecordsIsOfTypeList(self):
		self.assertEqual(True, isinstance(self.ds.data_records, list))

	def testInit_dataRecordsIsEmpty(self):
		self.assertEqual(True, len(self.ds.data_records) == 0)

	#
	# save()
	#

	def testSave_createsFileInDataDir(self):
		self.ds.save()
		try:
			self.assertEqual(True, os.path.exists(self.expectedFile))
		finally:
			os.remove(self.expectedFile)

	def testSave_clearsDataRecords(self):
		self.ds.data_records.append("x1")
		self.ds.data_records.append("x2")
		self.ds.data_records.append("x3")
		self.ds.save()
		try:
			self.assertEqual(0, len(self.ds.data_records))
		finally:
			os.remove(self.expectedFile)

	def testSave_writesDataRecordsToFileOneLineEach(self):
		self.ds.data_records.append("this")
		self.ds.data_records.append("is")
		self.ds.data_records.append("a")
		self.ds.data_records.append("test")
		self.ds.save()
		try:
			self.assertEqual(["this\n", "is\n", "a\n", "test\n"], open(self.expectedFile).readlines())
		finally:
			os.remove(self.expectedFile)

	def testSave_appendsToFileInDataDir(self):
		self.ds.data_records.append("record1")
		self.ds.save() # create file with one line
		self.ds.data_records.append("record2")
		self.ds.save() # append to file
		try:
			self.assertEqual(2, len(open(self.expectedFile).readlines()))
		finally:
			os.remove(self.expectedFile)

	def testRecords_returnsNumberOfLines(self):
		self.ds.data_records.append("foo")
		self.ds.data_records.append("bar")
		self.ds.data_records.append("blub")
		self.ds.save()
		try:
			self.assertEqual(3, self.ds.records())
		finally:
			os.remove(self.expectedFile)

	def testReadOldest_returnsFirstLine(self):
		self.ds.data_records.append("first-line")
		self.ds.data_records.append("second-line")
		self.ds.data_records.append("third-line")
		self.ds.save()
		try:
			self.assertEqual("first-line", self.ds.read_oldest())
		finally:
			os.remove(self.expectedFile)

	def testDropOldest_removesFirstLine(self):
		self.ds.data_records.append("1st-line")
		self.ds.data_records.append("2nd-line")
		self.ds.data_records.append("3rd-line")
		self.ds.save()
		self.ds.drop_oldest()
		try:
			self.assertEqual(2, self.ds.records())
		finally:
			os.remove(self.expectedFile)
