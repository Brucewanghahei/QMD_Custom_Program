import visa

class Keithley():
    def turn_on(self, keithley):
        keithley.write("OUTP ON")
    
    def set_voltage(self, keithley, value):
        keithley.write('TRACE:CLEar "defbuffer1"')
        keithley.write("ROUT:TERM FRONT")
        keithley.write('SENS:FUNC "CURR"')
        #keithley.write('SOUR:VOLT:RANG AUTO')
        keithley.write("SOUR:FUNC VOLT")
        keithley.write("SOUR:VOLT:READ:BACK 1")
        keithley.write("SOUR:VOLT " + str(value))
    
    def read_data_write(self, keithley):
        keithley.write('READ? "defbuffer1", SOUR, READ')
        
    def read_data_read(self, keithley):
        voltage, current = keithley.read().replace("\n", "").split(",")
        return [voltage, current]
    
    def turn_off(self, keithley):
        keithley.write("OUTP OFF")
            
    

    
