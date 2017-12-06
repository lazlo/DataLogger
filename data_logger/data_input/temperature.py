import sensor

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

	def get_data(self):
		path = self.args["path"]
		self.lines = self._read_file(path)
		return 0.0
