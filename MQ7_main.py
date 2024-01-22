# Test for MQ-series drivers

from MQ7 import MQ7
import utime


class App:
	pin = 'P13' #change to PyCom analog pin# 
	baseVoltage = 5.0 #change to the voltage powering the Sensor
	ro = 9.654 # Lost the spec sheet to my sensor. So,i am navigating blind here. 
	           # play with the MQ7_RO_BASE value in MQ7.py file and calibrate the sensor by passing ro=-1 in sensor.calibrate() below, 
	           # so that the base resistance is nearly equal to MQ7_RO_BASE.
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
