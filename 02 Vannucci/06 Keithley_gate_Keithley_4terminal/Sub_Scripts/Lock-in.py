class Lockin():
    
    self.sens= ['100','200','500','1','2','5','10','20','50','100','200','500','1','2','5','10','20','50','100','200','500']
    self.qfactor = ['1','2','5','10','20','50','100']
    self.tc = ['500 us','1 ms','3 ms','10 ms','30 ms', '100 ms','300 ms','1 s','3 s','10 s','30 s','100 s','300 s']
    
    def Read(self, inst):
        return inst.read()

    def Sensitivity(self, inst):
        inst.write('SENS?')
        num = inst.read()
        return self.sens[num]
    
    def Freq(self, inst):
        inst.ask('FREQ?')
        
    def TrimFreq(self, inst):
        inst.ask('IFFR?')
        
    def Phase(self, inst):
        inst.ask('PHAS?')
        
    def Amplitude(self, inst):
        inst.ask('SLVL?')
        
    def QFacotr(self, inst):
        inst.write('QFCT?')
        num = inst.read
        return self.qfactor[num]
    
    def TimeConstant(self, inst):
        inst.write('OFLT?')
        num = inst.read
        return self.tc[num]