# A micropython-enabled ESP32 board (Pycom FiPy) streaming gas sensor (MQ sensors e.g. MQ2, MQ7 etc.) data in realtime to a node-red dashboard and sending critical alerts as push notifications to your phone

### Realtime streaming of noxious gas levels (CO, LPG) from MQ gas sensors connected to a PyCom FipY (or WiPy) microcontroller that runs micropython. The data is streamed into a Aedes MQTT broker hosted on a device in local network (raspberry pi or a computer) that is running a node-red server. When gas levels reach a pre-defined critical threshold, the microcontroller uses internet connectivity to send a push notification to your phone.

The gas sensing code is from kartun83 (github account) and can be found here: https://github.com/kartun83/micropython-MQ/tree/master. The gas sensing MQ codes have been modified so it can be run on a PyCom device. 

I AM CURRENTLY NOT SURE ABOUT THE ACCURACY OF MY SENSOR VALUES AND AM FINDING IT HARD TO CALIBRATE IT. I HAVE LOST THE SPEC SHEET TO THESE SENSORS AND DON'T REALLY REMEMBER WHERE I PROCURED THEM FROM. SO I AM NOT VERY SURE ABOUT ITS INTERNAL RESISTANCE OR IF THE CALIBRATION CURVE OF MY SENSOR MATCHES THAT OF THE SENSOR MENTIONED IN KARTUN83' REPO. SO PPM VALUES ARE MOST PROBABLY ONLY GOOD FOR SELF COMPARISONS (LEVELS RISING / FALLING IN RELATION TO IT OWN PAST VALUES). THIS IS JUST A WORK IN PROGRESS.

I have ported micropython-collections, micropython-requests, micropython-urllib-parse to make a url connection to simplepush.io that sends push notifications to your phone. You need to download install the simplepush app from the app store on your phone to receive notifications.
