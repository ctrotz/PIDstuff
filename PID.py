
class PIDController:
	def __init__(self,time, Kp=0, Ki=0, Kd=0):
		self._Kp = Kp
		self._Kd = Kd
		self._Ki = Ki

		self._integrator = 0
		self._error=0
		self._lastTime = time

	def update(self, error, time):
		P = self._Kp * error

		dt = float(time - self._lastTime)

		self._integrator += error * dt

		I = self._integrator * self._Ki
		errDiff = error - self._error
		diff = errDiff/dt if dt != 0 else 0
		D = self._Kd * diff
		PID = P + I + D

		self._lastTime = time

		self._error = error
		#print str(self._Kp)
		#print str(D)
		return PID


