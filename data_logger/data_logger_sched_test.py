import unittest

import data_logger_sched

testTask1_called = False

def testTask1():
	global testTask1_called
	testTask1_called = True

def testTask2():
	return

def testTask3():
	return

class DataLoggerSchedTestCase(unittest.TestCase):

	def setUp(self):
		self.sch = data_logger_sched.DataLoggerScheduler()

	#
	# __init__()
	#

	def testInit_taskListIsEmpty(self):
		self.assertEqual(0, len(self.sch.tasks))

	#
	# add()
	#

	def testAdd_insertsTaskIntoTaskList(self):
		self.sch.add(testTask1, 1, 0)
		self.sch.add(testTask2, 1, 0)
		self.sch.add(testTask3, 1, 0)
		self.assertEqual(3, len(self.sch.tasks))

	def testAdd_insertsTaskIntoTaskListWithFirstArgumentAsFunctionPointer(self):
		self.sch.add(testTask1, 1, 0)
		self.assertEqual(testTask1, self.sch.tasks[0]["fp"])

	def testAdd_insertsTaskIntoTaskListWithSecondArgumentPeriodInSeconds(self):
		period_sec = 20
		self.sch.add(testTask1, period_sec, 0)
		self.assertEqual(period_sec, self.sch.tasks[0]["period_sec"])

	def testAdd_insertsTaskIntoTaskListWithThirdArgumentDelayInSeconds(self):
		delay_sec = 10
		self.sch.add(testTask1, 15, delay_sec)
		self.assertEqual(delay_sec, self.sch.tasks[0]["delay_sec"])

	def testAdd_insertsTaskWithDoRunSetToFalse(self):
		self.sch.add(testTask1, 90, 0)
		self.assertEqual(False, self.sch.tasks[0]["do_run"])

	#
	# update()
	#

	def testUpdate_decrementsTaskDelaySecIfNotZero(self):
		self.sch.add(testTask3, 0, 10)
		self.sch.update()
		self.sch.update()
		self.sch.update()
		self.assertEqual(7, self.sch.tasks[0]["delay_sec"])

	def testUpdate_decrementsTaskDelaySecOnlyWhenGreaterZero(self):
		self.sch.add(testTask2, 0, 2)
		self.sch.update()
		self.sch.update()
		self.sch.update()
		self.assertEqual(0, self.sch.tasks[0]["delay_sec"])

	def testUpdate_setsDoRunTrueWhenDelaySecBecomesZero(self):
		self.sch.add(testTask2, 0, 2)
		self.sch.update()
		self.sch.update()
		self.assertEqual(True, self.sch.tasks[0]["do_run"])

	#
	# dispatch()
	#

	def testDispatch_executesTaskWhereDoRunIsTrue(self):
		global testTask1_called
		testTask1_called = False
		self.sch.add(testTask1, 0, 0)
		self.sch.update()
		self.sch.dispatch()
		self.assertEqual(True, testTask1_called)

	def testDispatch_setsDoRunFalseAfterTaskWasExecuted(self):
		self.sch.add(testTask1, 0, 0)
		self.sch.update()
		self.sch.dispatch()
		self.assertEqual(False, self.sch.tasks[0]["do_run"])

	def testDispatch_reloadsDelayWithPeriodAfterTaskWasExecuted(self):
		period_sec = 10
		self.sch.add(testTask1, period_sec, 0)
		self.sch.update()
		self.sch.dispatch()
		self.assertEqual(period_sec, self.sch.tasks[0]["delay_sec"])
