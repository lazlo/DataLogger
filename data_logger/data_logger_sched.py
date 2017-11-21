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

	def update(self):
		for t in self.tasks:
			if t["delay_sec"] > 0:
				t["delay_sec"] -= 1
			if t["delay_sec"] == 0:
				t["do_run"] = True

	def dispatch(self):
		for t in self.tasks:
			if not t["do_run"]:
				continue
			t["fp"]()
			t["do_run"] = False
			t["delay_sec"] = t["period_sec"]
