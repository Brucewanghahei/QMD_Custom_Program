class Temp():
	
	def frequncy_sweep(self):
		while num < max(len(self.array_f_1[1]), len(self.array_f_2[1]), len(self.array_f_3[1])): 
			while self.pause_collecting:
				if self.stop_collecting:
					break
				else:
					pass
			if not self.stop_collecting:
				self.run_time = time.time()
				time.sleep(self.Yokogawa_collect_step) # Time sleep
				self.agilent1.timeout = 100000  
				if num < len(self.array_1[1]):
					input_volt = str(float(self.array_1[1][num]) * 1E-3)
					self.yokogawa1.write('SOUR:LEV:AUTO ' + input_volt)
					self.power_sweep("Yokogawa1", float(input_volt), num, Round)
			else:
				break
			
	def power_sweep(self):
		while num < max(len(self.array_p_1[1]), len(self.array_p_2[1]), len(self.array_p_3[1])):
			while self.pause_collecting:
				if self.stop_collecting:
					break
				else:
					pass
			if not self.stop_collecting:
				if num < len(self.array_1[1]):
					input_volt = str(float(self.array_1[1][num]) * 1E-3)
					self.yokogawa1.write('SOUR:LEV:AUTO ' + input_volt)
					self.voltage_sweep("Yokogawa1", float(input_volt), num, Round)
			else:
				break
			
	def voltage_sweep(self):
		while num < max(len(self.array_v_1[1]), len(self.array_v_2[1]), len(self.array_v_3[1])):
			while self.pause_collecting:
				if self.stop_collecting:
					break
				else:
					pass
			if not self.stop_collecting:
				if num < len(self.array_1[1]):
					input_volt = str(float(self.array_1[1][num]) * 1E-3)
					self.yokogawa1.write('SOUR:LEV:AUTO ' + input_volt)
					self.Reading("Yokogawa1", float(input_volt), num, Round)
			else:
				break
	
	def Reading(self, Agilent_1, Agilent_2, pre_amp_1, pre_amp_2):
		volt = self.Average.Avg_Collect(self.Agilent_1, self.pre_amp_1)
		diff_resist = self.Average.Diff_Resist_Collect(self.Agilent_2, self.diff_constant)
		self.Current1.append(current)
		self.Volt1.append(volt)
		self.DiffResist1.append(diff_resist)
		self.emit(SIGNAL('print_value'), "Yokogawa1", [self.total_during, self.during, input_volt, current, volt, self.Data[2][15]])
		self.setup_plot(self.curveWidgets[0], self.curves[0], [self.step, self.Current1], ['Current Step', "Step", "Current (A)"])
		self.setup_plot(self.curveWidgets[3], self.curves[3], [self.Current1, self.DiffResist1], ["Differential Resistance vs Current In", "Current (A)", "Differential Resistance (Ohms)"])
		self.setup_plot(self.curveWidgets[2], self.curves[2], [self.Current1, self.Volt1], ["Voltage Out vs Current In", "Current (A)", "Voltage (V)"])
		self.Pre_dynamic_save(num, False, [current, volt, stdv, diff_resist], 2, Round)
		
		
		
			
