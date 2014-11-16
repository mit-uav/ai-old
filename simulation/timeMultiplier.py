import time

class TimeMultiplier:

	def __init__ (self, k):
		self.startTime = time.time()
		self.k = k

	def getTime(self):
		return self.k*(time.time()-self.startTime)