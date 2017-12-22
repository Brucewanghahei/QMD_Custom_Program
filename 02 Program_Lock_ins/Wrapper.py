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
        self.connect(self.ui.pushButton_select_3, SIGNAL('clicked()'), lambda : self.Select("visa3", self.visa3, self.ui.comboBox_visa_3, self.ui.label_visa_3, [self.ui.pushButton_select_3, self.ui.pushButton_close_3]))
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
        
        self.Update("visa1", self.ui.comboBox_visa_1)
        self.Update("visa2", self.ui.comboBox_visa_2)
        self.Update("visa3", self.ui.comboBox_visa_3)
        self.Update("visa4", self.ui.comboBox_visa_4)
        self.Update("visa5", self.ui.comboBox_visa_5)
        
        self.curve_1 = self.make_curveWidgets(self.ui.curvewidget_1, "b", titles = ["Plot 1", "X (x)", "Y (y)"])
        self.curve_2 = self.make_curveWidgets(self.ui.curvewidget_2, "b", titles = ["Plot 2", "X (x)", "Y (y)"])
        self.curve_3 = self.make_curveWidgets(self.ui.curvewidget_3, "b", titles = ["Plot 3", "X (x)", "Y (y)"])
        self.curve_4 = self.make_curveWidgets(self.ui.curvewidget_4, "b", titles = ["Plot 4", "X (x)", "Y (y)"])
        
        self.visa1 = None
        self.visa2 = None
        self.visa3 = None
        self.visa4 = None
        self.visa5 = None
        
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
    
    def Select(self, signal, visa_chosen, comboBoxVisa, lineEditVisa, selectClose):
        visa_address = str(comboBoxVisa.currentText())
        rm = visa.ResourceManager()
        rm.list_resources()
        inst = rm.open_resource(visa_address)
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
                self.Enable(signal)
                self.visa1 = inst
            elif signal == "visa2":
                lineEditVisa.setText(visa_name)
                selectClose[0].setEnabled(False)
                selectClose[1].setEnabled(True)
                self.Enable(signal)
                self.visa2 = inst
            elif signal == "visa3":
                lineEditVisa.setText(visa_name)
                selectClose[0].setEnabled(False)
                selectClose[1].setEnabled(True)
                self.Enable(signal)
                self.visa3 = inst
            elif signal == "visa4":
                lineEditVisa.setText(visa_name)
                selectClose[0].setEnabled(False)
                selectClose[1].setEnabled(True)
                self.Enable(signal)
                self.visa4 = inst
            elif signal == "visa5":
                lineEditVisa.setText(visa_name)
                selectClose[0].setEnabled(False)
                selectClose[1].setEnabled(True)
                self.Enable(signal)
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
            self.Disable(signal)
        elif signal == "visa2":
            visa_chosen.close()
            self.visa2 = None
            self.Disable(signal)
        elif signal == "visa3":
            visa_chosen.close()
            self.visa3 = None
            self.Disable(signal)
        elif signal == "visa4":
            visa_chosen.close()
            self.visa4 = None
            self.Disable(signal)
        elif signal == "visa5":
            visa_chosen.close()
            self.visa5 = None
            self.Disable(signal)
            
    def Check(self, inst):
        try:
            inst.ask("*IDN?")
            valid = True
        except:
            valid = False
        return valid
    
    def make_curveWidgets(self, curvewidget, color, titles):
        curve_temp = make.curve([], [], color = 'b', marker = "o")
        curvewidget.plot.add_item(curve_temp)
        curvewidget.plot.set_antialiasing(True)
        curvewidget.plot.set_titles(titles[0], titles[1], titles[2])
        return curve_temp
    
    def start(self):
        instruments = [self.visa1, self.visa2, self.visa3, self.visa4, self.visa5]
        curves = [self.curve_1, self.curve_2, self.curve_3, self.curve_4]
        curveWidgets =[self.ui.curvewidget_1, self.ui.curvewidget_2, self.ui.curvewidget_3, self.ui.curvewidget_4]
        go_on = None
        self.collect_data_thread.input(self.ui, instruments, curves, curveWidgets, go_on)
                        
    def curvePlots_update(self, curveInfo):
        curveWidget = curveInfo[0]
        curve = curveInfo[1]
        curveWidget.plot.do_autoscale()
        curve.plot().replot()
    
    def Print_data(self, step, time, V1, V2, V3, V4, V5, V6):
        self.ui.label_step.setText(step)
        self.ui.label_time.setText(time)
        self.ui.label_V1.setText(V1)
        self.ui.label_V2.setText(V2)
        self.ui.label_V3.setText(V3)
        self.ui.label_V4.setText(V4)
        self.ui.label_V5.setText(V5)
        self.ui.label_V6.setText(V6)
    
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

    def input(self, ui, instruments, curves, curveWidgets, go_on):
        self.ui = ui
        self.instruments = instruments
        self.curves = curves
        self.curveWidgets = curveWidgets
        self.go_on = go_on
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
        x_value = []
        y_value = []
        date_and_time = []
        self.x_plot = []
        self.y_plot = []
        self.s_value = []
        temp = 0
        start_time = time.time()
        self.Array = []
        while True:
            if self.go_on:
                if self.pause:
                    self.ui.label_condition.setText('Reading paused.')                  
                    self.ui.pushButton_Stop.setEnabled(False)
                    break
                if temp == len(self.Array):
                    self.ui.pushButton_Start.setEnabled(True)
                    self.ui.pushButton_Pause.setEnabled(False)
                    self.ui.pushButton_Stop.setEnabled(False)
                    self.ui.label_condition.setText('Scan complete.')
                    self.ui.tabWidget_save_keithley.setEnabled(True)
                    break
                
                self.ui.label_condition.setText('Reading...')
                
                self.set_voltage(self.Array[temp])
                self.read_data_write()
                self.data = self.read_data_read()
                
                x_value.append(float(self.data[0]))
                self.x_plot = np.array(x_value)
                
                y_value.append(float(self.data[1]))
                self.y_plot = np.array(y_value)
                
                self.s_value.append(temp)
                
                end_time = time.time()
                self.during = end_time - start_time
                self.t_plot.append(self.during)
                
                self.setup_plot(self.curveWidgets[0], self.curves[0], [self.x_plot, self.y_plot], ["Plot 1", "X(x)", "Y(y)"])
                self.setup_plot(self.curveWidgets[1], self.curves[1], [self.x_plot, self.y_plot], ["Plot 2", "X(x)", "Y(y)"])
                self.setup_plot(self.curveWidgets[2], self.curves[2], [self.x_plot, self.y_plot], ["Plot 3", "X(x)", "Y(y)"])
                self.setup_plot(self.curveWidgets[3], self.curves[3], [self.x_plot, self.y_plot], ["Plot 4", "X(x)", "Y(y)"])

                self.emit(SIGNAL("print"), temp, self.during, float(self.data[0]), float(self.data[1]))
                
                now = datetime.datetime.now()
                date = '%s-%s-%s' % (now.year, now.month, now.day)
                current_time = '%s:%s:%s' % (now.hour, now.minute, now.second)
                self.date_and_time = date + ' ' + current_time
                date_value.append(self.date_and_time)
                
                temp += 1
            else:
                self.ui.label_condition.setText('Reading stoped.')
    
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
        
        

        
