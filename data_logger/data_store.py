import os

class DataStore():

	def __init__(self, data_dir):
		if not os.path.exists(data_dir):
			raise IOError("No such file or directory: \"%s\"" % data_dir)
		if not os.access(data_dir, os.W_OK):
			raise IOError("Permission denied: \"%s\"" % data_dir)
		self.data_dir = data_dir
		self.recordFile = os.path.join(self.data_dir, "foo.txt")
		self.data_records = []

	def save(self):
		f = open(self.recordFile, "a")
		for dr in self.data_records:
			f.write("%s\n" % dr.to_json())
		f.close()
		# reset data_records
		self.data_records = []
		return

	def save_latest(self):
		latest_record_only = self.data_records[-1:]
		self.data_records = latest_record_only
		self.save()

	def records(self):
		return len(open(self.recordFile).readlines())

	def read_oldest(self):
		return open(self.recordFile).readline().rstrip()

	def drop_oldest(self):
		f = open(self.recordFile)
		lines = f.readlines()
		f.close()
		f = open(self.recordFile, "w")
		for line in lines[1:]:
			f.write(line)
		f.close()
