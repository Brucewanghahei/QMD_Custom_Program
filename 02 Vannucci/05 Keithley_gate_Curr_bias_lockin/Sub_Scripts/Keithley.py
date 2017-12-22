import visa

class Keithley():
    def turn_on(self, keithley):
        keithley.write("OUTP ON\n")
    
    def set_voltage(self, keithley, value):
        keithley.write('TRACE:CLEar "defbuffer1"\n')
        keithley.write("ROUT:TERM FRONT\n")
        keithley.write('SENS:FUNC "CURR"\n')
        #keithley.write('SOUR:VOLT:RANG AUTO')
        keithley.write("SOUR:FUNC VOLT\n")
        keithley.write("SOUR:VOLT:READ:BACK 1\n")
        keithley.write("SOUR:VOLT " + str(value) + "\n")

    def set_4terminal(self, keithley):
        keithley.write('SENS:CURR:RSEN ON\n')

    def set_2terminal(self, keithley):
        keithley.write('SENS:CURR:RSEN OFF\n')
    
    def read_data_write(self, keithley):
        keithley.write('READ? "defbuffer1", SOUR, READ\n')

    def read_data_read(self, keithley):
        voltage, current = keithley.read().replace("\n", "").split(",")
        return [voltage, current]
    
    def turn_off(self, keithley):
        keithley.write("OUTP OFF\n")
            
    

    
