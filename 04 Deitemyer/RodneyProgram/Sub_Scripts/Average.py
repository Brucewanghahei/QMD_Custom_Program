import visa
import numpy

class Average():
	
	def Avg_DC_Volt_write(self, Agilent, Aperture, points):
		Agilent.write('SENS:VOLT:DC:NPLC '+ str(Aperture))         
		Agilent.write('SAMP:COUN '+ str(points))
		Agilent.write('INIT')
	
	def Diff_DC_Volt_write(self, Agilent):         
		Agilent.write('CONF:VOLT:DC')
		Agilent.write('INIT')
		
	def Avg_Collect(self, Agilent, pre_amp_1):
		Agilent.write('*TRG')
		Agilent.write('FETCH?')
		string_ = Agilent.read().replace("\n", "")
		list_=numpy.fromstring(string_, dtype = numpy.float32, count=points,sep=',')
		volt = numpy.mean(list_)/ pre_amp_1
		return volt
	
	def Diff_Resist_Collect(self, Agilent, diff_constant):
		self.Agilent.write('*TRG')
		self.Agilent.write('FETCH?')
		lockin_volt = float(self.Agilent.read().replace("\n", ""))
		diff_resist = (lockin_volt* diff_constant)
		return diff_resist
	
	