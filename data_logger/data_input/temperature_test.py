import unittest
import os

import temperature

class TemperatureTestCase(unittest.TestCase):

	def setUp(self):
		self.expectedName = "Room 42"
		self.expectedFile = "test-sensor-file.txt"
		self.expectedArgs = {"path": self.expectedFile}
		self.expectedLines = []
		self.expectedLines.append("81 01 4b 01 7f ff 0c 10 9c : crc=9c YES\n")
		self.expectedLines.append("81 01 4b 01 7f ff 0c 10 9c t=24062\n")

		self._init_fake_sensor_file(self.expectedFile, self.expectedLines)

		self.t = temperature.Temperature(self.expectedName, self.expectedArgs)

	def tearDown(self):
		os.remove(self.expectedFile)

	def _init_fake_sensor_file(self, path, lines):
		f = open(path, "w")
		for line in lines:
			f.write(line)
		f.close()

	def testGetData_returnsFloat(self):
		self.assertEqual(True, type(self.t.get_data()) is float)

	def testGetData_readsLinesFromFileSpecifiedAsPath(self):
		self.t.get_data()
		self.assertEqual(self.expectedLines, self.t.lines)

	def testGetData_parsesTemperatureInCelsiusAsFloatFromLines(self):
		self.assertEqual(24.062, self.t.get_data())
