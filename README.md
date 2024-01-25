# A micropython-enabled ESP32 board (Pycom FiPy) streaming gas sensor (MQ sensors e.g. MQ2, MQ7 etc.) data in realtime to a node-red dashboard and sending critical alerts as push notifications on your phone

## Realtime streaming of noxious gas levels (CO, LPG) from MQ gas sensors connected to a PyCom FipY (or WiPy) microcontroller that runs micropython. The data is streamed into a Aedes MQTT broker hosted on a device in local network (raspberry pi or a computer) that is running a node-red server. 

The gas sensing code is from kartun83 (github account) and can be found here: https://github.com/kartun83/micropython-MQ/tree/master. The gas sensing MQ codes have been modified so it can be run on a PyCom device. 

I AM CURRENTLY NOT SURE ABOUT THE ACCURACY OF MY SENSOR VALUES AND AM FINDING IT HARD TO CALIBRATE IT. SO, THIS IS JUST A WORK IN PROGRESS.
