#!/usr/bin/env python

# Based on http://stackoverflow.com/questions/22390064/use-dbus-to-just-send-a-message-in-python

# Python script to call the methods of the DBUS Test Server

import time
from pydbus import SessionBus

bus = SessionBus()
#the_object = bus.get("com.ioexp", "/io_expansion_board")
the_object = bus.get("com.simcom", "/sim7600")

# call the methods and print the results
reply1 = the_object.power_module(False)
print(reply1)
time.sleep(10)
reply2 = the_object.power_module(True)
print(reply2)

