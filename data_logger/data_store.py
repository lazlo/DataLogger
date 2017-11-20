import os

class DataStore():

	DEFAULT_DATA_DIR = "/var/lib/data-logger"

	def __init__(self, data_dir = None):
		self.data_dir = self.DEFAULT_DATA_DIR
		if data_dir:
			self.data_dir = data_dir
		if not os.path.exists(self.data_dir):
			raise Exception()
		self.recordFile = os.path.join(self.data_dir, "foo.txt")

	def save(self, line):
		f = open(self.recordFile, "a")
		f.write("%s\n" % line)
		f.close()

	def records(self):
		return len(open(self.recordFile).readlines())
