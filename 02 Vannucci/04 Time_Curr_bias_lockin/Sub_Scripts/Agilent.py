import visa

class Agilent():
    def read_data_write(self, agilent):
        agilent.write('READ?')
    
    def AC_Curr_write(self, agilent):
        agilent.write('MEAS:CURR:AC?')
        
    def DC_Curr_write(self, agilent):
        agilent.write('MEAS:CURR:DC?')
    
    def AC_Volt_write(self, agilent):
        agilent.write('MEAS:VOLT:AC?')
        
    def DC_Volt_write(self, agilent):
        agilent.write('MEAS:VOLT:DC?')
        
    def Resistance_write(self, agilent):
        agilent.write('MEAS:RES?')
    
    def read_data_read(self, agilent):
        value = agilent.read()
        return value
