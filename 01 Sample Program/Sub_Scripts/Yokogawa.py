import visa

class Yokogawa():
    def Output_On(self, yokogawa):
        yokogawa.write('OUTP ON')
    
    def Output_Off(self, yokogawa):
        yokogawa.write('OUTP OFF')
        
    def Source_Voltage(self, yokogawa):
        yokogawa.write('SOUR:FUNC VOLT')
    
    def Source_Current(self, yokogawa):
        yokogawa.write('SOUR:FUNC CURR')
        
    def Set_Voltage(self, yokogawa,value):
        yokogawa.write('SOUR:LEV:AUTO ' + str(value))
        
    def Voltage_Limit(self, yokogawa, value):
        yokogawa.write('SOUR:PROT:VOLT ' + str(value))
        
    def Current_Limit(self, yokogawa, value):
        yokogawa.write('SOUR:PROT:CURR ' + str(value))
        
    