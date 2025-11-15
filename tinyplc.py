#import RPi.GPIO as GPIO
#from machine import Timer
import time
from plcprog import loop, init

class Timer:
    PERIODIC = 1
    
    def __init__(self, period, mode, callback):
        self.period = period
        self.mode = mode
        self.callback = callback
        
        while(1):
            time.sleep(period/1000)
            self.callback()

class PLC:
    
    IN1 = 1
    IN2 = 2
    IN3 = 3
    IN4 = 4

    OUT1 = 5
    OUT2 = 6
    OUT3 = 7
    OUT4 = 8

class TinyPLC:
    _input_channels = [PLC.IN1, PLC.IN2, PLC.IN3, PLC.IN4]
    _output_channels = [PLC.OUT1, PLC.OUT2, PLC.OUT3, PLC.OUT4]

    def __init__(self):
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(self._input_channels, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.setup(self._output_channels, GPIO.OUT)
        pass
    
    def start(self, loopPeriod, loopCallback):
        # setup plc loop
        self._loopPeriod = loopPeriod
        self._loopCallback = loopCallback
        self._loopTimer = Timer(period=self._loopPeriod, mode=Timer.PERIODIC, callback=self._loopCallback)
        
    def stop(self):
        self._loopTimer.deinit()
        
    def period(self):
        return self._loopPeriod

if __name__ == "__main__":
    plc = TinyPLC()
    
    # run user init code
    init()
    
    # start plc loop
    plc.start(20, loop)