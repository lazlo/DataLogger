class DataLoggerScheduler():

	def __init__(self):
		self.tasks = []

	def add(self, fp, period_sec, delay_sec):
		task = {}
		task.update({"fp": fp})
		task.update({"period_sec": period_sec})
		task.update({"delay_sec": delay_sec})
		task.update({"do_run": False})
		self.tasks.append(task)
