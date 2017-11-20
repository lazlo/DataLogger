import os

class DataStore():

	def __init__(self, data_dir):
		if not os.path.exists(data_dir):
			raise IOError("No such file or directory: \"%s\"" % data_dir)
		if not os.access(data_dir, os.W_OK):
			raise IOError("Permission denied: \"%s\"" % data_dir)
		self.data_dir = data_dir
		self.recordFile = os.path.join(self.data_dir, "foo.txt")

	def save(self, line):
		f = open(self.recordFile, "a")
		f.write("%s\n" % line)
		f.close()

	def records(self):
		return len(open(self.recordFile).readlines())

	def read_oldest(self):
		return open(self.recordFile).readline().rstrip()
