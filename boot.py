# boot.py -- run on boot-up
# --------------------------------------------------
# Author: avsg8, (https://github.com/avsg8), 01/2024

from BaseMQ import BaseMQ 
from micropython import const
import machine
# select which "main" file you want to run once the device boots
#machine.main('MQ7_main.py')
machine.main('main.py')
