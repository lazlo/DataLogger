import sensor
import re

class Temperature(sensor.Sensor):

	def __init__(self, name, args):
		sensor.Sensor.__init__(self, name, args)
		self.lines = []

	def _read_file(self, path):
		lines = []
		f = open(path)
		for line in f.readlines():
			lines.append(line)
		f.close()
		return lines

	def _parse_temp_from_lines(self):
		m = re.search("t=(?P<temp>\d+)", self.lines[1])
		return float(m.group("temp")) / 1000.0

	def get_data(self):
		path = self.args["path"]
		self.lines = self._read_file(path)
		return self._parse_temp_from_lines()
