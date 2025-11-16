# MIT License
# 
# Copyright (c) 2025 Christoph Brennig
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from machine import Pin, Signal, Timer, I2C

def clamp(x, min_x, max_x):
    return max(min(max_x, x), min_x)

class TinyPLC:
    _input_channels = [10, 11, 12, 13]
    _output_channels = [6, 7, 8, 9, "LED"]
    
    # index of board led in output list
    BOARD_LED = len(_output_channels) - 1
    
    _inputs = [0 for x in range(len(_input_channels))]
    _outputs = [0 for x in range(len(_output_channels))]

    def __init__(self, initCallback, loopCallback, loopPeriod, verbose=False):
        # initialize TinyPLC instance
        self._loopPeriod = loopPeriod
        self._loopCallback = loopCallback
        self._initCallback = initCallback
        self._verboseOutput = verbose
        
        # I/Os
        for i in range(len(self._output_channels)):
            pin = Pin(self._output_channels[i], Pin.OUT)
            self._outputs[i] = Signal(pin, invert=False)
            self._outputs[i].off()
        
        for i in range(len(self._input_channels)):
            pin = Pin(self._input_channels[i], Pin.IN)
            self._inputs[i] = Signal(pin, invert=True)
            
        # I2C
        self._i2c = I2C(id=0, freq=400000, scl=Pin(17), sda=Pin(16))
        
        if self._verboseOutput:
            print("TinyPLC initialized")
    
    def verboseOutput(enable):
        self._verboseOutput = enable
    
    def start(self):
        # setup plc loop
        self._loopTimer = Timer(period=self._loopPeriod, mode=Timer.PERIODIC, callback=self.callbackWrapper)
        
        # run user init code
        self._initCallback(self)
        
    def callbackWrapper(self, t):
        # use a wrapper to eliminate the timer reference
        try:
            self._loopCallback(self)
        except KeyboardInterrupt:
            t.deinit()
        except Exception as e:
            raise e
        
    def stop(self):
        # stop plc loop function execution
        self._loopTimer.deinit()
        
    def period(self):
        # return plc loop period
        return self._loopPeriod
    
    ### OUTPUT METHODS ###
    
    def setOutput(self, num, state):
        # take care of lousy user inputs
        state = clamp(state, 0, 1)
        num = clamp(num, 0 , len(self._outputs) - 1)
        
        # set output state
        self._outputs[num].value(state)
        
        if self._verboseOutput:
            print("Output " + str(num) + " set to " + str(state))
        
    def toggleOutput(self, num):
        # toggle output state
        # num has to be checked for boundaries, as it is used as list index
        num = clamp(num, 0 , len(self._outputs) - 1)
        self.setOutput(num, (1 - self._outputs[num].value()))
    
    def setLED(self, state):
        # set the RPi Pico onboard LED
        self.setOutput(self.BOARD_LED, state)
        
    def toggleLED(self):
        # toggle the RPi Pico onboard LED
        self.toggleOutput(self.BOARD_LED)
        
    ### INPUT METHODS ###
        
    def getInput(self, num):
        num = clamp(num, 0 , len(self._inputs) - 1)
        return self._inputs[num].value()
    
    # ToDo: edge-detection
    
    ### SERIAL INTERFACES ###
    
    def serial_I2C(self):
        return self._i2c
        