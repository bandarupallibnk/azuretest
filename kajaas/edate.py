import datetime
import time



class cl_date():
	def __init__(self):
		today = datetime.date.today()
		now = datetime.datetime.now()
		utctime = datetime.datetime.utcnow()
		time = now.strftime("%d_%m_%Y_%H_%M_%S")
		sutctime = utctime.strftime("%d%m%Y%H%M%S")
		self.currentdate =  today.strftime('%Y%m%d')
		self.sdatetime = time
		self.utcdatetime = sutctime

	def futcdatetime(self):
		return self.utcdatetime

	def fcurrentdate(self):
		return self.currentdate

	def fdatetime(self):
		return self.sdatetime
		