class Magnet():
    def Read(self, Model):
        return Model.read()
    
    def Conf_field(self, Model, target):
        Model.write('CONF:FIELD:TARG ' + str(target))
        
    def Asking_field(self, Model):
        Model.write('FIELD: TARG?')
        
    def Conf_ramp_rate_field(self, Model, rate):
        Model.write('CONF:RAMP:RATE:FIELD: 1, ' + str(rate) + "," + str(rate))
        
    def Ramp_rate_field(self, Model):
        Model.write('RAMP:RATE:FIELD:1?')
        
    def Ramp(self, Model):
        Model.write('RAMP')
        
    def Pause(self, Model):
        Model.write('PAUSE')
        
    def Zero(self, Model):
        Model.write('ZERO')
        
    def Asking_state(self, Model):
        Model.write('STATE?')
        
    def Magnet_volt(self, Model):
        Model.write('VOLT:MAG?')
        
    def Supply_volt(self, Model):
        Model.write('VOLT:SUPP?')
        
    def Magnet_curr(self, Model):
        Model.write('CURR:MAG?')
        
    def Supply_curr(self, Model):
        Model.write('CURR:MAG?')
        
    def Magnet_field(self, Model):
        Model.write('FIELD:MAG?')
        
    def Quench(self, Model):
        Model.write('QUENCH?')