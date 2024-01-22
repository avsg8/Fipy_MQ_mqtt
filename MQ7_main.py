# Test for MQ-series drivers

from MQ7 import MQ7
import utime

pin = 'P13'
baseVoltage = 5
ro = 9.654 # if you want to calibrate it else, supply with values gotten from previous runs

class App:
	pin = 'P13'
	baseVoltage = 5
	ro = 9.654 
	def __init__(self, pin = pin):
		self.sensor = MQ7(pinData = pin, baseVoltage = baseVoltage)
		#self.sensor._ro = 0.7663 #0.2022838 # comment this line for the first run, calibrate and get the value. Then put the value here

	def Run(self):
		print("Calibrating")
		self.sensor.calibrate(ro = ro)
		print("Calibration completed")
		print("Base resistance:{0}".format(self.sensor._ro))
		val = self.sensor.readCarbonMonoxide()
		return val
		#while True:
		#	print("C0: {0}".format(self.sensor.readCarbonMonoxide()))
			#print("LPG: {0}".format(self.sensor.readLPG()))
			#print("Methane: {0}".format(self.sensor.readMethane()))
			#print("Hydrogen: {0}".format(self.sensor.readHydrogen()))
		#	utime.sleep(5)

if __name__=="__main__":
	val = App().Run()			
