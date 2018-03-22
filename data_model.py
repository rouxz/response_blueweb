class ReportResponseTime():
	def __init__(self):
		self.responseTime = {}
		
	def add_measurement(self, step, duration):
		""" Add a measurement of response time at step """
		if not(step in self.responseTime):
			self.responseTime[step] = (1, duration)
		else:
			(i, dd) = self.responseTime[step]
			self.responseTime[step] = (i+1, dd + duration)
			
	def print(self):
		""" Print what we saw"""
		for (i, (n, d)) in self.responseTime.items():
			print("Step: ", i ," : " + "occurences : " , n , " , total duration : ", d)