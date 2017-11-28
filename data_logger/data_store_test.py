import unittest
import os
import time

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
		self.expectedFile = os.path.join(self.expectedDataDir, data_store.DataStore.DEFAULT_FILENAME)
		os.mkdir(self.expectedDataDir)
		self.ds = data_store.DataStore(self.expectedDataDir)

	def tearDown(self):
		if os.path.exists(self.expectedFile):
			os.remove(self.expectedFile)
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
		self.assertEqual(True, os.path.exists(self.expectedFile))

	def testSave_clearsDataRecords(self):
		for i in range(0, 3):
			self.ds.data_records.append(data_record.DataRecord())
		self.ds.save()
		self.assertEqual(0, len(self.ds.data_records))

	def testSave_writesDataRecordsToFileOneLineEach(self):
		expected = []
		for i in range(0, 4):
			dr = data_record.DataRecord()
			expected.append("%s\n" % dr.to_json())
			self.ds.data_records.append(dr)
		self.ds.save()
		self.assertEqual(expected, open(self.expectedFile).readlines())

	def testSave_appendsToFileInDataDir(self):
		self.ds.data_records.append(data_record.DataRecord())
		self.ds.save() # create file with one line
		self.ds.data_records.append(data_record.DataRecord())
		self.ds.save() # append to file
		self.assertEqual(2, len(open(self.expectedFile).readlines()))

	def testSave_writesDataRecordAsJSONtoFile(self):
		dr = data_record.DataRecord()
		expected = dr.to_json()
		self.ds.data_records.append(dr)
		self.ds.save()
		self.assertEqual([expected], read_file_lines(self.expectedFile))

	#
	# save_latest()
	#

	def testSaveLatest_onlyWritesLatestRecordToFile(self):
		expected = []
		for i in range(0, 10):
			dr = data_record.DataRecord()
			self.ds.data_records.append(dr)
			if i == 9:
				expected.append(dr.to_json())
		self.ds.save_latest()
		self.assertEqual(expected, read_file_lines(self.expectedFile))

	#
	# records()
	#

	def testRecords_returnsNumberOfLines(self):
		for i in range(0, 3):
			self.ds.data_records.append(data_record.DataRecord())
		self.ds.save()
		self.assertEqual(3, self.ds.records())

	#
	# read()
	#

	def testRead_returnsFileContents(self):
		expected = []
		for i in range(0, 3):
			dr = data_record.DataRecord()
			self.ds.data_records.append(dr)
			expected.append(dr.to_json())
		self.ds.save()
		self.assertEqual(expected, self.ds.read())

	#
	# read_latest()
	#

	def testReadLatest_returnsNLatestLine(self):
		expected = []
		for i in range(0, 10):
			ts = "2017-11-28T%02d:00:00" % (2 + i)
			dr = data_record.DataRecord(ts)
			self.ds.data_records.append(dr)
			if i > 7:
				expected.append(dr.to_json())
		self.ds.save()
		self.assertEqual(expected, self.ds.read_latest(2))

	#
	# drop_by()
	#

	def testDropBy_doesNotChangeFileOnMismatch(self):
		for i in range(0, 10):
			self.ds.data_records.append(data_record.DataRecord())
		self.ds.save()
		self.ds.drop_by("timestamp", "foo")
		self.assertEqual(10, self.ds.records())

	def testDropBy_removesLineFromFileOnMatch(self):
		t = time.gmtime()
		arg_filter_value = "1983-10-10T12:23:42"
		for i in range(0, 10):
			t = time.gmtime()
			# this is the special record we want to delete
			if i == 5:
				ts = arg_filter_value
			else:
				ts = time.strftime("%Y-%m-%dT%H:%M:%S", t)
			dr = data_record.DataRecord(ts)
			self.ds.data_records.append(dr)
		self.ds.save()
		self.ds.drop_by("timestamp", arg_filter_value)
		self.assertEqual(9, self.ds.records())

	def testDropBy_removesMultipleLinesFromFileOnMatch(self):
		t = time.gmtime()
		arg_filter_value = ["1983-10-10T12:23:42", "1983-10-10T12:23:53"]
		for i in range(0, 10):
			t = time.gmtime()
			# this is the special record we want to delete
			if i == 5:
				ts = arg_filter_value[0]
			elif i == 6:
				ts = arg_filter_value[1]
			else:
				ts = time.strftime("%Y-%m-%dT%H:%M:%S", t)
			dr = data_record.DataRecord(ts)
			self.ds.data_records.append(dr)
		self.ds.save()
		self.ds.drop_by("timestamp", arg_filter_value)
		self.assertEqual(8, self.ds.records())
