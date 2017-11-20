import os

class DataStore():

	def __init__(self, data_dir):
		if not os.path.exists(data_dir):
			raise IOError()
		if not os.access(data_dir, os.W_OK):
			raise IOError()
		self.data_dir = data_dir
		self.recordFile = os.path.join(self.data_dir, "foo.txt")

	def save(self, line):
		f = open(self.recordFile, "a")
		f.write("%s\n" % line)
		f.close()

	def records(self):
		return len(open(self.recordFile).readlines())
