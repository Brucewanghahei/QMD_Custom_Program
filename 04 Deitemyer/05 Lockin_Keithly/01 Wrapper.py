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
#from Sub_Scripts.Agilent import Agilent
#from Sub_Scripts.RfPower import RfPower
from Sub_Scripts.DigitalLockin import DigitalLockin

import time

from Sub_Scripts.D_save import Dynamic_Save_Thread

continue_check = True
# The class that controls all the operations of the GUI. This is the self class that contains all the functions that control the GUI.
class MyForm(QMainWindow):
    
    # The __init__ function is what is everything the user wants to be initialized when the class is called.
    # Here we shall define the trig functions to corresponding variables.
    # Note that the "self" variable means that the function is part of the class and can be called inside and outside the class.(Although __init__ is special.)
    def __init__(self, parent = None):
        
        self.collect_data_thread = Collect_data()
        self.dsave_thread = Dynamic_Save_Thread()
        
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
        self.connect(self.ui.pushButton_select_1, SIGNAL('clicked()'), lambda : self.Select("visa1", self.visa1, self.ui.comboBox_visa_1, self.ui.label_visa_1, [self.ui.pushButton_select_1, self.ui.pushButton_close_1]))
        self.connect(self.ui.pushButton_select_2, SIGNAL('clicked()'), lambda : self.Select("visa2", self.visa2, self.ui.comboBox_visa_2, self.ui.label_visa_2, [self.ui.pushButton_select_2, self.ui.pushButton_close_2]))
        self.connect(self.ui.pushButton_select_3, SIGNAL('clicked()'), lambda : self.Select("visa3", self.visa3, self.ui.comboBox_visa_3, self.ui.label_visa_3, [self.ui.pushButton_select_3, self.ui.pushButton_close_3]))
        self.connect(self.ui.pushButton_select_4, SIGNAL('clicked()'), lambda : self.Select("visa4", self.visa4, self.ui.comboBox_visa_4, self.ui.label_visa_4, [self.ui.pushButton_select_4, self.ui.pushButton_close_4]))
        self.connect(self.ui.pushButton_close_1, SIGNAL('clicked()'), lambda : self.Close("visa1", self.visa1, self.ui.label_visa_1, [self.ui.pushButton_select_1, self.ui.pushButton_close_1]))
        self.connect(self.ui.pushButton_close_2, SIGNAL('clicked()'), lambda : self.Close("visa2", self.visa2, self.ui.label_visa_2, [self.ui.pushButton_select_2, self.ui.pushButton_close_2]))
        self.connect(self.ui.pushButton_close_3, SIGNAL('clicked()'), lambda : self.Close("visa3", self.visa3, self.ui.label_visa_3, [self.ui.pushButton_select_3, self.ui.pushButton_close_3]))
        self.connect(self.ui.pushButton_close_4, SIGNAL('clicked()'), lambda : self.Close("visa4", self.visa4, self.ui.label_visa_4, [self.ui.pushButton_select_4, self.ui.pushButton_close_4]))

        self.connect(self.ui.pushButton_Start, SIGNAL('clicked()'), self.start)
        self.connect(self.ui.pushButton_Stop, SIGNAL('clicked()'), self.collect_data_thread.stop)
        self.connect(self.ui.pushButton_Pause, SIGNAL('clicked()'), self.collect_data_thread.pause)
        self.connect(self.collect_data_thread, SIGNAL("curve_plot"), self.curvePlots_update)
        self.connect(self.collect_data_thread, SIGNAL("freq_update"), self.setup_plot)
        self.connect(self.collect_data_thread, SIGNAL("power_update"), self.setup_plot)
        self.connect(self.collect_data_thread, SIGNAL("print_value"), self.Print_data)
        self.connect(self.ui.checkBox_dsave, SIGNAL("clicked()"), self.Pre_dsave)
        self.connect(self.ui.textEdit, SIGNAL('textChanged ()'), lambda : self.start_font("C"))
        self.connect(self.ui.pushButton_dsave_browse, SIGNAL('clicked()'), self.Dsave_browse)
        
        self.Update("visa1", self.ui.comboBox_visa_1)
        self.Update("visa2", self.ui.comboBox_visa_2)
        self.Update("visa3", self.ui.comboBox_visa_3)
        self.Update("visa4", self.ui.comboBox_visa_4)

        
        self.curve_3 = self.make_curveWidgets(self.ui.curvewidget_3, "b", "blue", titles = ["RF Power", "Step", "Power (dBm)"])
        self.curve_3_update = self.make_curveWidgets(self.ui.curvewidget_3, "red", "red", titles = ["RF Power", "Step", "Power (dBm)"])
        self.curve_2_b = self.make_curveWidgets(self.ui.curvewidget_2, "black", "black", titles = ["Keithley", "Step", "Voltage (V)"])
        self.curve_2_r = self.make_curveWidgets(self.ui.curvewidget_2, "red", "red", titles = ["Keithley", "Step", "Voltage (V)"])
        self.curve_1 = self.make_curveWidgets(self.ui.curvewidget_1, "b", "blue", titles = ["Keithley", "Step", "Voltage (V)"])
        self.curve_1_update = self.make_curveWidgets(self.ui.curvewidget_1, "red", "red", titles = ["Keithley", "Step", "Voltage (V)"])
        
        self.Curve1 = self.make_curveWidgets(self.ui.curvewidget_13, "r", "black", titles = ["Plot 1", "X (x)", "Y (y)"])
        self.Curve2 = self.make_curveWidgets(self.ui.curvewidget_14, "g", "black", titles = ["Plot 2", "X (x)", "Y (y)"])
        self.Curve3 = self.make_curveWidgets(self.ui.curvewidget_15, "r", "black", titles = ["Plot 3", "X (x)", "Y (y)"])
        self.Curve4 = self.make_curveWidgets(self.ui.curvewidget_16, "g", "black", titles = ["Plot 4", "X (x)", "Y (y)"])
        
        self.visa1 = None
        self.visa2 = None
        self.visa3 = None
        self.visa4 = None

        self.setWindowTitle("Sweep with Lock-in without Magnetic")
        
        self.input_string = []
        self.input_string.append("00 Run_Number: 01\n\n")
        
        self.input_string.append("01 Start Gate Voltage (V): 35\n")
        self.input_string.append("02 Step Gate Voltage (V): 0.1\n")
        self.input_string.append("03 03 End Gate Voltage (V): 0\n")
        self.input_string.append("04 Double Linear (y/n): n\n")
        self.input_string.append("05 Turn off Keithley (y/n): n\n")
        self.input_string.append("06 CurrBias Lock-in Sens: 20e-6\n")
        self.input_string.append("07 Reading wait time(s): .25\n\n")
        
        self.input_string.append("08 Current Bias Resistor: 1.009e9\n")
        self.input_string.append("09 Lock-in Output Voltage: 10\n")
        self.input_string.append("10 Additional Lock-in Volt Gain: 1\n\n")
        
        self.input_string.append("11 User: Vannucci\n")
        self.input_string.append("12 File Name: S-SiA0036-V_B1_leads\n")
        self.input_string.append("13 TimeStamp (y/n): y\n")
        self.input_string.append("14 Comments:\n\n")
        self.start_font("C")        
        
        self.out0_1 = "None"
        self.out0_2 = "None"
        self.out0_3 = "None"
        self.out0_4 = "None"
        self.out1_0 = "None"
        self.out1_1 = "None"
        self.out1_2 = "None"
        self.out1_3 = "None"
        self.out2_0 = "None"
        self.out2_1 = "None"
        self.out2_2 = "None"
        self.out2_3 = "None"
        self.out3_0 = "None"
        self.out3_1 = "None"
        self.out3_2 = "None"
        self.out3_3 = "None"
        
        self.scale1_1 = [1, ""]
        self.scale1_2 = [1, ""]
        self.scale1_3 = [1, ""]
        self.scale2_1 = [1, ""]
        self.scale2_2 = [1, ""]
        self.scale2_3 = [1, ""]
        self.scale3_1 = [1, ""]
        self.scale3_2 = [1, ""]
        self.scale3_3 = [1, ""]
        
        self.Coil_Constant = 1E-3/9.1E-3
        
        try:
            file_par = open("parameters.txt", "r")
            input_string_print = file_par.read()
            
        except:
            input_string_print = ""
            for st_i in self.input_string:
                input_string_print = input_string_print + st_i
        
        font = QFont()
        font.setPointSize(10)
        self.ui.textEdit.setFont(font)
        self.ui.textEdit.setText(input_string_print)
        
        self.inputted_data = []
        self.array_sweep = []
        
        rm = visa.ResourceManager()
        self.Visa_states = []
        try:
            alls = rm.list_resources()
            for i in range(0, len(alls)):
                self.Visa_states.append([alls[i], True])
        except:
            alls = "No Visa Available."
        
    def start_font(self, status):
        if status == "C":
            font = QFont()
            font.setPointSize(8)
            self.ui.pushButton_Start.setFont(font)
            self.ui.pushButton_Start.setText("Check Array")
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
        
        for temp in alls:
            if signal == "visa1":
                self.ui.comboBox_visa_1.addItem(temp)
            elif signal == "visa2":
                self.ui.comboBox_visa_2.addItem(temp)
            elif signal == "visa3":
                self.ui.comboBox_visa_3.addItem(temp)
            elif signal == "visa4":
                self.ui.comboBox_visa_4.addItem(temp)
        
        # if signal == "visa1":
        #     self.ui.comboBox_visa_1.addItem(alls[3])
        # elif signal == "visa2":
        #     self.ui.comboBox_visa_2.addItem(alls[0])
        # elif signal == "visa3":
        #     self.ui.comboBox_visa_3.addItem(alls[4])
        # elif signal == "visa4":
        #     self.ui.comboBox_visa_4.addItem(alls[1])
    
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
            
            visa_name = inst.query("*IDN?")
            name_list = visa_name.split(',')
            first_name = name_list[0]
            if signal == "visa1":
                if self.Ready(inst):
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa1 = inst
                    self.Mark(inst, False)
                    self.ui.label_condition.setText("Visa is selected succefully!")
                else:
                    self.ui.label_condition.setText("Pick another Lock_In address")
            elif signal == "visa2":
                if self.Ready(inst):
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2 = inst
                    self.Mark(inst, False)
                    self.ui.label_condition.setText("Visa is selected succefully!")
                else:
                    self.ui.label_condition.setText("Pick another Keithley address")
            
        elif visa_check == False:
            self.ui.label_condition.setText("Invalid visa address.")
            lineEditVisa.setText("None.")
            visa_chosen = False
    
    def Ready(self, inst):
        temp = str(inst).split(' ')
        address = temp[len(temp) - 1]
        for i in range(0, len(self.Visa_states)):
            if self.Visa_states[i][0] == address:
                return self.Visa_states[i][1]
        return False
    
    def Mark(self, inst, bol):
        temp = str(inst).split(' ')
        address = temp[len(temp) - 1]
        for i in range(0, len(self.Visa_states)):
            if self.Visa_states[i][0] == address:
                self.Visa_states[i][1] = bol
    
    def Close(self, signal, visa_chosen, lineEditVisa, selectClose):
        self.ui.label_condition.setText('Visa address is closed')
        lineEditVisa.setText('')
        selectClose[0].setEnabled(True)
        selectClose[1].setEnabled(False)
        self.Mark(visa_chosen, True)
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
    
    def array_builder(self, start, step, stop, double_linear):
        if start < stop:
            array_1 = numpy.arange(start, stop + step, abs(step))
        elif start > stop:
            array_1 = numpy.arange(stop, start - step, abs(step))[::-1]
        else:
            array_1 = numpy.array([start])
        
        if double_linear == "y":
            array = array_1[::-1]
            array_2 = numpy.delete(array, 0)
            
            array_sweep = numpy.append(array_1, array_2)
        else:
             array_sweep = array_1
        return array_sweep
            
    def start(self):
        self.Device1_state = False
        
        self.instruments = []
        curves = [self.Curve1, self.Curve2, self.Curve3, self.Curve4, self.curve_3, self.curve_3_update, self.curve_1, self.curve_1_update]
        curveWidgets =[self.ui.curvewidget_13, self.ui.curvewidget_14, self.ui.curvewidget_15, self.ui.curvewidget_16, self.ui.curvewidget_1]
        array_1 = []
        go_on = True
        
        input_data = []
        temp = str(self.ui.textEdit.toPlainText()).split("\n")
        for i in range(0, len(temp)):
            if temp[i] != '':
                input_data.append(temp[i])
        inputted_data = []
        inputted_data.append([input_data[0].split(":")[1].replace(" ", "")])
        temp = []
        for i in range(1, 8):
            temp.append(input_data[i].split(":")[1].replace(" ", ""))
        inputted_data.append(temp)
        temp = []
        for i in range(8, 11):
            temp.append(input_data[i].split(":")[1].replace(" ", ""))
        inputted_data.append(temp)
        temp = []
        for i in range(11, 15):
            temp.append(input_data[i].split(":")[1].replace(" ", ""))
        inputted_data.append(temp)
        self.Device1_state = True
        device_state = [self.Device1_state]
        
        #Make Array
        count = 0
        if self.Device1_state:
            count += 1
            temp = []
            array_1 = self.array_builder(float(inputted_data[1][0]), float(inputted_data[1][1]), float(inputted_data[1][2]), inputted_data[1][3])
            
        
        if str(self.ui.pushButton_Start.text()) == "Start":
            if self.Check_ready(count):
                if self.ui.checkBox_dsave.isChecked():
                    self.Dsave_directory()
                    if self.dsave_dir_ok:
                        self.Dsave_filename()
                        if self.dsave_filename_ok:    
                            self.Dsave_username()
                            if self.dsave_username_ok:
                                self.Dsave_filetype()
                                dsave = [self.dsave_directory, self.dsave_filename, self.dsave_username, self.dsave_thread, self.dsave_filetype, self.dsave_divide, self.date]
                                self.start_font("C")
                                self.ui.tabWidget.setCurrentIndex(2)
                                self.ui.pushButton_Start.setEnabled(False)
                                self.ui.pushButton_Pause.setEnabled(True)
                                self.ui.pushButton_Stop.setEnabled(True)
                                
                                file_par = open("parameters.txt", "w").write(str(self.ui.textEdit.toPlainText()))
                                self.collect_data_thread.input(self.ui, self.instruments, curves, curveWidgets, go_on, inputted_data, array_1, device_state, count, dsave, input_data)
                            else:
                                self.ui.label_condition.setText('Enter user name for dynamic saving.')
                        else:
                            self.ui.label_condition.setText('Enter file name for dynamic saving.')
                    else:
                        self.ui.label_condition.setText('Choose valid directory for dynamic saving.')
                else:
                    self.ui.label_condition.setText('Choose dynamic saving.')
            else:
                self.ui.label_condition.setText('Make sure enough devices are connected.')
        else:
            # if self.Device1_state:
            #     self.setup_plot_2(self.curve_2_b, self.curve_2_r, array_1)
            self.setup_plot(self.curve_1, array_1)
            self.ui.tabWidget.setCurrentIndex(0)
            self.start_font("S")
    
    def Check_ready(self, count):
        if count == 1:
            self.instruments = [self.visa1, self.visa2]
            return True
        return False
    
    def setup_plot(self, curve, data):
        x = []
        for i in range(0, len(data)):
            x.append(i)
        curve.set_data(x, data)
        self.ui.curvewidget_1.plot.do_autoscale()
        self.ui.curvewidget_2.plot.do_autoscale()
        self.ui.curvewidget_3.plot.do_autoscale()
        curve.plot().replot()
    
    def setup_plot_2(self, curve_b, curve_r, data):
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        num = 0
        for i in range(0, len(data)):
            x1.append(num)
            y1.append(data[i])
            num += 1
        num -= 1
        curve_b.set_data(x1, y1)
        #curve_r.set_data(x2, y2)
        curve_b.plot().replot()
        #curve_r.plot().replot()
            
    def curvePlots_update(self, curveInfo):
        curveWidget = curveInfo[0]
        curve = curveInfo[1]
        curveWidget.plot.do_autoscale()
        curve.plot().replot()
    
    def Print_data(self, device, text):
        font = QFont()
        font.setPointSize(10)
        self.ui.textEditDisplay.setFont(font)
        self.out0_1 = str(format(text[0], '.3f'))
        self.out0_2 = str(format(text[1], '.3f'))
        lockin_params = text[7]
        # print lockin_params
        # print lockin_params[1][0]
        # print lockin_params[0][0]
        # print lockin_params[1][1]
        # print lockin_params[0][1]
        display_text = ""
        display_text = display_text + "Time: " + self.out0_1 + " s\n"
        display_text = display_text + "Time Step: " + self.out0_2 + " s\n"
        out1_1 = float(text[2])
        self.scale1_1 = self.Switch_scale(out1_1)
        self.out1_1 = str(format(out1_1 * self.scale1_1[0], '.3f'))
        out1_2 = float(text[3])
        self.scale1_2 = self.Switch_scale(out1_2)
        self.out1_2 = str(format(out1_2 * self.scale1_2[0], '.3f'))
        out1_3 = float(text[4])
        self.scale1_3 = self.Switch_scale(out1_3)
        self.out1_3 = str(format(out1_3 * self.scale1_3[0], '.3f'))
        out1_4 = float(text[5])
        self.scale1_4 = self.Switch_scale(out1_4)
        self.out1_4 = str(format(out1_4 * self.scale1_4[0], '.3f'))
        self.out1_5 = float(text[6])
        # self.scale1_5 = self.Switch_scale(out1_5)
        # self.out1_5 = str(format(out1_5 * self.scale1_5[0], '.3f'))
            
        if self.Device1_state:
            display_text = display_text + "Output Voltage: " + str(self.out1_1) + " " + str(self.scale1_1[1]) + "Volts\n"
            display_text = display_text + "Output Current: " + str(self.out1_2) + " " + str(self.scale1_2[1])+ "Amps\n"
            display_text = display_text + "X: " + str(self.out1_3) + " "  + str(self.scale1_3[1])+ "Volts\n"
            display_text = display_text + "Y: " + str(self.out1_4) + " "  + str(self.scale1_4[1])+ "Volts\n"
            display_text = display_text + "Phase: " + str(self.out1_5) + " " + "Radians\n"
            display_text = display_text + lockin_params[1][0] + ': ' + lockin_params[0][0] +'\n'
            display_text = display_text + lockin_params[1][1] + ': ' + lockin_params[0][1] +'\n'
            display_text = display_text + lockin_params[1][2] + ': ' + lockin_params[0][2] +'\n'
            display_text = display_text + lockin_params[1][3] + ': ' + lockin_params[0][3] +'\n'
            display_text = display_text + lockin_params[1][4] + ': ' + lockin_params[0][4] +'\n'
            display_text = display_text + lockin_params[1][5] + ': ' + lockin_params[0][5] +'\n'
            display_text = display_text + lockin_params[1][6] + ': ' + lockin_params[0][6] +'\n'
            display_text = display_text + lockin_params[1][7] + ': ' + lockin_params[0][7] +'\n'
            display_text = display_text + lockin_params[1][8] + ': ' + lockin_params[0][8] +'\n'
            display_text = display_text + lockin_params[1][9] + ': ' + lockin_params[0][9] +'\n'
            display_text = display_text + text[8]+ '\n'
            
            
        self.ui.textEditDisplay.setText(display_text)       
    
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
    
    def Pre_dsave(self):
        if self.ui.checkBox_dsave.isChecked():
            self.ui.label_dsave_directory.setEnabled(True)
            self.ui.lineEdit_dsave_directory.setEnabled(True)
            self.ui.pushButton_dsave_browse.setEnabled(True)
            self.ui.groupBox_dsave_filename.setEnabled(True)
            self.ui.radioButton_dsave_timename.setEnabled(True)
            self.ui.radioButton_dsave_custname.setEnabled(True)
            self.ui.lineEdit_dsave_custname.setEnabled(True)
            self.ui.groupBox_dsave_filetype.setEnabled(True)
            self.ui.radioButton_csv.setEnabled(True)
            self.ui.radioButton_txt.setEnabled(True)
            self.ui.label_dsave_username.setEnabled(True)
            self.ui.lineEdit_dsave_username.setEnabled(True)
            self.ui.label_dsave_comment.setEnabled(True)
            self.ui.textEdit_dsave_comment.setEnabled(True)
            self.ui.label_condition.setText("Dynamic saving opened.")
        else:
            self.ui.label_dsave_directory.setEnabled(False)
            self.ui.lineEdit_dsave_directory.setEnabled(False)
            self.ui.pushButton_dsave_browse.setEnabled(False)
            self.ui.groupBox_dsave_filename.setEnabled(False)
            self.ui.radioButton_dsave_timename.setEnabled(False)
            self.ui.radioButton_dsave_custname.setEnabled(False)
            self.ui.lineEdit_dsave_custname.setEnabled(False)
            self.ui.groupBox_dsave_filetype.setEnabled(False)
            self.ui.radioButton_csv.setEnabled(False)
            self.ui.radioButton_txt.setEnabled(False)
            self.ui.label_dsave_username.setEnabled(False)
            self.ui.lineEdit_dsave_username.setEnabled(False)
            self.ui.label_dsave_comment.setEnabled(False)
            self.ui.textEdit_dsave_comment.setEnabled(False)
            self.ui.label_condition.setText("Dynamic saving closed.")

    def Dsave_browse(self):
        self.dsave_directory = ''
        prev_dir = os.getcwd()
        fileDir = QFileDialog.getExistingDirectory(None, 'Select Folder to Save', prev_dir)
        if fileDir != '':
            open_dir = ''
            file_list = str(fileDir).split('/')
            for i in range(0, len(file_list) - 1):
                if i < len(file_list) - 1:
                    open_dir += file_list[i] + '\\'
                elif i == len(file_list) - 1:
                    open_dir += file_list[i]
            fileDir.replace('/', '\\')
            self.dsave_directory = fileDir
            self.ui.lineEdit_dsave_directory.setText(fileDir)
            self.ui.label_condition.setText("Dynamic saving directory selected.")
        else:
            self.ui.lineEdit_dsave_directory.setText('None')
            self.ui.label_condition.setText('Choose a directory for dynamic saving.')
            
    def Dsave_directory(self):
        self.dsave_dir_ok = True
        if self.ui.lineEdit_dsave_directory.text() == '' or self.ui.lineEdit_dsave_directory.text() == 'None':
            self.dsave_dir_ok = False
        
    def Dsave_filename(self):
        self.dsave_filename_ok = True
        self.date = ''
        self.dsave_filename = ''
        if self.ui.radioButton_dsave_timename.isChecked():
            now = datetime.datetime.now()
            date = '%s-%s-%s' % (now.year, now.month, now.day)
            current_time = '%s.%s.%s' % (now.hour, now.minute, now.second)
            date_and_time = date + '_' + current_time
            self.date = date
            self.dsave_filename = str(date_and_time)
        elif self.ui.radioButton_dsave_custname.isChecked():
            self.dsave_filename = str(self.ui.lineEdit_dsave_custname.text())
            if self.dsave_filename == '':
                self.dsave_filename_ok = False
    
    def Dsave_filetype(self):
        if self.ui.radioButton_csv.isChecked():
            self.dsave_filetype = '.csv'
            self.dsave_divide = ','
        elif self.ui.radioButton_txt.isChecked():
            self.dsave_filetype = '.txt'
            self.dsave_divide = '\t'
            
    def Dsave_username(self):
        self.dsave_username_ok = True
        self.dsave_username = ''
        self.dsave_username = str(self.ui.lineEdit_dsave_username.text())
        if self.dsave_username == '':
            self.dsave_username_ok = False
            
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

    def input(self, ui, instruments, curves, curveWidgets, go_on, inputted_data, array_l, device_state, count, dsave, input_data):
        self.ui = ui
        self.curves = curves
        self.curveWidgets = curveWidgets
        self.go_on = go_on
        self.Data = inputted_data
        self.array_1 = array_l
        self.count = count
        self.Device1_state = device_state[0]
        self.dsave_directory = dsave[0]
        self.dsave_filename = dsave[1]
        self.dsave_username = dsave[2]
        self.dsave_thread = dsave[3]
        self.dsave_filetype = dsave[4]
        self.dsave_divide = dsave[5]
        self.date = dsave[6]
        self.input_data = input_data
        self.reading_wait = float(self.Data[1][6])
        self.turn_off_keithley = self.Data[1][4]
        for i in range(0, len(self.curves) - 4):
            self.curves[i].set_data([], [])
            self.curves[i].plot().replot()
            
        if self.count == 1:
            if self.Device1_state:
                self.lockin = instruments[0]
                self.keithley = instruments[1]
            
        self.pause_collecting = False
        self.stop_collecting = False
        
        #self.run()
        self.start()
    
    def stop(self):
        self.stop_collecting = True
        self.ui.label_condition.setText('Stopped.')
        self.ui.pushButton_Start.setEnabled(True)
        self.ui.pushButton_Pause.setEnabled(False)
        self.ui.pushButton_Stop.setEnabled(False)
    
    def pause(self):
        if self.pause_collecting:
            self.ui.label_condition.setText('Running...')
            self.ui.pushButton_Pause.setText("Pause")
            self.pause_collecting = False
        else:
            self.ui.label_condition.setText('Paused. Click continue to run.')
            self.ui.pushButton_Pause.setText("Continue")
            self.pause_collecting = True
    
    def run(self):
        import time
        
        
        self.start_time = time.time()
        
        Round = 1
        
        self.Voltage_sweep(Round)
                
        self.ui.pushButton_Start.setEnabled(True)
        self.ui.pushButton_Pause.setEnabled(False)
        self.ui.pushButton_Stop.setEnabled(False)
        self.ui.label_condition.setText('Scan complete.')
        if self.turn_off_keithley == "y":
            Keithley().turn_off(self.keithley)

    def Voltage_sweep(self, Round):
        import time
        self.Xvalues = []
        self.Yvalues = []
        self.Thetvalues = []
        self.GateVoltage = []
        self.GateCurrent = []
        num = 0
        time_collect = 0
        self.step = []
        while num < len(self.array_1):
            while self.pause_collecting:
                if self.stop_collecting:
                    break
                else:
                    pass
            if not self.stop_collecting:
                #self.run_time = time.time()
                # Time sleep
                # Device 1
                if self.Device1_state and num < len(self.array_1):
                    input_volt = str(float(self.array_1[num]))
                    Keithley().turn_on(self.keithley)
                    Keithley().set_voltage(self.keithley, input_volt)
                    time.sleep(self.reading_wait)
                    self.Reading("Keithley", float(input_volt), num, Round)
                num += 1
            else:
                break
    def Reading(self, device, input_volt, num, Round):
        self.run_time = time.time()
        
        #self.during = self.check_time - self.run_time
        now = datetime.datetime.now()
        date = '%s-%s-%s' % (now.year, now.month, now.day)
        current_time = '%s:%s:%s' % (now.hour, now.minute, now.second)
        self.date_and_time = date + ' ' + current_time
        #print 0
        # Device 1
        if device == "Keithley":
            Keithley().read_data_write(self.keithley)
            temp = Keithley().read_data_read(self.keithley)
            k_volt = float(temp[0])
            k_curr = float(temp[1])
            
            a = DigitalLockin().XYRTHET_query(self.lockin, 0, 1, 3)
            lockindata = numpy.fromstring(a, dtype = numpy.float32, count=3, sep=',')
            x = float(lockindata[0])
            y = float(lockindata[1])
            thet = float(lockindata[2])
            
            self.GateVoltage.append(k_volt)
            self.GateCurrent.append(k_curr)
            self.Xvalues.append(x)
            self.Yvalues.append(y)
            self.Thetvalues.append(thet)
            
            #print str(k_volt)  + " " + str(k_curr) + " " + str(x) + ' ' + str(y) +  ' ' + str(thet)
            
            lockin_params = DigitalLockin().param_query(self.lockin)
            self.step.append(num)
            self.check_time = time.time()
            self.total_during = self.check_time - self.start_time
            self.during = self.check_time - self.run_time
            self.emit(SIGNAL('print_value'), "Keithley", [self.total_during, self.during, k_volt, k_curr, x, y, thet, lockin_params, self.Data[3][1]])
            self.setup_plot(self.curveWidgets[0], self.curves[0], [self.step, self.GateVoltage], ['Gate Voltage', "Step", "Volt (V)"])
            self.setup_plot(self.curveWidgets[1], self.curves[1], [self.GateVoltage, self.Xvalues], ['X vs Gate Voltage', "Volt (V)", "Volt (V)"])
            self.setup_plot(self.curveWidgets[2], self.curves[2], [self.GateVoltage, self.Yvalues], ['Y vs Gate Voltage', "Volt (V)", "Volt (V)"])
            self.setup_plot(self.curveWidgets[3], self.curves[3], [self.GateVoltage, self.Thetvalues], ['Theta vs Gate Voltage', "Volt (V)", "Theta (Deg)"])
            self.Pre_dynamic_save(num, False, [k_volt, k_curr, x, y, thet, lockin_params], 2, Round)

    def Pre_dynamic_save(self, num, is_last, data_lst, i, Round):
        if self.ui.checkBox_dsave.isChecked():
            is_first = False
            comments = []
            parameters = []
            units = []
            data = []
            file_info = []
            
            # File_info
            # First is file name
            file_info.append(self.Data[3][1] + '_' + self.dsave_filename)
            # csv file
            file_info.append(self.dsave_filetype)
            # the divide of csv is ","
            file_info.append(self.dsave_divide)
            # Always "Collected Data"
            file_info.append('Collected Data')
            # The saving directory
            file_info.append(self.dsave_directory + '\\' + self.Data[3][1] + '_' + self.date)
            
            if is_last:
                self.dsave_thread.input(comments, parameters, units, data, file_info, is_first, is_last)
            else:
                data.append(self.date_and_time)
                #data.append(self.during)
                data.append(num)
                data.append(data_lst[0])
                data.append(data_lst[1])
                data.append(data_lst[2])
                data.append(data_lst[3])
                data.append(data_lst[4])
                data.append(data_lst[5][0][0])
                data.append(data_lst[5][0][1])
                data.append(data_lst[5][0][2])
                data.append(data_lst[5][0][3])
                data.append(data_lst[5][0][4])
                data.append(data_lst[5][0][5])
                data.append(data_lst[5][0][6])
                data.append(data_lst[5][0][7])
                data.append(data_lst[5][0][8])
                data.append(data_lst[5][0][9])
                data.append(data_lst[5][0][10])
                data.append(data_lst[5][0][11])
                data.append(data_lst[5][0][12])
                data.append(data_lst[5][0][13])
                data.append(data_lst[5][0][14])
                
                if num == 0:
                    is_first = True
                    
                    # User name
                    temp = []
                    temp.append('User Name:')
                    temp.append(self.dsave_username)
                    comments.append(temp)
                    # Edit Time
                    temp = []
                    temp.append('Edit Time:')
                    temp.append(str(datetime.datetime.now()))
                    comments.append(temp)
                    # Yokogawa1 visa address
                    temp = []
                    temp.append('Lockin Visa Address:')
                    temp.append(str(self.ui.comboBox_visa_1.currentText()))
                    comments.append(temp)
                    temp = []
                    temp.append('Lockin Visa Name:')
                    name = str(self.ui.label_visa_1.text())
                    name = name.rstrip()
                    temp.append(name)
                    comments.append(temp)
                    # Agilent1 visa address
                    temp = []
                    temp.append('Keithley Visa Address:')
                    temp.append(str(self.ui.comboBox_visa_2.currentText()))
                    comments.append(temp)
                    temp = []
                    temp.append('Keithly Visa Name:')
                    name = str(self.ui.label_visa_2.text())
                    name = name.rstrip()
                    temp.append(name)
                    comments.append(temp)
                    temp = []
                    temp.append('Comments:')
                    temp.append(str(self.ui.textEdit_dsave_comment.toPlainText()))
                    comments.append(temp)
                    # New line
                    temp = []
                    temp.append('')
                    comments.append(temp)
                    # Lock-in Parameters
                    temp = []
                    temp.append(self.ui.textEdit.toPlainText())
                    comments.append(temp)
                    parameters.append('date')
                    units.append('date')
                    parameters.append('step')
                    units.append('int')
                    parameters.append('k_volt')
                    units.append('V')
                    parameters.append('k_curr')
                    units.append('A')
                    parameters.append('x')
                    units.append('V')
                    parameters.append('y')
                    units.append('V')
                    parameters.append('thet')
                    units.append('Deg')
                    parameters.append(data_lst[5][1][0])
                    parameters.append(data_lst[5][1][1])
                    parameters.append(data_lst[5][1][2])
                    parameters.append(data_lst[5][1][3])
                    parameters.append(data_lst[5][1][4])
                    parameters.append(data_lst[5][1][5])
                    parameters.append(data_lst[5][1][6])
                    parameters.append(data_lst[5][1][7])
                    parameters.append(data_lst[5][1][8])
                    parameters.append(data_lst[5][1][9])
                    parameters.append(data_lst[5][1][10])
                    parameters.append(data_lst[5][1][11])
                    parameters.append(data_lst[5][1][12])
                    parameters.append(data_lst[5][1][13])
                    parameters.append(data_lst[5][1][14])
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    units.append('NA')
                    print len(data)
                    print len(parameters)
                    print len(units)
                    self.dsave_thread.input(comments, parameters, units, data, file_info, is_first, is_last)
                else:
                    self.dsave_thread.input(comments, parameters, units, data, file_info, is_first, is_last)
      
        
    def setup_plot(self, curveWidget, curve, data, titles):
        curveWidget.plot.set_titles(titles[0], titles[1], titles[2])
        curve.set_data(data[0], data[1])
        self.emit(SIGNAL("curve_plot"), [curveWidget, curve])
    
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
        
        

        
