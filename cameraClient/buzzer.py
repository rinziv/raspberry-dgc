
#!/usr/bin/env python
#---------------------------------------------------
#
#       This is a program for Passive Buzzer Module
#               It will play simple songs.
#       You could try to make songs by youselves!
#
#               Passive buzzer                     Pi
#                       VCC ----------------- 3.3V
#                       GND ------------------ GND
#                       SIG ---------------- Pin 11
#
#---------------------------------------------------

import RPi.GPIO as GPIO
import time

Buzzer = 7

def setup():
        GPIO.setmode(GPIO.BOARD)                # Numbers GPIOs by physical location
        GPIO.setup(Buzzer, GPIO.OUT)    # Set pins' mode is output
        global Buzz                                             # Assign a global variable to replace GPIO.PWM
        Buzz = GPIO.PWM(Buzzer, 440)    # 440 is initial frequency.
        Buzz.start(50)                                  # Start Buzzer pin with 50% duty ration


def success():
       for  i in [0,1]:
          Buzz.start(20)
          Buzz.ChangeFrequency(990)
          time.sleep(.1)
          Buzz.stop()
          time.sleep(.2)


def fail():
       for  i in [0,1]:
          Buzz.start(90)
          Buzz.ChangeFrequency(248)
          time.sleep(.3)
          Buzz.stop()
          time.sleep(.2)


def loop():
        while True:
                success()
                time.sleep(2)
                fail()
                time.sleep(2)

def destory():
        Buzz.stop()                                     # Stop the buzzer
        GPIO.output(Buzzer, 1)          # Set Buzzer pin to High
        GPIO.cleanup()                          # Release resource

if __name__ == '__main__':              # Program start from here
        setup()
        try:
                loop()
        except KeyboardInterrupt:       # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                destory()

