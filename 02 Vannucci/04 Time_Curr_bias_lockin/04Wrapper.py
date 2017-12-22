"""Written by Bruce Wang.
    Inspired and helped by Johnathon Vannucci.
    Contact wdmzcjwq@gmail.com if you have any questions"""

"""To compile the .ui file into .py file, it is very simple. Do the following stpes:
   1. Open Command Proment (Terminal if you are using mac), using 'cd' to get the directory that contains the .ui file
   2. Type "pyuic4 -x filename.ui -o filename.py"
   3. If nothing strange happens, it means a .py file is successfully created in the same directory contains your original .ui file
   4. Do not change any of the code in the .py file because recomling any new changes in the .ui file will delete your changes"""

# Import os library
import os, inspect

# These are the modules required for the guiqwt widgets.
# Import plot widget base class
from guiqwt.pyplot import *
from guiqwt.plot import CurveWidget
from guiqwt.builder import make

from scipy import signal

import string

# Import system library
import sys

# Import datetime
from datetime import datetime
now = datetime.now()

# Import the visa library
try:
    import visa
    visa_available = True
except:
    visa_available = False

# Import numpy library
import numpy

# Import pylab library 
# It contains some functions necessary to create some of the functions in the used in the plots
from pylab import *

# It makes the text format looks pretty and well-designed
from textwrap import wrap

# Adding navigation toolbar to the figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

# Import the PyQt4 modules for all the commands that control the GUI.
# Importing as from "Module" import * implies that everything from that module is not part of this module.
# You do not need to put the module name before its commands
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# This is very important because it imports the GUI created earlier using Qt Designer
# To import the GUI from another python file, it is very simple. Just following the following steps:
# 1. Create an empyty file called __init__.py in the same directory as the GUI file
# 2. If the GUI file and __init__.py file are in the same directory as this file, just type "from .GUIfilename import classname"
# 3. If the GUI file and __init__.py file are in the sub file of this file, then type "from subfilename.GUIfilename import classname"
# classname is the name of the class in the GUI file, usually it should be 'Ui_MainWindow'
from Sub_Scripts.GUI import Ui_MainWindow

# To get the screen dimensions (in pixels) using the standard Python library.
from win32api import GetSystemMetrics
screen_res = [GetSystemMetrics (0), GetSystemMetrics (1)]

import subprocess

from Sub_Scripts.Keithley import Keithley
from Sub_Scripts.Agilent import Agilent
from Sub_Scripts.Magnet import Magnet


continue_check = True
# The class that controls all the operations of the GUI. This is the self class that contains all the functions that control the GUI.
class MyForm(QMainWindow):
    
    # The __init__ function is what is everything the user wants to be initialized when the class is called.
    # Here we shall define the trig functions to corresponding variables.
    # Note that the "self" variable means that the function is part of the class and can be called inside and outside the class.(Although __init__ is special.)
    def __init__(self, parent = None):
        
        self.collect_data_thread = Collect_data()

        # Standard GUI code
        QWidget.__init__(self, parent)

        # All the GUI data and widgets in the Ui_MainWindow() class is defined to self.ui
        # Thus to do anything on the GUI, the commands must go through this variable
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.connect(self.ui.pushButton_update_1, SIGNAL('clicked()'), lambda : self.Update("visa1", self.ui.comboBox_visa_1))
        self.connect(self.ui.pushButton_update_2, SIGNAL('clicked()'), lambda : self.Update("visa2", self.ui.comboBox_visa_2))
        self.connect(self.ui.pushButton_update_3, SIGNAL('clicked()'), lambda : self.Update("visa3", self.ui.comboBox_visa_3))
        self.connect(self.ui.pushButton_update_4, SIGNAL('clicked()'), lambda : self.Update("visa4", self.ui.comboBox_visa_4))
        self.connect(self.ui.pushButton_update_5, SIGNAL('clicked()'), lambda : self.Update("visa5", self.ui.comboBox_visa_5))
        self.connect(self.ui.pushButton_select_1, SIGNAL('clicked()'), lambda : self.Select("visa1", self.visa1, self.ui.comboBox_visa_1, self.ui.label_visa_1, [self.ui.pushButton_select_1, self.ui.pushButton_close_1]))
        self.connect(self.ui.pushButton_select_2, SIGNAL('clicked()'), lambda : self.Select("visa2", self.visa2, self.ui.comboBox_visa_2, self.ui.label_visa_2, [self.ui.pushButton_select_2, self.ui.pushButton_close_2]))
        self.connect(self.ui.pushButton_select_3, SIGNAL('clicked()'), lambda : self.Select("visa3", self.visa3, self.ui.comboBox_visa_3, self.ui.label_visa_3, [self.ui.pushButton_select_3, self.ui.pushButton_close_3], baud = 115200))
        self.connect(self.ui.pushButton_select_4, SIGNAL('clicked()'), lambda : self.Select("visa4", self.visa4, self.ui.comboBox_visa_4, self.ui.label_visa_4, [self.ui.pushButton_select_4, self.ui.pushButton_close_4]))
        self.connect(self.ui.pushButton_select_5, SIGNAL('clicked()'), lambda : self.Select("visa5", self.visa5, self.ui.comboBox_visa_5, self.ui.label_visa_5, [self.ui.pushButton_select_5, self.ui.pushButton_close_5]))
        self.connect(self.ui.pushButton_close_1, SIGNAL('clicked()'), lambda : self.Close("visa1", self.visa1, self.ui.label_visa_1, [self.ui.pushButton_select_1, self.ui.pushButton_close_1]))
        self.connect(self.ui.pushButton_close_2, SIGNAL('clicked()'), lambda : self.Close("visa2", self.visa2, self.ui.label_visa_2, [self.ui.pushButton_select_2, self.ui.pushButton_close_2]))
        self.connect(self.ui.pushButton_close_3, SIGNAL('clicked()'), lambda : self.Close("visa3", self.visa3, self.ui.label_visa_3, [self.ui.pushButton_select_3, self.ui.pushButton_close_3]))
        self.connect(self.ui.pushButton_close_4, SIGNAL('clicked()'), lambda : self.Close("visa4", self.visa4, self.ui.label_visa_4, [self.ui.pushButton_select_4, self.ui.pushButton_close_4]))
        self.connect(self.ui.pushButton_close_5, SIGNAL('clicked()'), lambda : self.Close("visa5", self.visa5, self.ui.label_visa_5, [self.ui.pushButton_select_5, self.ui.pushButton_close_5]))
        
        self.connect(self.ui.pushButton_Start, SIGNAL('clicked()'), self.start)
        self.connect(self.ui.pushButton_Stop, SIGNAL('clicked()'), self.collect_data_thread.stop)
        self.connect(self.ui.pushButton_Pause, SIGNAL('clicked()'), self.collect_data_thread.pause)
        self.connect(self.collect_data_thread, SIGNAL("curve_plot"), self.curvePlots_update)
        self.connect(self.collect_data_thread, SIGNAL("print"), self.Print_data)
        
        self.connect(self.ui.textEdit, SIGNAL('textChanged ()'), lambda : self.start_font("C"))
        
        
        self.Update("visa1", self.ui.comboBox_visa_1)
        self.Update("visa2", self.ui.comboBox_visa_2)
        self.Update("visa3", self.ui.comboBox_visa_3)
        self.Update("visa4", self.ui.comboBox_visa_4)
        self.Update("visa5", self.ui.comboBox_visa_5)
        
        self.curve_1 = self.make_curveWidgets(self.ui.curvewidget_1, "black", "black", titles = ["Plot 1", "X (x)", "Y (y)"])
        self.curve_2 = self.make_curveWidgets(self.ui.curvewidget_2, "r", "black", titles = ["Plot 2", "X (x)", "Y (y)"])
        self.curve_3 = self.make_curveWidgets(self.ui.curvewidget_3, "g", "black", titles = ["Plot 3", "X (x)", "Y (y)"])
        self.curve_4 = self.make_curveWidgets(self.ui.curvewidget_4, "o", "black", titles = ["Plot 4", "X (x)", "Y (y)"])
        
        self.visa1 = None
        self.visa2 = None
        self.visa3 = None
        self.visa4 = None
        self.visa5 = None

        self.setWindowTitle("Current Bias Lock-in Time Collection")
        
        font = QFont()
        font.setPointSize(8)
        self.ui.tabWidget_visa.setFont(font)
        self.ui.tabWidget_visa.setTabText(0, "Lock-in")
        self.ui.tabWidget_visa.setTabText(1, "Gate Keithley")
        
        self.input_string = []
        self.input_string.append("00 Run_Number: 01\n\n")
        
        self.input_string.append("01 Time Step: 1.5\n")
        self.input_string.append("02 Averaging: 1\n")
        self.input_string.append("03 Plot Power Spectrum Every: 100\n\n")
        
        self.input_string.append("04 CurrBias Lock-in Sens: 1e-3\n")
        self.input_string.append("05 Current Bias Resistor: 1.009e9\n")
        self.input_string.append("06 Lock-in Output Voltage: 5\n")
        self.input_string.append("07 Additional Lock-in Volt Gain: 1\n\n")
        
        self.input_string.append("08 User: Vannucci\n")
        self.input_string.append("09 Save Name: \n")
        self.input_string.append("10 TimeStamp (y/n): y\n")
        self.input_string.append("11 Comments: ")
        
        
        self.start_font("C")
        
        try:
            file_par = open("parameters.txt", "r")
            input_string_print = file_par.read()
            file_par.close()
            
        except:
            input_string_print = ""
            for st_i in self.input_string:
                input_string_print = input_string_print + st_i
            
        font = QFont()
        font.setPointSize(8)
        self.ui.textEdit.setFont(font)
        self.ui.textEdit.setText(input_string_print)
        
        self.inputted_data = []
        self.array_sweep = []
        
        
        
    
    def start_font(self, status):
        if status == "C":
            font = QFont()
            font.setPointSize(8)
            self.ui.pushButton_Start.setFont(font)
            self.ui.pushButton_Start.setText("Check Inputs")
        elif status == "S":
            font = QFont()
            font.setPointSize(12)
            self.ui.pushButton_Start.setFont(font)
            self.ui.pushButton_Start.setText("Start")
    
    def Update(self, signal, comboBoxVisa):
        rm = visa.ResourceManager()
        try:
            alls = rm.list_resources()
        except:
            alls = "No Visa Available."
        if signal == "visa1":
            self.ui.comboBox_visa_1.clear()
        elif signal == "visa2":
            self.ui.comboBox_visa_2.clear()
        elif signal == "visa3":
            self.ui.comboBox_visa_3.clear()
        elif signal == "visa4":
            self.ui.comboBox_visa_4.clear()
        elif signal == "visa5":
            self.ui.comboBox_visa_5.clear()

        
        for temp in alls:
            if signal == "visa1":
                self.ui.comboBox_visa_1.addItem(temp)
            elif signal == "visa2":
                self.ui.comboBox_visa_2.addItem(temp)
            elif signal == "visa3":
                self.ui.comboBox_visa_3.addItem(temp)
            elif signal == "visa4":
                self.ui.comboBox_visa_4.addItem(temp)
            elif signal == "visa5":
                self.ui.comboBox_visa_5.addItem(temp)
    
    def Select(self, signal, visa_chosen, comboBoxVisa, lineEditVisa, selectClose, baud = None):
        visa_address = str(comboBoxVisa.currentText())
        rm = visa.ResourceManager()
        rm.list_resources()
        if baud == None:
            inst = rm.open_resource(visa_address)
        else:
            inst = rm.open_resource(visa_address, baud_rate = baud)
        visa_check = self.Check(inst)
        if visa_check == True:
            self.ui.label_condition.setText("Visa is selected succefully!")
            visa_name = inst.query("*IDN?")
            name_list = visa_name.split(',')
            first_name = name_list[0]
            if signal == "visa1":
                lineEditVisa.setText(visa_name)
                selectClose[0].setEnabled(False)
                selectClose[1].setEnabled(True)
                #self.Enable(signal)
                self.visa1 = inst
            elif signal == "visa2":
                lineEditVisa.setText(visa_name)
                selectClose[0].setEnabled(False)
                selectClose[1].setEnabled(True)
                #self.Enable(signal)
                self.visa2 = inst
            elif signal == "visa3":
                lineEditVisa.setText(visa_name)
                selectClose[0].setEnabled(False)
                selectClose[1].setEnabled(True)
                #self.Enable(signal)
                self.visa3 = inst
            elif signal == "visa4":
                lineEditVisa.setText(visa_name)
                selectClose[0].setEnabled(False)
                selectClose[1].setEnabled(True)
                #self.Enable(signal)
                self.visa4 = inst
            elif signal == "visa5":
                lineEditVisa.setText(visa_name)
                selectClose[0].setEnabled(False)
                selectClose[1].setEnabled(True)
                #self.Enable(signal)
                self.visa5 = inst
        elif visa_check == False:
            self.ui.label_condition.setText("Invalid visa address.")
            lineEditVisa.setText("None.")
            visa_chosen = False
    
    def Close(self, signal, visa_chosen, lineEditVisa, selectClose):
        self.ui.label_condition.setText('Visa address is closed')
        lineEditVisa.setText('')
        selectClose[0].setEnabled(True)
        selectClose[1].setEnabled(False)
        if signal == "visa1":
            visa_chosen.close()
            self.visa1 = None
            #self.Disable(signal)
        elif signal == "visa2":
            visa_chosen.close()
            self.visa2 = None
            #self.Disable(signal)
        elif signal == "visa3":
            visa_chosen.close()
            self.visa3 = None
            #self.Disable(signal)
        elif signal == "visa4":
            visa_chosen.close()
            self.visa4 = None
            #self.Disable(signal)
        elif signal == "visa5":
            visa_chosen.close()
            self.visa5 = None
            #self.Disable(signal)
            
    def Check(self, inst):
        try:
            inst.ask("*IDN?")
            valid = True
        except:
            valid = False
        return valid
    
    def make_curveWidgets(self, curvewidget, color, markerColor, titles):
        curve_temp = make.curve([], [], color = color, marker = "o", markerfacecolor = markerColor, markersize = 5)
        curvewidget.plot.add_item(curve_temp)
        curvewidget.plot.set_antialiasing(True)
        curvewidget.plot.set_titles(titles[0], titles[1], titles[2])
        return curve_temp
    
    def start(self):
        instruments = [self.visa1, self.visa2, self.visa3, self.visa4, self.visa5]
        curves = [self.curve_1, self.curve_2, self.curve_3, self.curve_4]
        curveWidgets =[self.ui.curvewidget_1, self.ui.curvewidget_2, self.ui.curvewidget_3, self.ui.curvewidget_4]
        go_on = True
        
        inputted_string = str(self.ui.textEdit.toPlainText())
        input_data = inputted_string.split("Comments:")
        comments = input_data[1]
        
        input_data = input_data[0].split("\n")
        
        inputted_data = []
        
        for i in range(0, len(input_data)):
            for j in range(0, len(self.input_string)):
                if len(input_data[i].split(self.input_string[j].split(":")[0])) > 1:
                    inputted_data.append(input_data[i].split(self.input_string[j].split(":")[0])[1].replace(":", "").replace(" ", ""))
                    print inputted_data
        
        run_program = True
        for i in range(0, len(inputted_data)):
            try:
                if self.inputted_data[i] != inputted_data[i]:
                    run_program = False
                    self.start_font("C")
            except:
                run_program = False
                self.start_font("C")
        
        if not run_program:
            self.inputted_data = inputted_data
            self.start_font("S")
            
        elif run_program:
            if str(self.ui.pushButton_Start.text()) == "Start":
                self.start_font("C")
                self.collect_data_thread.input(self.ui, instruments, curves, curveWidgets, go_on, inputted_data, comments, inputted_string, self.input_string)
            else:
                self.start_font("S")

    def curvePlots_update(self, curveInfo):
        curveWidget = curveInfo[0]
        curve = curveInfo[1]
        curveWidget.plot.do_autoscale()
        curve.plot().replot()
    
    def Print_data(self, display_text):
        
        font = QFont()
        font.setPointSize(8)
        self.ui.textEditDisplay.setFont(font)
        self.ui.textEditDisplay.setText(display_text)
        
        """self.ui.label_step.setText(step)
        self.ui.label_time.setText(time)
        self.ui.label_V1.setText(V1)
        self.ui.label_V2.setText(V2)
        self.ui.label_V3.setText(V3)
        self.ui.label_V4.setText(V4)
        self.ui.label_V5.setText(V5)
        self.ui.label_V6.setText(V6)"""
        
    
    def Switch_scale(self, num):
        temp = abs(num)
        if temp >= 1E9:
            scale = [1E-9, "G"]
        elif temp >= 1E6 and temp < 1E9:
            scale = [1E-6, "M"]
        elif temp >= 1E3 and temp < 1E6:
            scale = [1E-3, "k"]
        elif temp >= 1 and temp < 1000:
            scale = [1, ""]
        elif temp >= 1E-3 and temp < 1:
            scale = [1E3, "m"]
        elif temp >= 1E-6 and temp < 1E-3:
            scale = [1E6, "u"]
        elif temp >= 1E-9 and temp < 1E-6:
            scale = [1E9, "n"]
        elif temp < 1E-9:
            scale = [1E12, "p"]
            
        return scale
    
    def closeEvent(self, event):
        quit_msg = "Do you want to quit the program?"
        reply = QMessageBox.question(self, "Message", quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
class Collect_data(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False

    def input(self, ui, instruments, curves, curveWidgets, go_on, inputted_data, comments, inputted_string, input_string):
        self.ui = ui
        self.lockin_visa = instruments[0]
        self.keithley_visa = instruments[1]
        self.curves = curves
        self.curveWidgets = curveWidgets
        self.go_on = go_on
        self.inputted_string = inputted_string
        self.input_string = input_string
        
        self.run_num = str(inputted_data[0])
        self.time_step = float(inputted_data[1])
        self.averaging = int(inputted_data[2])
        self.plot_PSD = int(inputted_data[3])
        self.lockin_sens = float(inputted_data[4])
        self.currBias_resis = float(inputted_data[5])
        self.lockin_voltage = float(inputted_data[6])
        self.currBias_curr = self.lockin_voltage/self.currBias_resis
        self.volt_gain = float(inputted_data[7])
        self.user = str(inputted_data[8])
        self.file_name = str(inputted_data[9])
        self.timeStamp = str(inputted_data[10]).upper()
        self.comments = comments
        
        self.Gate_Volt = []
        self.Gate_Curr = []
        self.Field = []
        self.Device_Volt = []
        self.Device_Curr = []
        self.Device_Cond = []
        self.Device_Resis = []
        
        #self.run()
        self.start()
    
    def stop(self):
        self.stop_collecting = True
        self.pause_collecting = False
        self.ui.label_condition.setText('Stopped.')
        self.ui.pushButton_Start.setEnabled(True)
        self.ui.pushButton_Pause.setEnabled(False)
        self.ui.pushButton_Stop.setEnabled(False)
    
    def pause(self):
        if self.pause_collecting:
            self.read_textEditIn()
            self.ui.label_condition.setText('Running...')
            self.ui.pushButton_Pause.setText("Pause")
            self.pause_collecting = False
        else:
            self.ui.label_condition.setText('Paused. Click continue to run.')
            self.ui.pushButton_Pause.setText("Continue")
            self.pause_collecting = True
            
    def run(self):
        import time
        
        if self.timeStamp == "Y":
            file_name = self.run_num + "_" + self.file_name + "_" + str(time.ctime().replace(":", "-").replace(" ", "_"))
        else:
            file_name = self.run_num + "_" + self.file_name
            
        self.write_file = open(file_name + ".txt", 'w')
        self.write_file.write("User: " + self.user + "\n\n")
        self.write_file.write(self.inputted_string + "\n\n")
        self.write_file.write("Collected Data\n")
        self.write_file.write("Time, Gate Voltage, Gate Current, Device Voltage, Device Current, Device Conductane, Device Resistance\n")
        self.write_file.write("s, V, A, V, A, S, Ohms\n")
        


        self.t_plot = []
        date_value = []
        date_and_time = []
        self.s_value = []
        temp = 0
        start_time = time.time()
        
        self.pause_collecting = False
        self.stop_collecting = False
        self.ui.pushButton_Start.setEnabled(False)
        self.ui.pushButton_Pause.setEnabled(True)
        self.ui.pushButton_Stop.setEnabled(True)
        
        self.time_collect = 0
        self.i_psd = 0
        
        while True:
            time_step_run = (time.time() - self.time_collect)
            if time_step_run > self.time_step:
                
                self.time_collect = time.time()
                
                if self.go_on:
                    if self.stop_collecting:
                        self.ui.label_condition.setText('Reading stoped.')
                        break
                    
                    if self.pause_collecting:
                        self.ui.label_condition.setText('Reading paused.')                  
                        
                    else:
                        
                        self.ui.label_condition.setText('Reading...')
                        
                        Keithley().read_data_write(self.keithley_visa)
                        gate_data = Keithley().read_data_read(self.keithley_visa)
                        
                        DeviceVolt = 0
                        for i in range(0, self.averaging):
                            
                            Agilent().read_data_write(self.lockin_visa)
                            DeviceVolt = DeviceVolt + float(Agilent().read_data_read(self.lockin_visa))
                        
                        DeviceVolt = DeviceVolt*self.lockin_sens/(10.0*self.volt_gain*self.averaging)
                        
                        
                        end_time = time.time()
                        self.during = end_time - start_time
                        self.t_plot.append(self.during/3600.0)
                        
                        self.write_file.write(str(self.during) + "," + str(float(gate_data[0])) + "," + str(float(gate_data[1])) + "," + str(DeviceVolt)+ "," + str(self.currBias_curr) + "," + str(self.currBias_curr/DeviceVolt) + "," + str(DeviceVolt/self.currBias_curr)+ "\n")
                        
                        self.Gate_Volt.append(float(gate_data[0]))
                        self.Gate_Curr.append(float(gate_data[1])*1e12) #pA
                        self.Device_Curr.append(self.currBias_curr*1e9) #nA
                        self.Device_Volt.append(DeviceVolt*1e6) #uV
                        self.Device_Resis.append(DeviceVolt/self.currBias_curr*1e-3) #kOhms
                        self.Device_Cond.append(self.currBias_curr/DeviceVolt*1e6) #uS
                        
                        self.s_value.append(temp)
                        
                        self.setup_plot(self.curveWidgets[0], self.curves[0], [self.t_plot, self.Device_Resis], ["Device Resistance", "Time (hr)", "Resistance (kOhms)"])
                        self.setup_plot(self.curveWidgets[1], self.curves[1], [self.t_plot, self.Device_Cond], ["Device Conductance", "Time (hr)", "Conductance (uS)"])
                        #self.setup_plot(self.curveWidgets[2], self.curves[2], [self.t_plot, self.Gate_Volt], ["Gate Voltage", "Time (hr)", "Voltage (V)"])
                        
                        plotted_psd = str(self.i_psd - self.plot_PSD)
                        if self.i_psd == self.plot_PSD:
                            self.i_psd = 0
                            f, Pxx_den = signal.periodogram(self.Device_Cond, fs = self.time_step, scaling = "density")
                            f = f[1:]
                            Pxx_den = Pxx_den[1:]
                            f = numpy.log10(f)
                            Pxx_den = numpy.log10(Pxx_den)
                            plotted_psd = "True"
                            self.setup_plot(self.curveWidgets[3], self.curves[3], [f, Pxx_den], ["Conductance Power Spectral Density", "Frequency (log(Hz))", "Amplitude (log(S^2/Hz)"])
                        
                        
                        display_text = ""
                        
                        display_text = display_text + "Time: " + str(round(self.during, 3)) + " s\n"
                        display_text = display_text + "Time Step: " + str(round(time_step_run, 3)) + " s\n\n"
                        display_text = display_text + "Gate Voltage: " + str(round(float(gate_data[0]), 3)) + " V\n"
                        display_text = display_text + "Gate Current: " + str(round(float(gate_data[1])*1e12, 3)) + " pA\n\n"
                        display_text = display_text + "Device Voltage: " + str(round(DeviceVolt*1e6, 3)) + " uV\n"
                        display_text = display_text + "Device Current: " + str(round(self.currBias_curr*1e9, 3)) + " nA\n"
                        display_text = display_text + "Device Resistance: " + str(round(DeviceVolt/self.currBias_curr*1e-3, 3)) + " kOhms\n"
                        display_text = display_text + "Device Conductance: " + str(round(self.currBias_curr/DeviceVolt*1e6, 3)) + " uS\n\n"
                        display_text = display_text + "Plotted PSD: " + plotted_psd + "\n"
                        
                        
                        self.emit(SIGNAL("print"), display_text) #, self.during, float(self.data[0]), float(self.data[1]))
                        
                        now = datetime.datetime.now()
                        date = '%s-%s-%s' % (now.year, now.month, now.day)
                        current_time = '%s:%s:%s' % (now.hour, now.minute, now.second)
                        self.date_and_time = date + ' ' + current_time
                        date_value.append(self.date_and_time)
                        
                        temp += 1
                        self.i_psd += 1
        

        self.ui.pushButton_Start.setEnabled(True)
        self.ui.pushButton_Pause.setEnabled(False)
        self.ui.pushButton_Stop.setEnabled(False)
        self.write_file.close()
        
        file_par = open("parameters.txt", "w").write(str(self.ui.textEdit.toPlainText()))
        file_par.close()
        
    def setup_plot(self, curveWidget, curve, data, titles):
        curveWidget.plot.set_titles(titles[0], titles[1], titles[2])
        curve.set_data(data[0], data[1])
        self.emit(SIGNAL("curve_plot"), [curveWidget, curve])
    
    
    def read_textEditIn(self):
        inputted_string = str(self.ui.textEdit.toPlainText())
        input_data = inputted_string.split("Comments:")
        comments = input_data[1]
        
        input_data = input_data[0].split("\n")
        
        inputted_data = []
        
        for i in range(0, len(input_data)):
            for j in range(0, len(self.input_string)):
                if len(input_data[i].split(self.input_string[j].split(":")[0])) > 1:
                    inputted_data.append(input_data[i].split(self.input_string[j].split(":")[0])[1].replace(":", "").replace(" ", ""))
        
        if self.lockin_sens != float(inputted_data[6]):
            self.lockin_sens = float(inputted_data[6])
            self.write_file.write("\nNew Lock-in Sens: " + str(self.lockin_sens) + "\n\n")
        if self.currBias_resis != float(inputted_data[7]):
            self.currBias_resis = float(inputted_data[7])
            self.currBias_curr = self.lockin_voltage/self.currBias_resis
            self.write_file.write("\nNew Current Bias Resistor: " + str(self.currBias_resis) + "\n\n")
        if self.lockin_voltage != float(inputted_data[8]):
            self.lockin_voltage = float(inputted_data[8])
            self.currBias_curr = self.lockin_voltage/self.currBias_resis
            self.write_file.write("\nNew Lock-in Voltage Output: " + str(self.lockin_voltage) + "\n\n")
        if self.volt_gain != float(inputted_data[9]):
            self.volt_gain = float(inputted_data[9])
            self.write_file.write("\nNew Lock-in Voltage Gain: " + str(self.volt_gain) + "\n\n")
        
    
    
    def Switch_scale(self, num):
        temp = abs(num)
        if temp >= 1E9:
            scale = [1E-9, "G"]
        elif temp >= 1E6 and temp < 1E9:
            scale = [1E-6, "M"]
        elif temp >= 1E3 and temp < 1E6:
            scale = [1E-3, "k"]
        elif temp >= 1 and temp < 1000:
            scale = [1, ""]
        elif temp >= 1E-3 and temp < 1:
            scale = [1E3, "m"]
        elif temp >= 1E-6 and temp < 1E-3:
            scale = [1E6, "u"]
        elif temp >= 1E-9 and temp < 1E-6:
            scale = [1E9, "n"]
        elif temp < 1E-9:
            scale = [1E12, "p"]
            
        return scale
    
    def __del__(self):
        self.exiting = True
        self.wait()
# The if statement is to check whether this module is the self module and in case that it is imported by another module
# If it is the self module then it starts the GUI under if condition
# This in case it is being imported, then it will not immediately start the GUI upon being imported
if __name__ == "__main__":
    # Opens the GUI
    app = QApplication(sys.argv)
    myapp = MyForm()

    # Shows the GUI
    myapp.show()

    # Exits the GUI when the x button is clicked
    sys.exit(app.exec_())
        
        

        
