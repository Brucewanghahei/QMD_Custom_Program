class DigitalLockin():
    def XYRTHET_query(self, lockin, a, b, c):
        a = lockin.query('SNAP? ' + str(a) + ',' + str(b) + ',' + str(c)).replace("\n", "")
        return a
    
    def param_query(self, lockin):
        a = []
        b = [ 'Sensitivity', 'Phase', 'Amplitude', 'Level', 'Int Freq', 'Ext Freq', 'Filter', 'Time Const', 'Inp Range Low-High', 'Inp Range 1V-10mV', 'Input', 'Voltage A A-B', 'Voltage ac dc', 'Voltage float ground', 'Current 1uA 10nA']
        c = [ 'SCAL?', 'OUTP? PHA', 'OUTP? SAM', 'OUTP? LEV', 'OUTP? FINT', 'OUTP? FEXT', 'OFSL?', 'OFLT?', 'ILVL?', 'IRNG?', 'IVMD?', 'ISRC?', 'ICPL?', 'IGND?', 'ICUR?']
        s = ['1V','500mV','200mV','100mV','50mV','20mV','10mV','5mV','2mV','1mV','500uV','200uV','100uV','50uV','20uV','10uV','5uV','2uV','1uV','500nV','200nV','100nV','50nV','20nV','10nV','5nV','2nV','1nV']
        t = ['1us','3us','10us','30us','100us','300us','1ms','3ms','10ms','30ms','100ms','300ms','1s','3s','10s','30s','100s','300s','1ks','3ks','10ks','30ks']
        d = [s, -1 , -1 , -1 , -1 , -1 , ['6dB/oct','12dB/oct','18dB/oct','24dB/oct'], t, ['lev 0','lev 1','lev 2','lev 3','lev 4'], ['1V','300mV', '100mV', '30mV','10mV'], ['Voltage','Current'], ['A','A-B'], ['AC','DC'], ['float','ground'], ['1uA','10nA']]
        
        for i in range(0,15):
            y = lockin.query(c[i]).replace("\n", "")
            if d[i] == -1 :
                a.append(y)
            else:
                x = int(y)
                a.append(d[i][x])
        e = [a, b]
        return e
    