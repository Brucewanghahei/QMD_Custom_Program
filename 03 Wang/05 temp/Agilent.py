
import visa
VISA_MOD_AVAILABLE = True
rm = visa.ResourceManager()
import time
visas = rm.list_resources()
print visas

Agilent = rm.open_resource(visas[0])
Agilent.write('SAMP:COUN 3')
Agilent.write('TRIG:SOUR BUS')
Agilent.write('INIT')
Agilent.write('*TRG')
t1 = time.time()
#time.sleep(4)
#print Agilent.query('*IDN?')
string_ = Agilent.query('FETCH?').replace("\n", "")
t2 = time.time()
print t2 - t1
print string_
list_ = string_.split(",")
total = 0
for i in range(0, len(list_)):
    total += float(list_[i])
avg = total/float(len(list_))
print avg

print list_