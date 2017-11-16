import unittest

import video
import data_input

class VideoTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Room 1 Camera"
		self.v = video.Video(self.expectedName)

	def testIsSubclassOfDataInput(self):
		self.assertEqual(True, issubclass(video.Video, data_input.DataInput))

	def testGetData_returnsDict(self):
		self.assertEqual(True, isinstance(self.v.get_data(), dict))
