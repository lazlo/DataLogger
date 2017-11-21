class DataLoggerTask():

	def __init__(self, fp, period_sec, delay_sec):
		self.fp = fp
		self.period_sec = period_sec
		self.delay_sec = delay_sec
		self.do_run = False

class DataLoggerScheduler():

	def __init__(self):
		self.tasks = []

	def add(self, fp, period_sec, delay_sec):
		task = DataLoggerTask(fp, period_sec, delay_sec)
		self.tasks.append(task)

	def update(self):
		for t in self.tasks:
			if t.delay_sec > 0:
				t.delay_sec -= 1
			if t.delay_sec == 0:
				t.do_run = True

	def dispatch(self):
		for t in self.tasks:
			if not t.do_run:
				continue
			t.fp()
			t.do_run = False
			t.delay_sec = t.period_sec
