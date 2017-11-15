import unittest

import data_input

class DataInputTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Room 1 Temperature"
		self.di = data_input.DataInput(self.expectedName)

	def testName_isSet(self):
		self.assertEqual(self.expectedName, self.di.name)
	# name
	# type
	# source

if __name__ == "__main__":
	unittest.main()
