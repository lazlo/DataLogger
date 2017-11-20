class DataStore():

	DEFAULT_DATA_DIR = "/var/lib/data-logger"

	def __init__(self, data_dir = None):
		self.data_dir = self.DEFAULT_DATA_DIR
		if data_dir:
			self.data_dir = data_dir

	def save(self):
		return
