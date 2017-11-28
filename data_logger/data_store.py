import os
import json

class DataStore():

	DEFAULT_FILENAME = "store.txt"

	def __init__(self, data_dir):
		if not os.path.exists(data_dir):
			raise IOError("No such file or directory: \"%s\"" % data_dir)
		if not os.access(data_dir, os.W_OK):
			raise IOError("Permission denied: \"%s\"" % data_dir)
		self.data_dir = data_dir
		self.recordFile = os.path.join(self.data_dir, self.DEFAULT_FILENAME)
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

	def read(self):
		rv = []
		for line in open(self.recordFile).readlines():
			rv.append(line.rstrip())
		return rv

	def read_latest(self, n=1):
		rv = []
		lines = self.read()
		return lines[-n:]

	def records(self):
		return len(self.read())

	def drop_by(self, filter_key, filter_value):
		if not type(filter_value) is list:
			filter_value = [filter_value]
		lines_in = []
		lines_out = []
		# get all lines from file
		lines_in = self.read()
		# filter out line we want to drop
		for line in lines_in:
			rec = json.loads(line)
			if rec[filter_key] in filter_value:
				continue
			lines_out.append(line)
		# write lines back to file
		f = open(self.recordFile, "w")
		for line in lines_out:
			f.write("%s\n" % line)
		f.close()
