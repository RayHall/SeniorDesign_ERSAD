# GPS.py
# Used to access latitude and longitude via UART "ttyS0"
#   from an Adafruit Ultimate GPS chip

#!/usr/bin/python

from serial import Serial
from time import sleep

# Returns latitude and longitude as string
#   If not found, returns '00.000000'
#   Otherwise returns lat/lon in format '##.######'
def getLocation(timeout = 1000000):

  # Open the serial port
  ser = Serial()
  ser.baudrate = 9600
  ser.port = '/dev/ttyS0'
  not_open = True
  while (not_open and timeout > 0):
    try:
      ser.open()
      not_open = False
    # An exception will be thrown if serial port fails to open
    except:
      timeout = timeout - 1
      sleep(1)

  # Retrieve latitude and longitude
  lat = '00.000000'
  lon = '00.000000'
  not_found = True
  while (timeout > 0 and not_found):
    rcv = ser.read(250)
    index = rcv.find("$GPRMC")
    # index == -1 if key not found
    if (index != -1 and index < 225):
      start = index + 18
      end = start + 1
      if rcv[start:(start+1)] == "A": # GPS data valid
        lat = (rcv[(start+2):(start+4)] + "." +
              rcv[(start+4):(start+6)] + rcv[(start+7):(start+11)])
        lon = (rcv[(start+15):(start+17)] + "." +
              rcv[(start+17):(start+19)] + rcv[(start+20):(start+24)])
        not_found = False
      else:
        timeout = timeout - 1
        sleep(1)
  if ser.is_open:
    ser.close()

  print lat
  print lon
  return (lat, lon)
