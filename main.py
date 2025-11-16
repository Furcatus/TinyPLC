from tinyplc import TinyPLC
import ahtx0

humtemp = 0

def init_sensor(plc):
    global humtemp
    
    humtemp = ahtx0.AHT20(plc.serial_I2C())
    print("Init")

def loop_sensor(plc):
    global humtemp
    
    print("T: %0.2f°C" % humtemp.temperature + "\nH: %0.2f%%" % humtemp.relative_humidity)
    
def init_io(plc):
    pass

def loop_io(plc):
    plc.toggleLED()
    plc.toggleOutput(0)

if __name__ == "__main__":
    plc1 = TinyPLC(init_sensor, loop_sensor, 1000)
    plc2 = TinyPLC(init_io, loop_io, 500)
    
    plc1.start()
    plc2.start()