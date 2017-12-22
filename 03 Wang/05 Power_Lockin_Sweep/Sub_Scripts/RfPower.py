import visa

class RfPower():
    def RST(self, Rf):
        Rf.write('*RST')
    
    def freq_mode_write(self, Rf):
        Rf.write('FREQ:MODE CW')
        
    def power_mode_write(self, Rf):
        Rf.write('POW:MODE CW')
        
    def set_freq_write(self, Rf, freq):
        Rf.write('FREQ' + ' ' + str(freq))
        
    def set_power_write(self, Rf, power):
        Rf.write('POW' + ' ' + str(power))
        
    def output_on_write(self, Rf):
        Rf.write('OUTP ON')
        
    def output_off_write(self, Rf):
        Rf.write('OUTP OFF')
        
    def read_onoff_write(self, rf):
        rf.write('OUTP?')

    def read_freq_write(self, Rf):
        Rf.write('FREQ?')

    def power_power_write(self, Rf):
        Rf.write('POW?')
    
    def read_freq_read(self, Rf):
        value = Rf.read()
        return value

