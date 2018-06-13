# network.py
# Used to determine if network has been configured

#!/usr/bin/python

from socket import *
from time import sleep

# Returns assigned IP address if network has been configured
#  Otherwise returns '000.000.000.000'
def checkForNetwork(timeout = 1000000):
  current_IP = '000.000.000.000'
  not_found = True
  while(not_found and timeout > 0):
    try:
      s = socket(AF_INET, SOCK_DGRAM)
      s.connect(("8.8.8.8", 80))
      current_IP = s.getsockname()[0]
      s.close()
      not_found = False
    except:
      sleep(.5)
      timeout = timeout - 1
  return current_IP
