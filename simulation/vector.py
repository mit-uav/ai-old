import math

class Vector(object):

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.rad = math.atan2(self.y, self.x)

	def add(self, vector):
		self.x = self.x + vector.x
		self.y = self.y + vector.y
		self.z = self.z + vector.z

	def sub(self, vector):
		self.x = self.x - vector.x
		self.y = self.y - vector.y
		self.z = self.z - vector.z

	def scale(self, alpha):
		self.x = self.x * alpha
		self.y = self.y * alpha
		self.z = self.z * alpha

	def update_angle(self, theta):
		self.rad = self.rad + theta
		c = self.magnitude()
		self.x = c*math.cos(self.rad)
		self.y = c*math.sin(self.rad)

	def magnitude(self):
		return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

	def quadrant(self):
		if rad < math.pi/2:
			return 1
		elif rad < math.pi:
			return 2
		elif rad < 3*math.pi/2:
			return 3
		else:
			return 4

	def cross(self, vector):
		return this.x*this.x*vector.y*vector.y - this.y*this.y*vector.x*vector.x

