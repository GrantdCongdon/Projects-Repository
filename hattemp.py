from sense_hat import SenseHat
from time import sleep
from time import time
import os
sense=SenseHat()

temp=round(sense.get_temperature()*1.8+32)
humidity=round(sense.get_humidity())
pressure=round(sense.get_pressure())
message = "Temp is %d *F. Humidity is %d percent. Pressure is %d milibars."%(
    temp,humidity,pressure)
sense.show_message(message, scroll_speed=(.003),back_colour=(255,0,0),
                   text_colour=(255,255,255))
sense.clear()
print(message)
