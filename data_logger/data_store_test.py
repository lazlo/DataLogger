import unittest
import os

import data_store
import data_record

def read_file_lines(filename):
	lines = []
	f = open(filename)
	for line in f.readlines():
		lines.append(line.rstrip())
	f.close()
	return lines

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
		for i in range(0, 3):
			self.ds.data_records.append(data_record.DataRecord())
		self.ds.save()
		try:
			self.assertEqual(0, len(self.ds.data_records))
		finally:
			os.remove(self.expectedFile)

	def testSave_writesDataRecordsToFileOneLineEach(self):
		expected = []
		for i in range(0, 4):
			dr = data_record.DataRecord()
			expected.append("%s\n" % dr.to_json())
			self.ds.data_records.append(dr)
		self.ds.save()
		try:
			self.assertEqual(expected, open(self.expectedFile).readlines())
		finally:
			os.remove(self.expectedFile)

	def testSave_appendsToFileInDataDir(self):
		self.ds.data_records.append(data_record.DataRecord())
		self.ds.save() # create file with one line
		self.ds.data_records.append(data_record.DataRecord())
		self.ds.save() # append to file
		try:
			self.assertEqual(2, len(open(self.expectedFile).readlines()))
		finally:
			os.remove(self.expectedFile)

	def testSave_writesDataRecordAsJSONtoFile(self):
		dr = data_record.DataRecord()
		expected = dr.to_json()
		self.ds.data_records.append(dr)
		self.ds.save()
		try:
			self.assertEqual([expected], read_file_lines(self.expectedFile))
		finally:
			os.remove(self.expectedFile)

	"""
	def testRecords_returnsNumberOfLines(self):
		for i in range(0, 3):
			self.ds.data_records.append(data_record.DataRecord())
		self.ds.save()
		try:
			self.assertEqual(3, self.ds.records())
		finally:
			os.remove(self.expectedFile)
	"""

	def testReadOldest_returnsFirstLine(self):
		dr = data_record.DataRecord("magic-timestamp-used-for-this-test")
		expected = dr.to_json()
		self.ds.data_records.append(dr)
		self.ds.data_records.append(data_record.DataRecord())
		self.ds.data_records.append(data_record.DataRecord())
		self.ds.save()
		try:
			# FIXME - make sure read oldest() will strip new-line characters
			self.assertEqual("%s" % expected, self.ds.read_oldest())
		finally:
			os.remove(self.expectedFile)

	def testDropOldest_removesFirstLine(self):
		for i in range(0, 3):
			self.ds.data_records.append(data_record.DataRecord())
		self.ds.save()
		self.ds.drop_oldest()
		try:
			self.assertEqual(2, self.ds.records())
		finally:
			os.remove(self.expectedFile)
