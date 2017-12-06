class DataInput():

	def __init__(self, name, args=None):
		self.name = name
		self.args = args

	def get_data(self):
		raise NotImplementedError()
