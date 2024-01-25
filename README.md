# A micropython-enabled ESP32 board (Pycom FiPy) streaming gas sensor (MQ sensors e.g. MQ2, MQ7 etc.) data in realtime to a node-red dashboard and sending critical alerts as push notifications to your phone (simplepush.io)
What this project is about: 

Realtime streaming of noxious gas levels (CO, LPG) from MQ gas sensors connected to a PyCom FipY (or WiPy) microcontroller that runs micropython. The data is streamed into a Aedes MQTT broker hosted on a device in local network (raspberry pi or a computer) that is running a node-red server. When gas levels reach a pre-defined critical threshold, the microcontroller uses internet connectivity to send a push notification to your phone in addition to sending the data to the node-red server.

Caveat: 

I AM CURRENTLY NOT SURE ABOUT THE ACCURACY OF MY SENSOR VALUES AND AM FINDING IT HARD TO CALIBRATE IT. I HAVE LOST THE SPEC SHEET TO THESE SENSORS AND DON'T REALLY REMEMBER WHERE I PROCURED THEM FROM. SO I AM NOT VERY SURE ABOUT ITS INTERNAL RESISTANCE OR IF THE CALIBRATION CURVE OF MY SENSOR MATCHES THAT OF THE SENSOR MENTIONED IN KARTUN83' REPO. SO PPM VALUES ARE MOST PROBABLY ONLY GOOD FOR SELF COMPARISONS (LEVELS RISING / FALLING IN RELATION TO IT OWN PAST VALUES). THIS IS JUST A WORK IN PROGRESS.

## Major Code Components:
### Gas sensing code:
The gas sensing code is from kartun83 (github account) and can be found here: https://github.com/kartun83/micropython-MQ/tree/master. The gas sensing MQ codes have been modified so it can be run on a PyCom device. 
### MQTT Code:
To achieve mqtt publishing to the local nodered broker from the microcontroller side, I have used micropython's umqtt-simple2 library. To create the local node-red broker, I have used a raspberry pi connected to the local network running a Aedes MQTT broker. Code and images for this are relatively simple and are present in the "images" folder.
### Push Notification to Phone:
I wanted to send a push notification from the microcontroller directly to my phone without using another device like a raspberry-pi as intermidiate, doing the job for it, when levels reach critical values. 
This can be done in a variety of ways. E.g. you could use Twilio's messaging services or AWS's SNS service in conjunction with their IoT Core. A few years back it would have been very simple to do. But due to current telecom regulations, you need to first buy and verify a number as a "sending entity". This may take time and money. And since I am not willing to wait so long for my hobby, I have gone with Simplepush.io's services. As per the current info on their site, they allow 10 msgs/month for free and without signup. You need to download and install the simplepush app from the app store on your phone to receive notifications, though. You also need to note down the "key" of your app on your phone, and supply that key in the code here for successfully sending notifications over the internet.

Simplepush has their own python library which can be leveraged to send push notifications (https://github.com/simplepush/simplepush-python). However, I wanted to simplify things and use bare-minimum space and components to acheive this. So, I ported the parse & request modules from micropython's urllib to achieve this. That meant porting libraries like micropython-collections, micropython-requests, micropython-urllib-parse on to the device to make a url connection to simplepush.io that sends push notifications to your phone. The source of these libraries are indicated on the top of their codes.
