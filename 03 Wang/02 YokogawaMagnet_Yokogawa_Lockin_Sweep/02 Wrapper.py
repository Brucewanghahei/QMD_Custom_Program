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
from Sub_Scripts.Agilent import Agilent
from Sub_Scripts.Magnet import Magnet

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
        self.connect(self.ui.pushButton_update_5, SIGNAL('clicked()'), lambda : self.Update("visa5", self.ui.comboBox_visa_5))
        self.connect(self.ui.pushButton_update_6, SIGNAL('clicked()'), lambda : self.Update("visa4", self.ui.comboBox_visa_6))
        self.connect(self.ui.pushButton_update_7, SIGNAL('clicked()'), lambda : self.Update("visa5", self.ui.comboBox_visa_7))
        self.connect(self.ui.pushButton_select_1, SIGNAL('clicked()'), lambda : self.Select("visa1", self.visa1, self.ui.comboBox_visa_1, self.ui.label_visa_1, [self.ui.pushButton_select_1, self.ui.pushButton_close_1]))
        self.connect(self.ui.pushButton_select_2, SIGNAL('clicked()'), lambda : self.Select("visa2", self.visa2, self.ui.comboBox_visa_2, self.ui.label_visa_2, [self.ui.pushButton_select_2, self.ui.pushButton_close_2]))
        self.connect(self.ui.pushButton_select_3, SIGNAL('clicked()'), lambda : self.Select("visa3", self.visa3, self.ui.comboBox_visa_3, self.ui.label_visa_3, [self.ui.pushButton_select_3, self.ui.pushButton_close_3]))
        self.connect(self.ui.pushButton_select_4, SIGNAL('clicked()'), lambda : self.Select("visa4", self.visa4, self.ui.comboBox_visa_4, self.ui.label_visa_4, [self.ui.pushButton_select_4, self.ui.pushButton_close_4]))
        self.connect(self.ui.pushButton_select_5, SIGNAL('clicked()'), lambda : self.Select("visa5", self.visa5, self.ui.comboBox_visa_5, self.ui.label_visa_5, [self.ui.pushButton_select_5, self.ui.pushButton_close_5]))
        self.connect(self.ui.pushButton_select_6, SIGNAL('clicked()'), lambda : self.Select("visa6", self.visa6, self.ui.comboBox_visa_6, self.ui.label_visa_6, [self.ui.pushButton_select_6, self.ui.pushButton_close_6]))
        self.connect(self.ui.pushButton_select_7, SIGNAL('clicked()'), lambda : self.Select("visa7", self.visa7, self.ui.comboBox_visa_7, self.ui.label_visa_7, [self.ui.pushButton_select_7, self.ui.pushButton_close_7]))
        self.connect(self.ui.pushButton_close_1, SIGNAL('clicked()'), lambda : self.Close("visa1", self.visa1, self.ui.label_visa_1, [self.ui.pushButton_select_1, self.ui.pushButton_close_1]))
        self.connect(self.ui.pushButton_close_2, SIGNAL('clicked()'), lambda : self.Close("visa2", self.visa2, self.ui.label_visa_2, [self.ui.pushButton_select_2, self.ui.pushButton_close_2]))
        self.connect(self.ui.pushButton_close_3, SIGNAL('clicked()'), lambda : self.Close("visa3", self.visa3, self.ui.label_visa_3, [self.ui.pushButton_select_3, self.ui.pushButton_close_3]))
        self.connect(self.ui.pushButton_close_4, SIGNAL('clicked()'), lambda : self.Close("visa4", self.visa4, self.ui.label_visa_4, [self.ui.pushButton_select_4, self.ui.pushButton_close_4]))
        self.connect(self.ui.pushButton_close_5, SIGNAL('clicked()'), lambda : self.Close("visa5", self.visa5, self.ui.label_visa_5, [self.ui.pushButton_select_5, self.ui.pushButton_close_5]))
        self.connect(self.ui.pushButton_close_6, SIGNAL('clicked()'), lambda : self.Close("visa6", self.visa6, self.ui.label_visa_6, [self.ui.pushButton_select_6, self.ui.pushButton_close_6]))
        self.connect(self.ui.pushButton_close_7, SIGNAL('clicked()'), lambda : self.Close("visa7", self.visa7, self.ui.label_visa_7, [self.ui.pushButton_select_7, self.ui.pushButton_close_7]))
        
        self.connect(self.ui.pushButton_Start, SIGNAL('clicked()'), self.start)
        self.connect(self.ui.pushButton_Stop, SIGNAL('clicked()'), self.collect_data_thread.stop)
        self.connect(self.ui.pushButton_Pause, SIGNAL('clicked()'), self.collect_data_thread.pause)
        
        self.connect(self.collect_data_thread, SIGNAL("curve_plot"), self.curvePlots_update)
        self.connect(self.collect_data_thread, SIGNAL("magnet_update"), self.setup_plot)
        self.connect(self.collect_data_thread, SIGNAL("print_value"), self.Print_data)
        self.connect(self.ui.checkBox_dsave, SIGNAL("clicked()"), self.Pre_dsave)
        self.connect(self.ui.textEdit, SIGNAL('textChanged ()'), lambda : self.start_font("C"))
        self.connect(self.ui.pushButton_dsave_browse, SIGNAL('clicked()'), self.Dsave_browse)
        
        self.Update("visa1", self.ui.comboBox_visa_1)
        self.Update("visa2", self.ui.comboBox_visa_2)
        self.Update("visa3", self.ui.comboBox_visa_3)
        self.Update("visa4", self.ui.comboBox_visa_4)
        self.Update("visa5", self.ui.comboBox_visa_5)
        self.Update("visa6", self.ui.comboBox_visa_6)
        self.Update("visa7", self.ui.comboBox_visa_7)
        
        self.curve_1 = self.make_curveWidgets(self.ui.curvewidget_1, "b", "blue", titles = ["Magnet", "Step", "Current (mA)"])
        self.curve_1_update = self.make_curveWidgets(self.ui.curvewidget_1, "red", "red", titles = ["Magnet", "Step", "Current (mA)"])
        self.curve_2_b = self.make_curveWidgets(self.ui.curvewidget_2, "black", "black", titles = ["Yokogawa1", "Step", "Voltage (mV)"])
        self.curve_2_r = self.make_curveWidgets(self.ui.curvewidget_2, "red", "red", titles = ["Yokogawa1", "Step", "Voltage (mV)"])
        self.curve_3_b = self.make_curveWidgets(self.ui.curvewidget_3, "black", "black", titles = ["Yokogawa2", "Step", "Voltage (mV)"])
        self.curve_3_r = self.make_curveWidgets(self.ui.curvewidget_3, "red", "red", titles = ["Yokogawa2", "Step", "Voltage (mV)"])
        self.curve_4_b = self.make_curveWidgets(self.ui.curvewidget_4, "black", "black", titles = ["Yokogawa3", "Step", "Voltage (mV)"])
        self.curve_4_r = self.make_curveWidgets(self.ui.curvewidget_4, "red", "red", titles = ["Yokogawa3", "Step", "Voltage (mV)"])

        self.Curve1 = self.make_curveWidgets(self.ui.curvewidget_13, "r", "black", titles = ["Plot 1", "X (x)", "Y (y)"])
        self.Curve2 = self.make_curveWidgets(self.ui.curvewidget_14, "g", "black", titles = ["Plot 2", "X (x)", "Y (y)"])
        self.Curve3 = self.make_curveWidgets(self.ui.curvewidget_15, "blue", "black", titles = ["Plot 3", "X (x)", "Y (y)"])
        
        self.visa1 = None
        self.visa2 = None
        self.visa3 = None
        self.visa4 = None
        self.visa5 = None
        self.visa6 = None
        self.visa7 = None

        self.setWindowTitle("Yokogawa-Magnetic Sweep with Voltage Bias Lock-in")
        
        self.input_string = []
        self.input_string.append("00 Run_Number: 01\n\n")
        
        self.input_string.append("01 Field TimeStep(s): 1\n")
        self.input_string.append("02 Field Sweep Start (mA): -13.66\n")
        self.input_string.append("03 Field Sweep Stop (mA): 200\n")
        self.input_string.append("04 Field Sweep Step (mA): 2.27\n\n")
        self.input_string.append("05 Yokogawa Ramp TimeStep(s): 0.2\n")
        self.input_string.append("06 Yokogawa Collect TimeStep(s): 1.8\n\n")
        
        self.input_string.append("07 Device 1 Measure (y/n): y\n")
        self.input_string.append("08 Lock-in Sense: 200e-6\n")
        self.input_string.append("09 Pre-Amp Gain: 100\n")
        self.input_string.append("10 Lock-in Resistor(Ohms): 1e6\n")
        self.input_string.append("11 Yokogawa Resistor(Ohms): 1e5\n")
        self.input_string.append("12 Output Voltage(mV): 50\n")
        self.input_string.append("13 Initial Ramp Start(mV): 0\n")
        self.input_string.append("14 Initial Ramp End(mV): -5000\n")
        self.input_string.append("15 Initial Ramp Step(mV): -100\n")
        self.input_string.append("16 Collecting Start(mV): -5000\n")
        self.input_string.append("17 Collecting Stop(mV): 5000\n")
        self.input_string.append("18 Collecting Step(mV): 100\n")
        self.input_string.append("19 Final Ramp Start(mV): 5000\n")
        self.input_string.append("20 Final Ramp Stop(mV): 0\n")
        self.input_string.append("21 Final Ramp Step(mV): -100\n")
        self.input_string.append("22 File Name: Device4\n\n")
        
        self.input_string.append("23 Device 2 Measure (y/n): y\n")
        self.input_string.append("24 Lock-in Sense: 200e-6\n")
        self.input_string.append("25 Pre-Amp Gain: 100\n")
        self.input_string.append("26 Lock-in Resistor(Ohms): 1e6\n")
        self.input_string.append("27 Yokogawa Resistor(Ohms): 1e5\n")
        self.input_string.append("28 Output Voltage(mV): 50\n")
        self.input_string.append("29 Initial Ramp Start(mV): 0\n")
        self.input_string.append("30 Initial Ramp End(mV): -5000\n")
        self.input_string.append("31 Initial Ramp Step(mV): -100\n")
        self.input_string.append("32 Collecting Start(mV): -5000\n")
        self.input_string.append("33 Collecting Stop(mV): 5000\n")
        self.input_string.append("34 Collecting Step(mV): 100\n")
        self.input_string.append("35 Final Ramp Start(mV): 5000\n")
        self.input_string.append("36 Final Ramp Stop(mV): 0\n")
        self.input_string.append("37 Final Ramp Step(mV): -100\n")
        self.input_string.append("38 File Name: Device5\n\n")
        
        self.input_string.append("39 Device 3 Measure (y/n): y\n")
        self.input_string.append("40 Lock-in Sense: 200e-6\n")
        self.input_string.append("41 Pre-Amp Gain: 100\n")
        self.input_string.append("42 Lock-in Resistor(Ohms): 1e6\n")
        self.input_string.append("43 Yokogawa Resistor(Ohms): 1e5\n")
        self.input_string.append("44 Output Voltage(mV): 50\n")
        self.input_string.append("45 Initial Ramp Start(mV): 0\n")
        self.input_string.append("46 Initial Ramp End(mV): -5000\n")
        self.input_string.append("47 Initial Ramp Step(mV): -100\n")
        self.input_string.append("48 Collecting Start(mV): -5000\n")
        self.input_string.append("49 Collecting Stop(mV): 5000\n")
        self.input_string.append("50 Collecting Step(mV): 100\n")
        self.input_string.append("51 Final Ramp Start(mV): 5000\n")
        self.input_string.append("52 Final Ramp Stop(mV): 0\n")
        self.input_string.append("53 Final Ramp Step(mV): -100\n")
        self.input_string.append("54 File Name: Device9\n")
        
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
        
        self.Visa_addresses = [["Yokogawa GS200", "YOKOGAWA"], ["Agilent 34460A", "Agilent Technologies"], ["Magnet Model 430", "AMERICAN MAGNETICS INC."]]
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
        elif signal == "visa5":
            self.ui.comboBox_visa_5.clear()
        elif signal == "visa6":
            self.ui.comboBox_visa_6.clear()
        elif signal == "visa7":
            self.ui.comboBox_visa_7.clear()
        
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
            elif signal == "visa6":
                self.ui.comboBox_visa_6.addItem(temp)
            elif signal == "visa7":
                self.ui.comboBox_visa_7.addItem(temp)
        
        # if signal == "visa1":
        #     self.ui.comboBox_visa_1.addItem(alls[3])
        # elif signal == "visa2":
        #     self.ui.comboBox_visa_2.addItem(alls[0])
        # elif signal == "visa3":
        #     self.ui.comboBox_visa_3.addItem(alls[4])
        # elif signal == "visa4":
        #     self.ui.comboBox_visa_4.addItem(alls[1])
        # elif signal == "visa5":
        #     self.ui.comboBox_visa_5.addItem(alls[5])
        # elif signal == "visa6":
        #     self.ui.comboBox_visa_6.addItem(alls[2])
        # elif signal == "visa7":
        #     self.ui.comboBox_visa_7.addItem(alls[6])
    
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
                if first_name == "YOKOGAWA":
                    if self.Ready(inst):
                        lineEditVisa.setText(visa_name)
                        selectClose[0].setEnabled(False)
                        selectClose[1].setEnabled(True)
                        self.visa1 = inst
                        self.Mark(inst, False)
                        self.ui.label_condition.setText("Visa is selected succefully!")
                    else:
                        self.ui.label_condition.setText("Pick another Yokogawa address")
                else:
                    self.ui.label_condition.setText("Invalid Yokogawa address")
            elif signal == "visa2":
                if first_name == "Agilent Technologies":
                    if self.Ready(inst):
                        lineEditVisa.setText(visa_name)
                        selectClose[0].setEnabled(False)
                        selectClose[1].setEnabled(True)
                        self.visa2 = inst
                        self.Mark(inst, False)
                        self.ui.label_condition.setText("Visa is selected succefully!")
                    else:
                        self.ui.label_condition.setText("Pick another Agilent address")
                else:
                    self.ui.label_condition.setText("Invalid Agilent address")
            elif signal == "visa3":
                if first_name == "YOKOGAWA":
                    if self.Ready(inst):
                        lineEditVisa.setText(visa_name)
                        selectClose[0].setEnabled(False)
                        selectClose[1].setEnabled(True)
                        self.visa3 = inst
                        self.Mark(inst, False)
                        self.ui.label_condition.setText("Visa is selected succefully!")
                    else:
                        self.ui.label_condition.setText("Pick another Yokogawa address")
                else:
                    self.ui.label_condition.setText("Invalid Yokogawa address")
            elif signal == "visa4":
                if first_name == "Agilent Technologies":
                    if self.Ready(inst):
                        lineEditVisa.setText(visa_name)
                        selectClose[0].setEnabled(False)
                        selectClose[1].setEnabled(True)
                        self.visa4 = inst
                        self.Mark(inst, False)
                        self.ui.label_condition.setText("Visa is selected succefully!")
                    else:
                        self.ui.label_condition.setText("Pick another Agilent address")
                else:
                    self.ui.label_condition.setText("Invalid Agilent address")
            elif signal == "visa5":
                if first_name == "YOKOGAWA":
                    if self.Ready(inst):
                        lineEditVisa.setText(visa_name)
                        selectClose[0].setEnabled(False)
                        selectClose[1].setEnabled(True)
                        self.visa5 = inst
                        self.Mark(inst, False)
                        self.ui.label_condition.setText("Visa is selected succefully!")
                    else:
                        self.ui.label_condition.setText("Pick another Yokogawa address")
                else:
                    self.ui.label_condition.setText("Invalid Yokogawa address")
            elif signal == "visa6":
                if first_name == "Agilent Technologies":
                    if self.Ready(inst):
                        lineEditVisa.setText(visa_name)
                        selectClose[0].setEnabled(False)
                        selectClose[1].setEnabled(True)
                        self.visa6 = inst
                        self.Mark(inst, False)
                        self.ui.label_condition.setText("Visa is selected succefully!")
                    else:
                        self.ui.label_condition.setText("Pick another Agilent address")
                else:
                    self.ui.label_condition.setText("Invalid Agilent address")
            elif signal == "visa7":
                if first_name == "YOKOGAWA":
                    if self.Ready(inst):
                        lineEditVisa.setText(visa_name)
                        selectClose[0].setEnabled(False)
                        selectClose[1].setEnabled(True)
                        self.visa7 = inst
                        self.Mark(inst, False)
                        self.ui.label_condition.setText("Visa is selected succefully!")
                    else:
                        self.ui.label_condition.setText("Pick another Yokogawa address")
                else:
                    self.ui.label_condition.setText("Invalid Yokogawa address")
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
        elif signal == "visa5":
            visa_chosen.close()
            self.visa5 = None
            #self.Disable(signal)
        elif signal == "visa6":
            visa_chosen.close()
            self.visa5 = None
            #self.Disable(signal)
        elif signal == "visa7":
            visa_chosen.close()
            self.visa7 = None
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
    
    def array_builder(self, start, stop, step):
        if start < stop:
            array = numpy.arange(start, stop + step, abs(step))
        elif start > stop:
            array = numpy.arange(stop, start - step, abs(step))[::-1]
        return array
            
    def start(self):
        self.Device1_state = False
        self.Device2_state = False
        self.Device3_state = False
        
        self.instruments = []
        curves = [self.Curve1, self.Curve2, self.Curve3, self.curve_1, self.curve_1_update]
        curveWidgets =[self.ui.curvewidget_13, self.ui.curvewidget_14, self.ui.curvewidget_15, self.ui.curvewidget_1]
        array_1 = []
        array_2 = []
        array_3 = []
        go_on = True
        
        input_data = []
        temp = str(self.ui.textEdit.toPlainText()).split("\n")
        for i in range(0, len(temp)):
            if temp[i] != '':
                input_data.append(temp[i])
        inputted_data = []
        inputted_data.append([input_data[0].split(":")[1].replace(" ", "")])
        temp = []
        for i in range(1, 7):
            temp.append(input_data[i].split(":")[1].replace(" ", ""))
        inputted_data.append(temp)
        temp = []
        for i in range(7, 23):
            temp.append(input_data[i].split(":")[1].replace(" ", ""))
        inputted_data.append(temp)
        temp = []
        for i in range(23, 39):
            temp.append(input_data[i].split(":")[1].replace(" ", ""))
        inputted_data.append(temp)
        temp = []
        for i in range(39, 55):
            temp.append(input_data[i].split(":")[1].replace(" ", ""))
        inputted_data.append(temp)
        
        if inputted_data[2][0].upper() == 'Y' or inputted_data[2][0].upper() == 'YES':
            self.Device1_state = True
        if inputted_data[3][0].upper() == 'Y' or inputted_data[3][0].upper() == 'YES':
            self.Device2_state = True
        if inputted_data[4][0].upper() == 'Y' or inputted_data[4][0].upper() == 'YES':
            self.Device3_state = True
        device_state = [self.Device1_state, self.Device2_state, self.Device3_state]
        
        #Make Array
        array_M = self.array_builder(float(inputted_data[1][1]), float(inputted_data[1][2]), float(inputted_data[1][3]))
        count = 0
        if self.Device1_state:
            count += 1
            temp = []
            temp = self.array_builder(float(inputted_data[2][6]), float(inputted_data[2][7]), float(inputted_data[2][8]))
            array_1.append(temp)
            temp = []
            temp = self.array_builder(float(inputted_data[2][9]), float(inputted_data[2][10]), float(inputted_data[2][11]))
            array_1.append(temp)
            temp = []
            temp = self.array_builder(float(inputted_data[2][12]), float(inputted_data[2][13]), float(inputted_data[2][14]))
            array_1.append(temp)
        if self.Device2_state:
            count += 1
            temp = []
            temp = self.array_builder(float(inputted_data[3][6]), float(inputted_data[3][7]), float(inputted_data[3][8]))
            array_2.append(temp)
            temp = []
            temp = self.array_builder(float(inputted_data[3][9]), float(inputted_data[3][10]), float(inputted_data[3][11]))
            array_2.append(temp)
            temp = []
            temp = self.array_builder(float(inputted_data[3][12]), float(inputted_data[3][13]), float(inputted_data[3][14]))
            array_2.append(temp)
        if self.Device3_state:
            count += 1
            temp = []
            temp = self.array_builder(float(inputted_data[4][6]), float(inputted_data[4][7]), float(inputted_data[4][8]))
            array_3.append(temp)
            temp = []
            temp = self.array_builder(float(inputted_data[4][9]), float(inputted_data[4][10]), float(inputted_data[4][11]))
            array_3.append(temp)
            temp = []
            temp = self.array_builder(float(inputted_data[4][12]), float(inputted_data[4][13]), float(inputted_data[4][14]))
            array_3.append(temp)
        
        array_lst = [array_M, array_1, array_2, array_3]
        
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
                                self.ui.pushButton_Pause.setEnabled(True)
                                self.ui.pushButton_Stop.setEnabled(True)
                                file_par = open("parameters.txt", "w").write(str(self.ui.textEdit.toPlainText()))
                                self.collect_data_thread.input(self.ui, self.instruments, curves, curveWidgets, go_on, inputted_data, array_lst, device_state, count, dsave, input_data)
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
            self.setup_plot(self.curve_1, array_M)
            self.setup_plot_2(self.curve_2_b, self.curve_2_r, [[],[],[]])
            self.setup_plot_2(self.curve_3_b, self.curve_3_r, [[],[],[]])
            self.setup_plot_2(self.curve_4_b, self.curve_4_r, [[],[],[]])
            if self.Device1_state:
                self.setup_plot_2(self.curve_2_b, self.curve_2_r, array_1)
            if self.Device2_state:
                self.setup_plot_2(self.curve_3_b, self.curve_3_r, array_2)
            if self.Device3_state:
                self.setup_plot_2(self.curve_4_b, self.curve_4_r, array_3)
            self.ui.tabWidget.setCurrentIndex(0)
            self.start_font("S")
    
    def Check_ready(self, count):
        if count == 1:
            if self.ui.label_visa_1.text() != '' and self.ui.label_visa_2.text() != '' and self.ui.label_visa_7.text() != '':
                self.instruments = [self.visa1, self.visa2, self.visa7]
                return True
            elif self.ui.label_visa_3.text() != '' and self.ui.label_visa_4.text() != '' and self.ui.label_visa_7.text() != '':
                self.instruments = [self.visa3, self.visa4, self.visa7]
                return True
            elif self.ui.label_visa_5.text() != '' and self.ui.label_visa_6.text() != '' and self.ui.label_visa_7.text() != '':
                self.instruments = [self.visa5, self.visa6, self.visa7]
                return True
        elif count == 2:
            if self.ui.label_visa_1.text() != '' and self.ui.label_visa_2.text() != '' and self.ui.label_visa_3.text() != '' and self.ui.label_visa_4.text() != '' and self.ui.label_visa_7.text() != '':
                self.instruments = [self.visa1, self.visa2, self.visa3, self.visa4, self.visa7]
                return True
            elif self.ui.label_visa_1.text() != '' and self.ui.label_visa_2.text() != '' and self.ui.label_visa_5.text() != '' and self.ui.label_visa_6.text() != '' and self.ui.label_visa_7.text() != '':
                self.instruments = [self.visa1, self.visa2, self.visa5, self.visa6, self.visa7]
                return True
            elif self.ui.label_visa_3.text() != '' and self.ui.label_visa_4.text() != '' and self.ui.label_visa_5.text() != '' and self.ui.label_visa_6.text() != '' and self.ui.label_visa_7.text() != '':
                self.instruments = [self.visa3, self.visa4, self.visa5, self.visa6, self.visa7]
                return True
        elif count == 3:
            if self.ui.label_visa_1.text() != '' and self.ui.label_visa_2.text() != '' and self.ui.label_visa_3.text() != '' and self.ui.label_visa_4.text() != '' and self.ui.label_visa_5.text() != '' and self.ui.label_visa_6.text() != ''and self.ui.label_visa_7.text() != '':
                self.instruments = [self.visa1, self.visa2, self.visa3, self.visa4, self.visa5, self.visa6, self.visa7]
                return True
        return False
    
    def setup_plot(self, curve, data):
        x = []
        for i in range(0, len(data)):
            x.append(i)
        curve.set_data(x, data)
        curve.plot().replot()
    
    def setup_plot_2(self, curve_b, curve_r, data):
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        num = 0
        for i in range(0, len(data[0])):
            x1.append(num)
            y1.append(data[0][i])
            num += 1
        num -= 1
        for i in range(0, len(data[1])):
            x2.append(num)
            y2.append(data[1][i])
            num += 1
        num -= 1
        for i in range(0, len(data[2])):
            x1.append(num)
            y1.append(data[2][i])
            num += 1
        curve_b.set_data(x1, y1)
        curve_r.set_data(x2, y2)
        curve_b.plot().replot()
        curve_r.plot().replot()
            
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
        self.out0_3 = str(format(text[2], '.3f'))
        self.out0_4 = str(format(text[2] * self.Coil_Constant, '.3f'))
        
        display_text = ""                
        display_text = display_text + "Time: " + self.out0_1 + " s\n"
        display_text = display_text + "Time Step: " + self.out0_2 + " s\n"
        display_text = display_text + "Magnet Yokogawa: " + self.out0_3 + " mA\n"
        display_text = display_text + "Magnet Field: " + self.out0_4 + " mT\n\n"
            
        if device == "Yokogawa1":
            self.out1_0 = text[6]
            out1_1 = text[3]
            self.scale1_1 = self.Switch_scale(out1_1)
            self.out1_1 = str(format(out1_1 * self.scale1_1[0], '.3f'))
            out1_2 = text[4]
            self.scale1_2 = self.Switch_scale(out1_2)
            self.out1_2 = str(format(out1_2 * self.scale1_2[0], '.3f'))
            out1_3 = text[5]
            self.scale1_3 = self.Switch_scale(out1_3)
            self.out1_3 = str(format(out1_3 * self.scale1_3[0], '.3f'))
        elif device == "Yokogawa2":
            self.out2_0 = text[6]
            out2_1 = text[3]
            self.scale2_1 = self.Switch_scale(out2_1)
            self.out2_1 = str(format(out2_1 * self.scale2_1[0], '.3f'))
            out2_2 = text[4]
            self.scale2_2 = self.Switch_scale(out2_2)
            self.out2_2 = str(format(out2_2 * self.scale2_2[0], '.3f'))
            out2_3 = text[5]
            self.scale2_3 = self.Switch_scale(out2_3)
            self.out2_3 = str(format(out2_3 * self.scale2_3[0], '.3f'))
        elif device == "Yokogawa3":
            self.out3_0 = text[6]
            out3_1 = text[3]
            self.scale3_1 = self.Switch_scale(out3_1)
            self.out3_1 = str(format(out3_1 * self.scale3_1[0], '.3f'))
            out3_2 = text[4]
            self.scale3_2 = self.Switch_scale(out3_2)
            self.out3_2 = str(format(out3_2 * self.scale3_2[0], '.3f'))
            out3_3 = text[5]
            self.scale3_3 = self.Switch_scale(out3_3)
            self.out3_3 = str(format(out3_3 * self.scale3_3[0], '.3f'))
            
        if self.Device1_state:
            display_text = display_text + self.out1_0 + " Input: " + self.out1_1 + " " + self.scale1_1[1] + "V\n"
            display_text = display_text + self.out1_0 + " Current: " + self.out1_2 + " " + self.scale1_2[1] + "A\n"
            display_text = display_text + self.out1_0 + " Resistivity: " + self.out1_3 + " " + self.scale1_3[1] + "Ohms\n"
        if self.Device2_state:
            display_text = display_text + self.out2_0 + " Input: " + self.out2_1 + " " + self.scale2_1[1] + "V\n"
            display_text = display_text + self.out2_0 + " Current: " + self.out2_2 + " " + self.scale2_2[1] + "A\n"
            display_text = display_text + self.out2_0 + " Resistivity: " + self.out2_3 + " " + self.scale2_3[1] + "Ohms\n"
        if self.Device3_state:
            display_text = display_text + self.out3_0 + " Input: " + self.out3_1 + " " + self.scale3_1[1] + "V\n"
            display_text = display_text + self.out3_0 + " Current: " + self.out3_2 + " " + self.scale3_2[1] + "A\n"
            display_text = display_text + self.out3_0 + " Resistivity: " + self.out3_3 + " " + self.scale3_3[1] + "Ohms\n"
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

    def input(self, ui, instruments, curves, curveWidgets, go_on, inputted_data, array_lst, device_state, count, dsave, input_data):
        self.ui = ui
        self.yokogawa1 = None
        self.agilent1 = None
        self.yokogawa2 = None
        self.agilent2 = None
        self.yokogawa3 = None
        self.agilent3 = None
        self.yokogawa_M = None
        self.curves = curves
        self.curveWidgets = curveWidgets
        self.go_on = go_on
        self.Data = inputted_data
        self.array_M = array_lst[0]
        self.array_1 = array_lst[1]
        self.array_2 = array_lst[2]
        self.array_3 = array_lst[3]
        self.count = count
        self.Device1_state = device_state[0]
        self.Device2_state = device_state[1]
        self.Device3_state = device_state[2]
        self.dsave_directory = dsave[0]
        self.dsave_filename = dsave[1]
        self.dsave_username = dsave[2]
        self.dsave_thread = dsave[3]
        self.dsave_filetype = dsave[4]
        self.dsave_divide = dsave[5]
        self.date = dsave[6]
        self.input_data = input_data
        self.field_step = float(self.Data[1][0])
        self.Yokogawa_ramp_step = float(self.Data[1][4])
        self.Yokogawa_collect_step = float(self.Data[1][5])
        
        if self.count == 1:
            if self.Device1_state:
                self.yokogawa1 = instruments[0]
                self.agilent1 = instruments[1]
                self.array_2 = self.array_1
                self.array_3 = self.array_1
            elif self.Device2_state:
                self.yokogawa2 = instruments[0]
                self.agilent2 = instruments[1]
                self.array_1 = self.array_2
                self.array_3 = self.array_2
            elif self.Device3_state:
                self.yokogawa3 = instruments[0]
                self.agilent3 = instruments[1]
                self.array_1 = self.array_3
                self.array_2 = self.array_3
            self.yokogawa_M = instruments[2]
        elif self.count == 2:
            if self.Device1_state and self.Device2_state:
                self.yokogawa1 = instruments[0]
                self.agilent1 = instruments[1]
                self.yokogawa2 = instruments[2]
                self.agilent2 = instruments[3]
                self.array_3 = self.array_1
            elif self.Device1_state and self.Device3_state:
                self.yokogawa1 = instruments[0]
                self.agilent1 = instruments[1]
                self.yokogawa3 = instruments[2]
                self.agilent3 = instruments[3]
                self.array_2 = self.array_1
            elif self.Device2_state and self.Device3_state:
                self.yokogawa2 = instruments[0]
                self.agilent2 = instruments[1]
                self.yokogawa3 = instruments[2]
                self.agilent3 = instruments[3]
                self.array_1 = self.array_2
            self.yokogawa_M = instruments[4]
        elif self.count == 3:
            if self.Device1_state and self.Device2_state and self.Device3_state:
                self.yokogawa1 = instruments[0]
                self.agilent1 = instruments[1]
                self.yokogawa2 = instruments[2]
                self.agilent2 = instruments[3]
                self.yokogawa3 = instruments[4]
                self.agilent3 = instruments[5]
            self.yokogawa_M = instruments[6]
            
        self.pause_collecting = False
        self.stop_collecting = False
        
        self.Coil_Constant = 1E-3/9.1E-3
        for i in range(0, len(self.curves) - 2):
            self.curves[i].set_data([], [])
            self.curves[i].plot().replot()
        
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
        self.yokogawa_M.write('SOUR:FUNC CURR')
        self.yokogawa_M.write('OUTP ON')
        
        Round = 1
        
        for i in range(0, len(self.array_M)):
            if self.go_on:
                while self.pause_collecting:
                    if self.stop_collecting:
                        break
                    else:
                        pass
                self.ui.label_condition.setText('Reading...')
                
                if not self.stop_collecting:
                    self.Current1 = []
                    self.Resistance1 = []
                    self.Current2 = []
                    self.Resistance2 = []
                    self.Current3 = []
                    self.Resistance3 = []
                    self.yokogawa_M.write('SOUR:LEV:AUTO ' + str(float(self.array_M[i]) * 1E-03))
                    time.sleep(self.field_step)
                    self.Sweep(float(self.array_M[i]), Round)
                    
                    # if self.Device1_state:
                    #     self.Pre_dynamic_save(num, True, [], 2, Round)
                    # if self.Device2_state:
                    #     self.Pre_dynamic_save(num, True, [], 3, Round)
                    # if self.Device3_state:
                    #     self.Pre_dynamic_save(num, True, [], 4, Round)
                    
                    self.emit(SIGNAL("magnet_update"), self.curves[3], self.array_M)
                    self.emit(SIGNAL("magnet_update"), self.curves[4], self.array_M[:Round])
                    
                    Round += 1
                else:
                    break
            else:
                self.ui.label_condition.setText('Reading stoped.')
        
        
        
        self.ui.pushButton_Start.setEnabled(True)
        self.ui.pushButton_Pause.setEnabled(False)
        self.ui.pushButton_Stop.setEnabled(False)
        self.ui.label_condition.setText('Scan complete.')
        
    def Sweep(self, input_M, Round):
        import time

        if self.Device1_state:
            self.agilent1.write('MEAS:VOLT?')
            self.yokogawa1.write('OUTP ON')
            self.yokogawa1.write('SOUR:FUNC VOLT')
        if self.Device2_state:
            self.agilent2.write('MEAS:VOLT?')
            self.yokogawa2.write('OUTP ON')
            self.yokogawa2.write('SOUR:FUNC VOLT')
        if self.Device3_state:
            self.agilent3.write('MEAS:VOLT?')
            self.yokogawa3.write('OUTP ON')
            self.yokogawa3.write('SOUR:FUNC VOLT')

        num = 0
        time_collect = 0
        while num < max(len(self.array_1[0]), len(self.array_2[0]), len(self.array_3[0])):
            while self.pause_collecting:
                if self.stop_collecting:
                    break
                else:
                    pass
            if not self.stop_collecting:
                # Device 1
                if self.Device1_state and num < len(self.array_1[0]):
                    input_volt = str(float(self.array_1[0][num]) * 1E-3)
                    self.yokogawa1.write('SOUR:LEV:AUTO ' + input_volt)
                # Device 2
                if self.Device2_state and num < len(self.array_2[0]):
                    input_volt = str(float(self.array_2[0][num]) * 1E-3)
                    self.yokogawa2.write('SOUR:LEV:AUTO ' + input_volt)
                # Device 3
                if self.Device3_state and num < len(self.array_3[0]):
                    input_volt = str(float(self.array_3[0][num]) * 1E-3)
                    self.yokogawa3.write('SOUR:LEV:AUTO ' + input_volt)
                num += 1
                time.sleep(self.Yokogawa_ramp_step)
            else:
                break
        
        num = 0
        while num < max(len(self.array_1[1]), len(self.array_2[1]), len(self.array_3[1])):
            while self.pause_collecting:
                if self.stop_collecting:
                    break
                else:
                    pass
            if not self.stop_collecting:
                self.run_time = time.time()
                # time sleep
                time.sleep(self.Yokogawa_collect_step)
                # Device 1
                if self.Device1_state and num < len(self.array_1[1]):
                    input_volt = str(float(self.array_1[1][num]) * 1E-3)
                    self.yokogawa1.write('SOUR:LEV:AUTO ' + input_volt)
                    self.Reading("Yokogawa1", float(input_volt), input_M, num, Round)
                # Device 2
                if self.Device2_state and num < len(self.array_2[1]):
                    input_volt = str(float(self.array_2[1][num]) * 1E-3)
                    self.yokogawa2.write('SOUR:LEV:AUTO ' + input_volt)
                    self.Reading("Yokogawa2", float(input_volt), input_M, num, Round)
                # Device 3
                if self.Device3_state and num < len(self.array_3[1]):
                    input_volt = str(float(self.array_3[1][num]) * 1E-3)
                    self.yokogawa3.write('SOUR:LEV:AUTO ' + input_volt)
                    self.Reading("Yokogawa3", float(input_volt), input_M, num, Round)
                num += 1
            else:
                break
        
        num = 0
        while num < max(len(self.array_1[2]), len(self.array_2[2]), len(self.array_3[2])):
            while self.pause_collecting:
                if self.stop_collecting:
                    break
                else:
                    pass
            if not self.stop_collecting:
                # Device 1
                if self.Device1_state and num < len(self.array_1[2]):
                    input_volt = float(self.array_1[2][num]) * 1E-3
                    self.yokogawa1.write('SOUR:LEV:AUTO ' + str(input_volt))
                # Device 2
                if self.Device2_state and num < len(self.array_2[2]):
                    input_volt = float(self.array_2[2][num]) * 1E-3
                    self.yokogawa2.write('SOUR:LEV:AUTO ' + str(input_volt))
                # Device 3
                if self.Device3_state and num < len(self.array_3[2]):
                    input_volt = float(self.array_3[2][num]) * 1E-3
                    self.yokogawa3.write('SOUR:LEV:AUTO ' + str(input_volt))
                num += 1
                time.sleep(self.Yokogawa_ramp_step)
            else:
                break
    
    def Reading(self, device, input_volt, input_M, num, Round):
        self.check_time = time.time()
        self.total_during = self.check_time - self.start_time
        self.during = self.check_time - self.run_time
        now = datetime.datetime.now()
        date = '%s-%s-%s' % (now.year, now.month, now.day)
        current_time = '%s:%s:%s' % (now.hour, now.minute, now.second)
        self.date_and_time = date + ' ' + current_time
        
        # Device 1
        if device == "Yokogawa1":
            lockin_sense = float(self.Data[2][1])
            pre_amp = float(self.Data[2][2]) * 10
            lockin_resist = float(self.Data[2][3])
            yoko_resist = float(self.Data[2][4])
            volt = float(self.agilent1.ask('READ?')) * lockin_sense / pre_amp
            curr = float(self.Data[2][5]) * 1E-3 / lockin_resist
            current = input_volt / yoko_resist
            resistance = volt / curr
            self.Current1.append(current)
            self.Resistance1.append(resistance)
            self.emit(SIGNAL('print_value'), "Yokogawa1", [self.total_during, self.during, input_M, input_volt, current, resistance, self.Data[2][15]])
            self.setup_plot(self.curveWidgets[0], self.curves[0], [self.Current1, self.Resistance1], [self.Data[2][15], "Current (A)", "Resistivity (Ohms)"])
            self.Pre_dynamic_save(num, False, [current, resistance, input_M], 2, Round)
        # Device 2
        elif device == "Yokogawa2":
            lockin_sense = float(self.Data[3][1])
            pre_amp = float(self.Data[3][2]) * 10
            lockin_resist = float(self.Data[3][3])
            yoko_resist = float(self.Data[3][4])
            volt = float(self.agilent2.ask('READ?')) * lockin_sense / pre_amp
            curr = float(self.Data[3][5]) * 1E-3 / lockin_resist
            current = input_volt / yoko_resist
            resistance = volt / curr
            self.Current2.append(current)
            self.Resistance2.append(resistance)
            self.emit(SIGNAL('print_value'), "Yokogawa2", [self.total_during, self.during, input_M, input_volt, current, resistance, self.Data[3][15]])
            self.setup_plot(self.curveWidgets[1], self.curves[1], [self.Current2, self.Resistance2], [self.Data[3][15], "Current (A)", "Resistivity (Ohms)"])
            self.Pre_dynamic_save(num, False, [current, resistance, input_M], 3, Round)
        # Device 3
        elif device == "Yokogawa3":
            lockin_sense = float(self.Data[4][1])
            pre_amp = float(self.Data[4][2]) * 10
            lockin_resist = float(self.Data[4][3])
            yoko_resist = float(self.Data[4][4])
            volt = float(self.agilent3.ask('READ?')) * lockin_sense / pre_amp
            curr = float(self.Data[4][5]) * 1E-3 / lockin_resist
            current = input_volt / yoko_resist
            resistance = volt / curr
            self.Current3.append(current)
            self.Resistance3.append(resistance)
            self.emit(SIGNAL('print_value'), "Yokogawa3", [self.total_during, self.during, input_M, input_volt, current, resistance, self.Data[4][15]])
            self.setup_plot(self.curveWidgets[2], self.curves[2], [self.Current3, self.Resistance3], [self.Data[4][15], "Current (A)", "Resistivity (Ohms)"])        
            self.Pre_dynamic_save(num, False, [current, resistance, input_M], 4, Round)
            
    def Pre_dynamic_save(self, num, is_last, data_lst, i, Round):
        magnet = str(data_lst[2] * self.Coil_Constant)
        magnet_ = str(format(data_lst[2] * self.Coil_Constant, '.3f'))
        if self.ui.checkBox_dsave.isChecked():
            is_first = False
            comments = []
            parameters = []
            units = []
            data = []
            file_info = []
            
            # File_info
            # First is file name
            file_info.append(self.Data[i][15] + '_' + str(Round) + '_' + magnet_ + 'mT_' + self.dsave_filename)
            # csv file
            file_info.append(self.dsave_filetype)
            # the divide of csv is ","
            file_info.append(self.dsave_divide)
            # Always "Collected Data"
            file_info.append('Collected Data')
            # The saving directory
            file_info.append(self.dsave_directory + '\\' + self.Data[i][15] + '_' + self.date)
            
            if is_last:
                self.dsave_thread.input(comments, parameters, units, data, file_info, is_first, is_last)
            else:
                data.append(self.date_and_time)
                data.append(self.total_during)
                data.append(num)
                data.append(data_lst[0])
                data.append(data_lst[1])
                
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
                    temp.append('Yokogawa1 Visa Address:')
                    temp.append(str(self.ui.comboBox_visa_1.currentText()))
                    comments.append(temp)
                    temp = []
                    temp.append('Yokogawa1 Visa Name:')
                    name = str(self.ui.label_visa_1.text())
                    name = name.rstrip()
                    temp.append(name)
                    comments.append(temp)
                    # Agilent1 visa address
                    temp = []
                    temp.append('Agilent1 Visa Address:')
                    temp.append(str(self.ui.comboBox_visa_2.currentText()))
                    comments.append(temp)
                    temp = []
                    temp.append('Agilent1 Visa Name:')
                    name = str(self.ui.label_visa_2.text())
                    name = name.rstrip()
                    temp.append(name)
                    comments.append(temp)
                    # Yokogawa2 visa address
                    temp = []
                    temp.append('Yokogawa2 Visa Address:')
                    temp.append(str(self.ui.comboBox_visa_3.currentText()))
                    comments.append(temp)
                    temp = []
                    temp.append('Yokogawa2 Visa Name:')
                    name = str(self.ui.label_visa_3.text())
                    name = name.rstrip()
                    temp.append(name)
                    comments.append(temp)
                    # Agilent2 visa address
                    temp = []
                    temp.append('Agilent2 Visa Address:')
                    temp.append(str(self.ui.comboBox_visa_4.currentText()))
                    comments.append(temp)
                    temp = []
                    temp.append('Agilent2 Visa Name:')
                    name = str(self.ui.label_visa_4.text())
                    name = name.rstrip()
                    temp.append(name)
                    comments.append(temp)
                    # Yokogawa3 visa address
                    temp = []
                    temp.append('Yokogawa3 Visa Address:')
                    temp.append(str(self.ui.comboBox_visa_5.currentText()))
                    comments.append(temp)
                    temp = []
                    temp.append('Yokogawa3 Visa Name:')
                    name = str(self.ui.label_visa_5.text())
                    name = name.rstrip()
                    temp.append(name)
                    comments.append(temp)
                    # Agilent3 visa address
                    temp = []
                    temp.append('Agilent3 Visa Address:')
                    temp.append(str(self.ui.comboBox_visa_6.currentText()))
                    comments.append(temp)
                    temp = []
                    temp.append('Agilent3 Visa Name:')
                    name = str(self.ui.label_visa_6.text())
                    name = name.rstrip()
                    temp.append(name)
                    comments.append(temp)
                    # Yokogawa_magnet visa address
                    temp = []
                    temp.append('Yokogawa_magnet Visa Address:')
                    temp.append(str(self.ui.comboBox_visa_7.currentText()))
                    comments.append(temp)
                    temp = []
                    temp.append('Yokogawa_magnet Visa Name:')
                    name = str(self.ui.label_visa_7.text())
                    name = name.rstrip()
                    temp.append(name)
                    comments.append(temp)
                    # Comments
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
                    temp.append(self.input_data[0])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[1])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[2])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[3])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[4])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[5])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[6])
                    comments.append(temp)
                    temp = []
                    temp.append('')
                    comments.append(temp)
                    j = 16 * i - 25
                    temp = []
                    temp.append(self.input_data[j])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 1])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 2])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 3])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 4])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 5])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 6])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 7])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 8])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 9])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 10])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 11])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 12])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 13])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 14])
                    comments.append(temp)
                    temp = []
                    temp.append(self.input_data[j + 15])
                    comments.append(temp)
                    # New line
                    temp = []
                    temp.append('')
                    comments.append(temp)
                    # Lock-in Parameters
                    temp = []
                    temp.append('Magnet field (mT):')
                    temp.append(magnet)
                    comments.append(temp)

                    #####################
                    parameters.append('Date')
                    units.append('String')
                    parameters.append('Time')
                    units.append('s')
                    parameters.append('Step')
                    units.append('1')
                    parameters.append('Current')
                    units.append('Amps')
                    parameters.append('Resistance')
                    units.append('Ohms')
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
        
        

        
