import visa
VISA_MOD_AVAILABLE = True
rm = visa.ResourceManager()
import time
import numpy
visas = rm.list_resources()
#print visas
#Aperture=(1,1)
point_list=(0,1,2)
Agilent = rm.open_resource(visas[0], timeout=10000000)
points = 10
NPCL = 1

Agilent.write('SENS:VOLT:DC:NPLC '+ str(NPCL))          #set Aperture
Agilent.write('SAMP:COUN '+ str(points))
Agilent.write('INIT')

for x in point_list:
        
    #NPCL = input('Aperture PCL?(0.02,0.2,1,10,100)')       #ask for Apature setting 
    #print NPCL
    t1 = time.time()
    #Agilent.write('CONF:VOLT:DC')                           #set to dc
    #Agilent.write('SENS:VOLT:DC:NPLC '+ str(NPCL))          #set Aperture
    #gilent.write('SAMP:COUN '+ str(points))                #set number of points
    #Agilent.write('TRIG:SOUR BUS')
    Agilent.write('*TRG')
    Agilent.write('FETCH?')
    string_ = Agilent.read().replace("\n", "")
    t2 = time.time()
    list_=numpy.fromstring(string_, dtype = numpy.float32, count=points,sep=',')
    #print string_
    print list_
    print ""
print ''



