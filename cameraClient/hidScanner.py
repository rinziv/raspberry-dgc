import evdev
import requests
from evdev import *
import RPi.GPIO as GPIO
import signal
import time
import psutil
import socket

import logging
import logging.handlers

mlogger = logging.getLogger('hidScanner')
mlogger.setLevel(logging.INFO)

#handler = logging.handlers.SysLogHandler()
handler = logging.handlers.SysLogHandler(address='/dev/log', facility=logging.handlers.SysLogHandler.LOG_DAEMON)
#handler = logging.handlers.TimedRotatingFileHandler('hidScanner.log', when='d')

mlogger.addHandler(handler)


colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
R = 11
G = 12
B = 13


def check_verification():
    conns = psutil.net_connections()
    for i in conns:
      if i.type == socket.SOCK_STREAM:
        if i.laddr.port == 3000:
          return True 
    return False




def setup(Rpin, Gpin, Bpin):
   global pins
   global p_R, p_G, p_B
   pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
   GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
   for i in pins:
      GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
      GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

   p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
   p_G = GPIO.PWM(pins['pin_G'], 1999)
   p_B = GPIO.PWM(pins['pin_B'], 5000)

   p_R.start(100)      # Initial duty Cycle = 0(leds off)
   p_G.start(100)
   p_B.start(100)

def map(x, in_min, in_max, out_min, out_max):
   return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def on():
   p_R.start(100)      # Initial duty Cycle = 0(leds off)
   p_G.start(100)
   p_B.start(100)



def off(signum=None, frame=None):
   #print('turning led off')
   GPIO.setmode(GPIO.BOARD)
   for i in pins:
      GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
      GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds

def setColor(col):   # For example : col = 0x112233
   R_val = (col & 0xff0000) >> 16
   G_val = (col & 0x00ff00) >> 8
   B_val = (col & 0x0000ff) >> 0

   R_val = map(R_val, 0, 255, 0, 100)
   G_val = map(G_val, 0, 255, 0, 100)
   B_val = map(B_val, 0, 255, 0, 100)

   p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
   p_G.ChangeDutyCycle(100-G_val)
   p_B.ChangeDutyCycle(100-B_val)

def destroy(signum=None, frame=None):
   p_R.stop()
   p_G.stop()
   p_B.stop()
   off()
   #GPIO.cleanup()


print('waiting for the verification service to be up')
while not check_verification():
     time.sleep(2)
print('verification service is alive')



signal.signal(signal.SIGALRM, destroy)

## Starting configuration
setup(R, G, B)
off()




dev =evdev.InputDevice('/dev/input/by-id/usb-SM_SM-2D_PRODUCT_HID_KBW_APP-000000000-event-kbd')
#dev =evdev.InputDevice('/dev/input/event4')
dev.grab()
mlogger.info('starting listening to %s ',  dev)
#print(dev)

setColor(0x333333) #bianco
signal.alarm(5)


# for event in dev.read_loop():
#     if event.type == ecodes.EV_KEY:
#         print(categorize(event))

scancodes = { 
    # Scancode: ASCIICode 
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8', 
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r', 
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL', 
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';', 
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n', 
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT' 
} 

capscodes = { 
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*', 
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R', 
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL', 
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':', 
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N', 
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT' 
} 

def read_scan():
   #setup vars 
   x = '' 
   caps = False 

   #grab provides exclusive access to the device 


   #loop 
   for event in dev.read_loop(): 
    if event.type == ecodes.EV_KEY: 
     data = categorize(event) # Save the event temporarily to introspect it 
     if data.scancode == 42: 
      if data.keystate == 1: 
       caps = True 
      if data.keystate == 0: 
       caps = False 
     if data.keystate == 1: # Down events only 
      if caps: 
       key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) # Lookup or return UNKNOWN:XX 
      else: 
       key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) # Lookup or return UNKNOWN:XX 
      if (data.scancode != 42) and (data.scancode != 28): 
       x += key_lookup 
      if(data.scancode == 28): 
       #print (x)   # Print it all out!
       yield x 
       x = ''



code_generator = read_scan()
try:
  for i in code_generator:
    setColor(0x0000FF)
    mlogger.info('code %s', i)
    payload = {'dgc': i}
    r = requests.get('http://localhost:3000/', params=payload)
    mlogger.info('Return code: %s, Text: %s', r.status_code, r.text)
    if r.status_code == 200:
       on()
       setColor(0xFF00FF)
       signal.alarm(10)
    else:
       on()
       setColor(0x00FFFF)
       signal.alarm(10)
except KeyboardInterrupt:
    destroy()
    GPIO.cleanup()
