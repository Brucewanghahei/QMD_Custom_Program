try:
    import visa
    VISA_MOD_AVAILABLE = True
    rm = visa.ResourceManager()
except:
    VISA_MOD_AVAILABLE = False

import sys

import numpy as np

import time
from datetime import datetime
import os

# Adding navigation toolbar to the figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

from guiqwt.pyplot import *
from guiqwt.plot import CurveWidget
from guiqwt.builder import make

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Sub_Scripts.GUI import Ui_MainWindow

class MyForm(QMainWindow):
    def __init__ (self, parent = None):
        QWidget.__init__(self,parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.update_visas()
        
        self.Device1DataThread = CollectDevice1Data()
        self.Device2DataThread = CollectDevice2Data()
        self.Device3DataThread = CollectDevice3Data()

        self.Device1DataThread.initial_input(self.ui)
        self.Device2DataThread.initial_input(self.ui)
        self.Device3DataThread.initial_input(self.ui)
        #Variables
        self.unique1 = False
        self.unique2 = False
        self.unique3 = False
        
        self.AgilentCheck1 = False
        self.AgilentCheck2 = False
        self.AgilentCheck3 = False
        
        #Commands
        self.connect(self.ui.pushButtonSelectYokogawa_1, SIGNAL('clicked()'), self.Select_Yokogawa_1)
        self.connect(self.ui.pushButtonSelectYokogawa_2, SIGNAL('clicked()'), self.Select_Yokogawa_2)
        self.connect(self.ui.pushButtonSelectYokogawa_3, SIGNAL('clicked()'), self.Select_Yokogawa_3)
        self.connect(self.ui.pushButtonSelectAgilent_1, SIGNAL('clicked()'), self.Select_Agilent_1)
        self.connect(self.ui.pushButtonSelectAgilent_2, SIGNAL('clicked()'), self.Select_Agilent_2)
        self.connect(self.ui.pushButtonSelectAgilent_3, SIGNAL('clicked()'), self.Select_Agilent_3)
        self.connect(self.ui.pushButtonSelectBField_Yokogawa, SIGNAL('clicked()'), self.Select_BField_Yokogawa)
        
        self.connect(self.ui.pushButtonStart, SIGNAL('clicked()'), self.start)
        self.connect(self.ui.pushButtonStop, SIGNAL('clicked()'), self.stop)
        self.connect(self.ui.pushButtonStopDevice1, SIGNAL('clicked()'), self.stopDevice1)
        self.connect(self.ui.pushButtonStopDevice2, SIGNAL('clicked()'), self.stopDevice2)
        self.connect(self.ui.pushButtonStopDevice3, SIGNAL('clicked()'), self.stopDevice3)
        
        self.connect(self.ui.pushButtonBFieldRamp, SIGNAL('clicked()'), self.Ramp_BField)
        
        self.connect(self.Device1DataThread, SIGNAL('Plot1'), self.Plot_Device1)
        self.connect(self.Device2DataThread, SIGNAL('Plot2'), self.Plot_Device2)
        self.connect(self.Device3DataThread, SIGNAL('Plot3'), self.Plot_Device3)
        
        self.connect(self.Device1DataThread, SIGNAL('Device1_Check'), self.Check_Device1)
        self.connect(self.Device2DataThread, SIGNAL('Device2_Check'), self.Check_Device2)
        self.connect(self.Device3DataThread, SIGNAL('Device3_Check'), self.Check_Device3)
        
        self.connect(self.ui.pushButtonBrowse_1, SIGNAL('clicked()'), self.Device1DataThread.browse)
        self.connect(self.ui.pushButtonSelectDirectory_1, SIGNAL('clicked()'), self.Device1DataThread.select_name)
        
        self.connect(self.ui.pushButtonBrowse_2, SIGNAL('clicked()'), self.Device2DataThread.browse)
        self.connect(self.ui.pushButtonSelectDirectory_2, SIGNAL('clicked()'), self.Device2DataThread.select_name)
        
        self.connect(self.ui.pushButtonBrowse_3, SIGNAL('clicked()'), self.Device3DataThread.browse)
        self.connect(self.ui.pushButtonSelectDirectory_3, SIGNAL('clicked()'), self.Device3DataThread.select_name)
        
        self.curve_item_device_1 = make.curve([], [], color='b')
        self.ui.curvewidgetDevice1.plot.add_item(self.curve_item_device_1)
        self.ui.curvewidgetDevice1.plot.set_antialiasing(True)
        
        self.curve_item_device_2 = make.curve([], [], color='b')
        self.ui.curvewidgetDevice2.plot.add_item(self.curve_item_device_2)
        self.ui.curvewidgetDevice2.plot.set_antialiasing(True)
        
        self.curve_item_device_3 = make.curve([], [], color='b')
        self.ui.curvewidgetDevice3.plot.add_item(self.curve_item_device_3)
        self.ui.curvewidgetDevice3.plot.set_antialiasing(True)
        
        # For the canvas.
        self.canvasDevice1 = FigureCanvas(self.ui.mplwidgetDevice1.figure)
        self.canvasDevice1.setParent(self.ui.widgetDevice1)
        self.mpl_toolbar_Device1 = NavigationToolbar(self.canvasDevice1, self.ui.widgetDevice1)
        self.canvasDevice2 = FigureCanvas(self.ui.mplwidgetDevice2.figure)
        self.canvasDevice2.setParent(self.ui.widgetDevice2)
        self.mpl_toolbar_Device2 = NavigationToolbar(self.canvasDevice2, self.ui.widgetDevice2)
        self.canvasDevice3 = FigureCanvas(self.ui.mplwidgetDevice3.figure)
        self.canvasDevice3.setParent(self.ui.widgetDevice3)
        self.mpl_toolbar_Device3 = NavigationToolbar(self.canvasDevice3, self.ui.widgetDevice3)

        
        # Create the QVBoxLayout object and add the widget into the layout
        vbox_Device1 = QVBoxLayout()
        vbox_Device1.addWidget(self.canvasDevice1)
        vbox_Device1.addWidget(self.mpl_toolbar_Device1)
        self.ui.widgetDevice1.setLayout(vbox_Device1)
        
        vbox_Device2 = QVBoxLayout()
        vbox_Device2.addWidget(self.canvasDevice2)
        vbox_Device2.addWidget(self.mpl_toolbar_Device2)
        self.ui.widgetDevice2.setLayout(vbox_Device2)
        
        vbox_Device3 = QVBoxLayout()
        vbox_Device3.addWidget(self.canvasDevice3)
        vbox_Device3.addWidget(self.mpl_toolbar_Device3)
        self.ui.widgetDevice3.setLayout(vbox_Device3)
  
        # Connect the mplwidget with canvas
        self.ui.mplwidgetDevice1 = self.canvasDevice1
        self.ui.mplwidgetDevice2 = self.canvasDevice2
        self.ui.mplwidgetDevice3 = self.canvasDevice3

        self.BField_increase = 0
        self.BField_Array = np.array([], dtype = float)
        self.Coil_Constant = 1E-3/9.1E-3
        self.downward_step = False
        
    def update_visas(self):
        self.rm = visa.ResourceManager()
        visas = self.rm.list_resources()
        
        self.ui.comboBoxYokogawa_1.clear()
        self.ui.comboBoxAgilent_1.clear()
        self.ui.comboBoxYokogawa_2.clear()
        self.ui.comboBoxAgilent_2.clear()
        self.ui.comboBoxYokogawa_3.clear()
        self.ui.comboBoxAgilent_3.clear()
        self.ui.comboBox_BField_Yokogawa.clear()
        
        for i in visas:
            self.ui.comboBoxYokogawa_1.addItem(i)
            self.ui.comboBoxAgilent_1.addItem(i)
            self.ui.comboBoxYokogawa_2.addItem(i)
            self.ui.comboBoxAgilent_2.addItem(i)
            self.ui.comboBoxYokogawa_3.addItem(i)
            self.ui.comboBoxAgilent_3.addItem(i)
            self.ui.comboBox_BField_Yokogawa.addItem(i)
            
    def Select_Yokogawa_1(self):
        temp = str(self.ui.comboBoxYokogawa_1.currentText())
        self.Yokogawa_1 = self.rm.open_resource(temp)
        if self.unique2 == True and self.unique3 == True:
            if temp == str(self.ui.comboBoxYokogawa_2.currentText()) and temp == str(self.ui.comboBoxYokogawa_3.currentText()):
                self.ui.lineEditStatus_1.setText("Error: The selected visa is the same as Yokogawa 2 and 3 ")
            else:
                try:
                    self.Yokogawa_1.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                    
                if valid == True:
                    self.ui.label_Yokogawa_1.setText(str(self.Yokogawa_1.ask('*IDN?')))
                    self.ui.lineEditStatus_1.setText("Yokogawa 1 has been selected")
                else:
                    self.ui.lineEditStatus_1.setText("There is an issue with selected Yokogawa 1")
        elif self.unique2 == True or self.unique3 == True:
            if temp == str(self.ui.comboBoxYokogawa_2.currentText()):
                self.ui.lineEditStatus_1.setText("Error: The selected visas is the same as Yokogawa 2")
            elif temp == str(self.ui.comboBoxYokogawa_3.currentText()):
                self.ui.lineEditStatus_1.setText("Error: The select visas is the same as Yokogawa 3")
            else:
                try:
                    self.Yokogawa_1.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                if valid == True:
                    self.ui.label_Yokogawa_1.setText(str(self.Yokogawa_1.ask('*IDN?')))
                    self.ui.lineEditStatus_1.setText("Yokogawa 1 has been selected")
                    self.unique1 = True
                else:
                    self.ui.lineEditStatus_1.setText("There is an issue with selected Yokogawa 1")
        else:
            self.ui.label_Yokogawa_1.setText(str(self.Yokogawa_1.ask('*IDN?')))
            self.ui.lineEditStatus_1.setText("Yokogawa 1 has been selected")
            self.unique1 = True
            
    def Select_Yokogawa_2(self):
        temp = str(self.ui.comboBoxYokogawa_2.currentText())
        self.Yokogawa_2 = self.rm.open_resource(temp)
        if self.unique1 == True and self.unique3 == True:
            if temp == str(self.ui.comboBoxYokogawa_1.currentText()) and temp == str(self.ui.comboBoxYokogawa_3.currentText()):
                self.ui.lineEditStatus_2.setText("Error: The selected visa is the same as Yokogawa 1 and 3 ")
            else:
                try:
                    self.Yokogawa_2.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                    
                if valid == True:
                    self.ui.label_Yokogawa_2.setText(str(self.Yokogawa_2.ask('*IDN?')))
                    self.ui.lineEditStatus_2.setText("Yokogawa 2 has been selected")
                else:
                    self.ui.lineEditStatus_2.setText("There is an issue with selected Yokogawa 2")
        elif self.unique1 == True or self.unique3 == True:
            if temp == str(self.ui.comboBoxYokogawa_1.currentText()):
                self.ui.lineEditStatus_2.setText("Error: The selected visas is the same as Yokogawa 1")
            elif temp == str(self.ui.comboBoxYokogawa_3.currentText()):
                self.ui.lineEditStatus_2.setText("Error: The select visas is the same as Yokogawa 3")
            else:
                try:
                    self.Yokogawa_2.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                if valid == True:
                    self.ui.label_Yokogawa_2.setText(str(self.Yokogawa_2.ask('*IDN?')))
                    self.ui.lineEditStatus_2.setText("Yokogawa 2 has been selected")
                    self.unique2 = True
                else:
                    self.ui.lineEditStatus_2.setText("There is an issue with selected Yokogawa 2")
        else:
            self.ui.label_Yokogawa_2.setText(str(self.Yokogawa_2.ask('*IDN?')))
            self.ui.lineEditStatus_2.setText("Yokogawa 2 has been selected")
            self.unique2 = True
            
    def Select_Yokogawa_3(self):
        temp = str(self.ui.comboBoxYokogawa_3.currentText())
        self.Yokogawa_3 = self.rm.open_resource(temp)
        if self.unique1 == True and self.unique2 == True:
            if temp == str(self.ui.comboBoxYokogawa_1.currentText()) and temp == str(self.ui.comboBoxYokogawa_2.currentText()):
                self.ui.lineEditStatus_3.setText("Error: The selected visa is the same as Yokogawa 1 and 2")
            else:
                try:
                    self.Yokogawa_3.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                    
                if valid == True:
                    self.ui.label_Yokogawa_3.setText(str(self.Yokogawa_3.ask('*IDN?')))
                    self.ui.lineEditStatus_3.setText("Yokogawa 3 has been selected")
                else:
                    self.ui.lineEditStatus_3.setText("There is an issue with selected Yokogawa 3")
        elif self.unique1 == True or self.unique2 == True:
            if temp == str(self.ui.comboBoxYokogawa_1.currentText()):
                self.ui.lineEditStatus_3.setText("Error: The selected visas is the same as Yokogawa 1")
            elif temp == str(self.ui.comboBoxYokogawa_2.currentText()):
                self.ui.lineEditStatus_3.setText("Error: The select visas is the same as Yokogawa 2")
            else:
                try:
                    self.Yokogawa_3.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                if valid == True:
                    self.ui.label_Yokogawa_3.setText(str(self.Yokogawa_3.ask('*IDN?')))
                    self.ui.lineEditStatus_3.setText("Yokogawa 3 has been selected")
                    self.unique3 = True
                else:
                    self.ui.lineEditStatus_3.setText("There is an issue with selected Yokogawa 3")
        else:
            self.ui.label_Yokogawa_3.setText(str(self.Yokogawa_3.ask('*IDN?')))
            self.ui.lineEditStatus_3.setText("Yokogawa 3 has been selected")
            self.unique3 = True
            
    def Select_Agilent_1(self):
        temp = str(self.ui.comboBoxAgilent_1.currentText())
        self.Agilent_1 = self.rm.open_resource(temp)
        if self.AgilentCheck2 == True and self.AgilentCheck3 == True:
            if temp == str(self.ui.comboBoxAgilent_2.currentText()) and temp == str(self.ui.comboBoxAgilent_3.currentText()):
                self.ui.lineEditStatus_1.setText("Error: The selected visa is the same as Agilent 2 and 3")
            else:
                try:
                    self.Agilent_1.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                    
                if valid == True:
                    self.ui.label_Agilent_1.setText(str(self.Agilent_1.ask('*IDN?')))
                    self.ui.lineEditStatus_1.setText("Agilent 1 has been selected")
                else:
                    self.ui.lineEditStatus_1.setText("There is an issue with the Agilent selected")             
        elif self.AgilentCheck2 == True or self.AgilentCheck3 == True:
            if temp == str(self.ui.comboBoxAgilent_2.currentText()):
                self.ui.lineEditStatus_1.setText("The selected agilent is the same as the one for agilent 2")
            elif temp == str(self.ui.comboBoxAgilent_3.currentText()):
                self.ui.lineEditStatus_1.setText("The selected agilent is the same as the one for agilent 3")
            else:
                try:
                    self.Agilent_1.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                    
                if valid == True:
                    self.ui.label_Agilent_1.setText(str(self.Agilent_1.ask('*IDN?')))
                    self.ui.lineEditStatus_1.setText("Agilent 1 has been selected")
                    self.AgilentCheck1 = True
                else:
                    self.ui.lineEditStatus_1.setText("There is an error with the selected agilent")
        else:
            self.ui.label_Agilent_1.setText(str(self.Agilent_1.ask('*IDN?')))
            self.ui.lineEditStatus_1.setText('Agilent 1 has been selected')
            self.AgilentCheck1 = True

    def Select_Agilent_2(self):
        temp = str(self.ui.comboBoxAgilent_2.currentText())
        self.Agilent_2 = self.rm.open_resource(temp)
        if self.AgilentCheck1 == True and self.AgilentCheck3 == True:
            if temp == str(self.ui.comboBoxAgilent_1.currentText()) and temp == str(self.ui.comboBoxAgilent_3.currentText()):
                self.ui.lineEditStatus_2.setText("Error: The selected visa is the same as Agilent 1 and 3")
            else:
                try:
                    self.Agilent_2.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                    
                if valid == True:
                    self.ui.label_Agilent_2.setText(str(self.Agilent_2.ask('*IDN?')))
                    self.ui.lineEditStatus_2.setText("Agilent 2 has been selected")
                else:
                    self.ui.lineEditStatus_2.setText("There is an issue with the Agilent selected")             
        elif self.AgilentCheck1 == True or self.AgilentCheck3 == True:
            if temp == str(self.ui.comboBoxAgilent_1.currentText()):
                self.ui.lineEditStatus_2.setText("The selected agilent is the same as the one for agilent 1")
            elif temp == str(self.ui.comboBoxAgilent_3.currentText()):
                self.ui.lineEditStatus_2.setText("The selected agilent is the same as the one for agilent 3")
            else:
                try:
                    self.Agilent_2.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                    
                if valid == True:
                    self.ui.label_Agilent_2.setText(str(self.Agilent_2.ask('*IDN?')))
                    self.ui.lineEditStatus_2.setText("Agilent 2 has been selected")
                    self.AgilentCheck2 = True
                else:
                    self.ui.lineEditStatus_2.setText("There is an error with the selected agilent")
        else:
            self.ui.label_Agilent_2.setText(str(self.Agilent_2.ask('*IDN?')))
            self.ui.lineEditStatus_2.setText('Agilent 2 has been selected')
            self.AgilentCheck2 = True
            
    def Select_Agilent_3(self):
        temp = str(self.ui.comboBoxAgilent_3.currentText())
        self.Agilent_3 = self.rm.open_resource(temp)
        if self.AgilentCheck1 == True and self.AgilentCheck2 == True:
            if temp == str(self.ui.comboBoxAgilent_1.currentText()) and temp == str(self.ui.comboBoxAgilent_2.currentText()):
                self.ui.lineEditStatus_3.setText("Error: The selected visa is the same as Agilent 1 and 2")
            else:
                try:
                    self.Agilent_3.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                    
                if valid == True:
                    self.ui.label_Agilent_3.setText(str(self.Agilent_3.ask('*IDN?')))
                    self.ui.lineEditStatus_3.setText("Agilent 3 has been selected")
                else:
                    self.ui.lineEditStatus_3.setText("There is an issue with the Agilent selected")             
        elif self.AgilentCheck1 == True or self.AgilentCheck2 == True:
            if temp == str(self.ui.comboBoxAgilent_1.currentText()):
                self.ui.lineEditStatus_3.setText("The selected agilent is the same as the one for agilent 1")
            elif temp == str(self.ui.comboBoxAgilent_2.currentText()):
                self.ui.lineEditStatus_3.setText("The selected agilent is the same as the one for agilent 2")
            else:
                try:
                    self.Agilent_3.ask('*IDN?')
                    valid = True
                except:
                    valid = False
                    
                if valid == True:
                    self.ui.label_Agilent_3.setText(str(self.Agilent_3.ask('*IDN?')))
                    self.ui.lineEditStatus_3.setText("Agilent 3 has been selected")
                    self.AgilentCheck3 = True
                else:
                    self.ui.lineEditStatus_3.setText("There is an error with the selected agilent")
        else:
            self.ui.label_Agilent_3.setText(str(self.Agilent_3.ask('*IDN?')))
            self.ui.lineEditStatus_3.setText('Agilent 3 has been selected')
            self.AgilentCheck3 = True
            
    def Select_BField_Yokogawa(self):
        temp = str(self.ui.comboBox_BField_Yokogawa.currentText())
        self.BField_Yokogawa = rm.open_resource(temp)
        self.ui.label_BField_Yokogawa.setText(str(self.BField_Yokogawa.ask('*IDN?')))
        self.BField_Yokogawa.write('SOUR:FUNC CURR')
        
    def Ramp_BField(self):
        Temp = (float(self.ui.lineEditBFieldRamp_Final.text())-float(self.ui.lineEditBFieldRamp_Initial.text()))/float(self.ui.lineEditBFieldRamp_Steps.text())
        Temp2 = np.array([], dtype = float)
        for i in range(0, int(Temp)+1):
            Temp2 = np.append(Temp2, float(self.ui.lineEditBFieldRamp_Initial.text()) + float(self.ui.lineEditBFieldRamp_Steps.text())*i)
        Temp2 = Temp2*1E-03
        for i in range(0,len(Temp2)):
            if Temp2[i] > 200E-03 or Temp2[i] < -200E-03:
                break
            else:
                pass
            self.BField_Yokogawa.write('OUTP ON')
            self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(Temp2[i]))
            time.sleep(float(self.ui.lineEditBFieldRamp_Timestep.text()))
            
    def start(self):
        #Array that determines what BField will be swept
        
        self.timestep = float(self.ui.lineEditTimestep.text())
        self.timedelay = float(self.ui.lineEditTimeDelay.text())
        self.start_check = True
        self.BField_Array = np.array([], dtype = float)
        
        if self.ui.radioButtonOne.isChecked():
            if self.ui.radioButton_nV_1.isChecked():
                self.LockIn_Sens1 = float(self.ui.lineEditLockInSens_1.text())*1E-09
            elif self.ui.radioButton_uV_1.isChecked():
                self.LockIn_Sens1 = float(self.ui.lineEditLockInSens_1.text())*1E-06
            elif self.ui.radioButton_mV_1.isChecked():
                self.LockIn_Sens1 = float(self.ui.lineEditLockInSens_1.text())*1E-03
            else:
                self.ui.lineEditStatus_1.setText("Please choose a unit for the lock in sens")      
                self.start_check = False
                
            self.PreAmp1 = float(self.ui.lineEditPreAmp_1.text())
            self.OutVoltage1 = float(self.ui.lineEditOutputVoltage_1.text())
            
            if self.ui.radioButtonMOhms_1.isChecked():
                self.Resistor1 = float(self.ui.lineEditResistor_1.text())*1E06
            elif self.ui.radioButtonGOhms_1.isChecked():
                self.Resistor1 = float(self.ui.lineEditResistor_1.text())*1E09
            else:
                self.ui.lineEditStatus_1.setText('Please choose a unit for the resistor')
                self.start_check = False
                
        elif self.ui.radioButtonTwo.isChecked():
            
            if self.ui.radioButton_nV_1.isChecked():
                self.LockIn_Sens1 = float(self.ui.lineEditLockInSens_1.text())*1E-09
            elif self.ui.radioButton_uV_1.isChecked():
                self.LockIn_Sens1 = float(self.ui.lineEditLockInSens_1.text())*1E-06
            elif self.ui.radioButton_mV_1.isChecked():
                self.LockIn_Sens1 = float(self.ui.lineEditLockInSens_1.text())*1E-03
            else:
                self.ui.lineEditStatus_1.setText("Please choose a unit for the lock in sens")
                self.start_check = False
                
            if self.ui.radioButton_nV_2.isChecked():
                self.LockIn_Sens2 = float(self.ui.lineEditLockInSens_2.text())*1E-09
            elif self.ui.radioButton_uV_2.isChecked():
                self.LockIn_Sens2 = float(self.ui.lineEditLockInSens_2.text())*1E-06
            elif self.ui.radioButton_mV_2.isChecked():
                self.LockIn_Sens2 = float(self.ui.lineEditLockInSens_2.text())*1E-03
            else:
                self.ui.lineEditStatus_2.setText("Please choose a unit for the lock in sens")
                self.start_check = False
            
            self.PreAmp1 = float(self.ui.lineEditPreAmp_1.text())
            self.PreAmp2 = float(self.ui.lineEditPreAmp_2.text())
            
            self.OutVoltage1 = float(self.ui.lineEditOutputVoltage_1.text())
            self.OutVoltage2 = float(self.ui.lineEditOutputVoltage_2.text())
            
            if self.ui.radioButtonMOhms_1.isChecked():
                self.Resistor1 = float(self.ui.lineEditResistor_1.text())*1E06
            elif self.ui.radioButtonGOhms_1.isChecked():
                self.Resistor1 = float(self.ui.lineEditResistor_1.text())*1E09
            else:
                self.ui.lineEditStatus_1.setText('Please choose a unit for the resistor')
                self.start_check = False
        
            if self.ui.radioButtonMOhms_2.isChecked():
                self.Resistor2 = float(self.ui.lineEditResistor_2.text())*1E06
            elif self.ui.radioButtonGOhms_3.isChecked():
                self.Resistor2= float(self.ui.lineEditResistor_2.text())*1E09
            else:
                self.ui.lineEditStatus_2.setText('Please choose a unit for the resistor')
                self.start_check = False
                
        else:
            if self.ui.radioButton_nV_1.isChecked():
                self.LockIn_Sens1 = float(self.ui.lineEditLockInSens_1.text())*1E-09
            elif self.ui.radioButton_uV_1.isChecked():
                self.LockIn_Sens1 = float(self.ui.lineEditLockInSens_1.text())*1E-06
            elif self.ui.radioButton_mV_1.isChecked():
                self.LockIn_Sens1 = float(self.ui.lineEditLockInSens_1.text())*1E-03
            else:
                self.ui.lineEditStatus_1.setText("Please choose a unit for the lock in sens")
                self.start_check = False
                
            if self.ui.radioButton_nV_2.isChecked():
                self.LockIn_Sens2 = float(self.ui.lineEditLockInSens_2.text())*1E-09
            elif self.ui.radioButton_uV_2.isChecked():
                self.LockIn_Sens2 = float(self.ui.lineEditLockInSens_2.text())*1E-06
            elif self.ui.radioButton_mV_2.isChecked():
                self.LockIn_Sens2 = float(self.ui.lineEditLockInSens_2.text())*1E-03
            else:
                self.ui.lineEditStatus_2.setText("Please choose a unit for the lock in sens")
                self.start_check = False
            
            if self.ui.radioButton_nV_3.isChecked():
                self.LockIn_Sens3 = float(self.ui.lineEditLockInSens_3.text())*1E-09
            elif self.ui.radioButton_uV_3.isChecked():
                self.LockIn_Sens3 = float(self.ui.lineEditLockInSens_3.text())*1E-06
            elif self.ui.radioButton_mV_3.isChecked():
                self.LockIn_Sens3 = float(self.ui.lineEditLockInSens_3.text())*1E-03
            else:
                self.ui.lineEditStatus_3.setText("Please choose a unit for the lock in sens")
                self.start_check = False
            
            self.PreAmp1 = float(self.ui.lineEditPreAmp_1.text())
            self.PreAmp2 = float(self.ui.lineEditPreAmp_2.text())
            self.PreAmp3 = float(self.ui.lineEditPreAmp_3.text())
            
            self.OutVoltage1 = float(self.ui.lineEditOutputVoltage_1.text())
            self.OutVoltage2 = float(self.ui.lineEditOutputVoltage_2.text())
            self.OutVoltage3 = float(self.ui.lineEditOutputVoltage_3.text())
            
            if self.ui.radioButtonMOhms_1.isChecked():
                self.Resistor1 = float(self.ui.lineEditResistor_1.text())*1E06
            elif self.ui.radioButtonGOhms_1.isChecked():
                self.Resistor1 = float(self.ui.lineEditResistor_1.text())*1E09
            else:
                self.ui.lineEditStatus_1.setText('Please choose a unit for the resistor')
                self.start_check = False
        
            if self.ui.radioButtonMOhms_2.isChecked():
                self.Resistor2 = float(self.ui.lineEditResistor_2.text())*1E06
            elif self.ui.radioButtonGOhms_3.isChecked():
                self.Resistor2= float(self.ui.lineEditResistor_2.text())*1E09
            else:
                self.ui.lineEditStatus_2.setText('Please choose a unit for the resistor')
                self.start_check = False
                
            if self.ui.radioButtonMOhms_3.isChecked():
                self.Resistor3 = float(self.ui.lineEditResistor_3.text())*1E06
            elif self.ui.radioButtonGOhms_3.isChecked():
                self.Resistor3 = float(self.ui.lineEditResistor_3.text())*1E09
            else:
                self.ui.lineEditStatus_3.setText('Please choose a unit for the resistor')
                self.start_check = False
            
        if self.ui.radioButtonOne.isChecked():
            self.Device1DataThread.input(self.ui, self.curve_item_device_1, self.timestep, self.timedelay, self.LockIn_Sens1, self.PreAmp1, self.OutVoltage1, self.Resistor1, self.Yokogawa_1, self.Agilent_1)
        elif self.ui.radioButtonTwo.isChecked():
            self.Device1DataThread.input(self.ui, self.curve_item_device_1, self.timestep, self.timedelay, self.LockIn_Sens1, self.PreAmp1, self.OutVoltage1, self.Resistor1, self.Yokogawa_1, self.Agilent_1)
            self.Device2DataThread.input(self.ui, self.curve_item_device_2, self.timestep, self.timedelay, self.LockIn_Sens2, self.PreAmp2, self.OutVoltage2, self.Resistor2, self.Yokogawa_2, self.Agilent_2) 
        elif self.start_check == True:
            self.Device1DataThread.input(self.ui, self.curve_item_device_1, self.timestep, self.timedelay, self.LockIn_Sens1, self.PreAmp1, self.OutVoltage1, self.Resistor1, self.Yokogawa_1, self.Agilent_1)
            self.Device2DataThread.input(self.ui, self.curve_item_device_2, self.timestep, self.timedelay, self.LockIn_Sens2, self.PreAmp2, self.OutVoltage2, self.Resistor2, self.Yokogawa_2, self.Agilent_2)
            self.Device3DataThread.input(self.ui, self.curve_item_device_3, self.timestep, self.timedelay, self.LockIn_Sens3, self.PreAmp3, self.OutVoltage3, self.Resistor3, self.Yokogawa_3, self.Agilent_3)

        else:
            pass
        
        Temp = (float(self.ui.lineEditBField_Sweep_Final.text())-float(self.ui.lineEditBField_Sweep_Initial.text()))/float(self.ui.lineEditBFieldSweep_Steps.text())
        for i in range(0, int(Temp)+1):
            self.BField_Array = np.append(self.BField_Array, float(self.ui.lineEditBField_Sweep_Initial.text())+ i*float(self.ui.lineEditBFieldSweep_Steps.text()))
            
        self.BField_Array = self.BField_Array*1E-03

        self.BField_Yokogawa.write('OUTP ON')
        self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase]))
        self.BField_Strength = self.BField_Array[self.BField_increase]*self.Coil_Constant
        self.ui.label_BField_Value.setText(str(round(self.BField_Strength*1000,2)) + ' ' + 'mT')

    def Check_Device1(self, Check, Current1, Resistance1):
        self.Device1DataThread.Device1Pause = True
        self.Check1 = Check
        self.Current1 = Current1
        self.Resistance1 = Resistance1
        self.ui.mplwidgetDevice1.figure.clear()
        self.analysis_Device1 = self.ui.mplwidgetDevice1.figure.add_subplot(111)
        self.analysis_Device1.grid()
        self.analysis_Device1.set_title('Resistance v. Current')
        self.analysis_Device1.set_xlabel('Current (A)')
        self.analysis_Device1.set_ylabel('Resistance (Ohms)')
        self.analysis_Device1.plot(self.Current1, self.Resistance1, marker = '.', linestyle = '-')
        self.ui.mplwidgetDevice1.draw()
        self.Change_BField()
        
    def Check_Device2(self, Check, Current2, Resistance2):
        self.Device2DataThread.Device2Pause = True
        self.Check2 = Check
        self.Current2 = Current2
        self.Resistance2 = Resistance2
        self.ui.mplwidgetDevice2.figure.clear()
        self.analysis_Device2 = self.ui.mplwidgetDevice2.figure.add_subplot(111)
        self.analysis_Device2.grid()
        self.analysis_Device2.set_title('Resistance v. Current')
        self.analysis_Device2.set_xlabel('Current (A)')
        self.analysis_Device2.set_ylabel('Resistance (Ohms)')
        self.analysis_Device2.plot(self.Current2, self.Resistance2, marker = '.', linestyle = '-')
        self.ui.mplwidgetDevice2.draw()
        self.Change_BField()
        
    def Check_Device3(self, Check, Current3, Resistance3):
        self.Device3DataThread.Device3Pause = True
        self.Check3 = Check
        self.Current3 = Current3
        self.Resistance3 = Resistance3
        self.analysis_Device3 = self.ui.mplwidgetDevice3.figure.add_subplot(111)
        self.analysis_Device3.grid()
        self.analysis_Device3.set_title('Resistance v. Current')
        self.analysis_Device3.set_xlabel('Current (A)')
        self.analysis_Device3.set_ylabel('Resistance (Ohms)')
        self.analysis_Device3.plot(self.Current3, self.Resistance3, marker = '.', linestyle = '-')
        self.ui.mplwidgetDevice3.draw()
        self.Change_BField()
        
    def Change_BField(self):
        if self.ui.radioButtonOne.isChecked():
            if self.Check1 == True:
                if self.BField_Array[self.BField_increase] > 200E-03 or self.BField_Array[self.BField_increase] < -200E-03:
                    self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase]))
                else:
                    pass
                
                if self.BField_increase < len(self.BField_Array)-1 and self.downward_step == False:
                    self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase+1]))
                    self.BField_Strength = self.BField_Array[self.BField_increase+1]*self.Coil_Constant
                    self.BField_increase += 1
                # elif self.BField_increase == len(self.BField_Array)-1:
                #     self.BField_increase = self.BField_increase - 1
                #     self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase+1]))
                #     self.BField_Strength = self.BField_Array[self.BField_increase+1]*self.Coil_Constant
                #     self.downward_step = True
                    self.ui.label_BField_Value.setText(str(self.BField_Strength*1000) + ' ' + 'mT')
                    time.sleep(1.5)
                    self.Device1DataThread.f_name = self.Device1DataThread.directory + '\\' + self.Device1DataThread.File_Name + ' ' + 'B_Field ' + str(round(self.BField_Strength*1000,2)) + ' ' + 'mT' + 'Sweep ' + str(self.Device1DataThread.Save_Index) + self.Device1DataThread.type
                    self.Device1DataThread.Device1Pause = False
                    self.Check1 = False
                else:
                    self.stop()
                # 
                # if self.downward_step == True and self.BField_increase > 0:
                #     self.BField_increase = self.BField.increase - 1
                #     self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase+1]))
                #     self.BField_Strength = self.BField_Array[self.BField_increase+1]*self.Coil_Constant
                # elif self.BField_increase == 0:
                #     self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase]))
                #     self.BField_Strength = self.BField_Array[self.BField_increase]*self.Coil_Constant
                #     self.downward_step = False
                # else:
                #     pass
                # self.ui.label_BField_Value.setText(str(self.BField_Strength) + ' ' + 'T')
                # time.sleep(1)
                # self.Device1DataThread.f_name = self.Device1DataThread.File_Name + ' ' + 'Sweep ' + str(self.Device1DataThread.Save_Index) + 'B_Field ' + str(self.BField_Strength) + self.Device1DataThread.type
                # self.Device1DataThread.Device1Pause = False
                # self.Check1 = False
            else:
                pass
        elif self.ui.radioButtonTwo.isChecked():
            if self.Check1 and self.Check2 == True:
                
                if self.BField_Array[self.BField_increase] > 200E-03 or self.BField_Array[self.BField_increase] < -200E-03:
                    self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase]))
                else:
                    pass
                
                if self.BField_increase < len(self.BField_Array)-1 and self.downward_step == False:
                    self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase+1]))
                    self.BField_Strength = self.BField_Array[self.BField_increase+1]*self.Coil_Constant
                    self.BField_increase += 1
                # elif self.BField_increase == len(self.BField_Array)-1:
                #     self.BField_increase = self.BField_increase - 1
                #     self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase+1]))
                #     self.BField_Strength = self.BField_Array[self.BField_increase+1]*self.Coil_Constant
                #     self.downward_step = True
                    self.ui.label_BField_Value.setText(str(self.BField_Strength*1000) + ' ' + 'mT')
                    time.sleep(1.5)
                    self.Device1DataThread.f_name = self.Device1DataThread.directory + '\\' + self.Device1DataThread.File_Name + ' ' + 'B_Field ' + str(round(self.BField_Strength*1000,2)) + ' ' + 'mT'  + 'Sweep ' + str(self.Device1DataThread.Save_Index) + self.Device1DataThread.type
                    self.Device2DataThread.f_name = self.Device2DataThread.directory + '\\' + self.Device2DataThread.File_Name + ' ' + 'B_Field ' + str(round(self.BField_Strength*1000,2)) + ' ' + 'mT' +'Sweep ' + str(self.Device2DataThread.Save_Index) + self.Device2DataThread.type
                    #self.Device1DataThread.f_name = self.Device1DataThread.directory + '\\' + self.Device1DataThread.File_Name + ' ' + self.Device1DataThread.date + ' ' + 'B_Field ' + str(round(self.BField_Strength*1000,2)) + ' ' + 'mT' + self.Device1DataThread.type
                    #self.Device2DataThread.f_name = self.Device2DataThread.directory + '\\' + self.Device2DataThread.File_Name + ' ' + self.Device2DataThread.date + ' ' + 'B_Field ' + str(round(self.BField_Strength*1000,2)) + ' ' + 'mT' + self.Device2DataThread.type
                    #self.Device1DataThread.f_name = self.Device1DataThread.File_Name + ' ' + 'Sweep ' + str(self.Device1DataThread.Save_Index) + ' ' + 'B_Field ' + str(self.BField_Strength) + self.Device1DataThread.type
                    #self.Device2DataThread.f_name = self.Device2DataThread.File_Name + ' ' + 'Sweep ' + str(self.Device2DataThread.Save_Index) + ' ' + 'B_Field ' + str(self.BField_Strength) + self.Device2DataThread.type
                    self.Device1DataThread.Device1Pause = False
                    self.Device2DataThread.Device2Pause = False
                    self.Check1 = False
                    self.Check2 = False
                else:
                    self.stop()
                    pass
                
                # if self.downward_step == True and self.BField_increase > 0:
                #     self.BField_increase = self.BField_increase - 1
                #     self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase+1]))
                #     self.BField_Strength = self.BField_Array[self.BField_increase+1]*self.Coil_Constant
                # elif self.BField_increase == 0:
                #     self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase]))
                #     self.BField_Strength = self.BField_Array[self.BField_increase]*self.Coil_Constant
                #     self.downward_step = False
                # else:
                #     pass
                # self.ui.label_BField_Value.setText(str(self.BField_Strength) + ' ' + 'T')
                # time.sleep(1)
                # self.Device1DataThread.f_name = self.Device1DataThread.File_Name + ' ' + 'Sweep ' + str(self.Device1DataThread.Save_Index) + ' ' + 'B_Field ' + str(self.BField_Strength) + self.Device1DataThread.type
                # self.Device2DataThread.f_name = self.Device2DataThread.File_Name + ' ' + 'Sweep ' + str(self.Device2DataThread.Save_Index) + ' ' + 'B_Field ' + str(self.BField_Strength) + self.Device2DataThread.type
                # self.Device1DataThread.Device1Pause = False
                # self.Device2DataThread.Device2Pause = False
                # self.Check1 = False
                # self.Check2 = False
            else:
                pass
        else: 
            if self.Check1 == True and self.Check2 == True and self.Check3 == True:
                
                if self.BField_Array[self.BField_increase] > 200E-03 or self.BField_Array[self.BField_increase] < -200E-03:
                    self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase]))
                else:
                    pass
                if self.BField_increase < len(self.BField_Array)-1 and self.downward_step == False:
                    self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase+1]))
                    self.BField_Strength = self.BField_Array[self.BField_increase+1]*self.Coil_Constant
                    self.BField_increase += 1
                # elif self.BField_increase == len(self.BField_Array)-1:
                #     self.BField_increase = self.BField_increase - 1
                #     self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase+1]))
                #     self.BField_Strength = self.BField_Array[self.BField_increase+1]*self.Coil_Constant
                #     self.downward_step = True
                    self.ui.label_BField_Value.setText(str(self.BField_Strength*1000) + ' ' + 'mT')
                    time.sleep(1.5)
                    self.Device1DataThread.f_name = self.Device1DataThread.directory + '\\' + self.Device1DataThread.File_Name + ' ' + 'B_Field ' + str(round(self.BField_Strength*1000,2)) + ' ' + 'mT' + 'Sweep ' + str(self.Device1DataThread.Save_Index) + self.Device1DataThread.type
                    self.Device2DataThread.f_name = self.Device2DataThread.directory + '\\' + self.Device2DataThread.File_Name + ' ' + 'B_Field ' + str(round(self.BField_Strength*1000,2)) + ' ' + 'mT' +'Sweep ' + str(self.Device2DataThread.Save_Index) + self.Device2DataThread.type
                    self.Device3DataThread.f_name = self.Device3DataThread.directory + '\\' + self.Device3DataThread.File_Name + ' ' + 'B_Field ' + str(round(self.BField_Strength*1000,2)) + ' ' + 'mT' + 'Sweep ' + str(self.Device3DataThread.Save_Index) + self.Device3DataThread.type
                    self.Device1DataThread.Device1Pause = False
                    self.Device2DataThread.Device2Pause = False
                    self.Device3DataThread.Device3Pause = False
                    self.Check1 = False
                    self.Check2 = False
                    self.Check3 = False
                else:
                    self.stop()
                
                # if self.downward_step == True and self.BField_increase > 0:
                #     self.BField_increase = self.BField.increase - 1
                #     self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase+1]))
                #     self.BField_Strength = self.BField_Array[self.BField_increase+1]*self.Coil_Constant
                # elif self.BField_increase == 0:
                #     self.BField_Yokogawa.write('SOUR:LEV:AUTO ' + str(self.BField_Array[self.BField_increase]))
                #     self.BField_Strength = self.BField_Array[self.BField_increase]*self.Coil_Constant
                #     self.downward_step = False
                # else:
                #     pass
                # self.ui.label_BField_Value.setText(str(self.BField_Strength) + ' ' + 'T')
                # time.sleep(1)
                # self.Device1DataThread.f_name = self.Device1DataThread.File_Name + ' ' + 'Sweep ' + str(self.Device1DataThread.Save_Index) + 'B_Field ' + str(self.BField_Strength) + self.Device1DataThread.type
                # self.Device2DataThread.f_name = self.Device2DataThread.File_Name + ' ' + 'Sweep ' + str(self.Device2DataThread.Save_Index) + 'B_Field ' + str(self.BField_Strength) + self.Device2DataThread.type
                # self.Device3DataThread.f_name = self.Device3DataThread.File_Name + ' ' + 'Sweep ' + str(self.Device3DataThread.Save_Index) + 'B_Field ' + str(self.BField_Strength) + self.Device3DataThread.type
                # self.Device1DataThread.Device1Pause = False
                # self.Device2DataThread.Device2Pause = False
                # self.Device3DataThread.Device3Pause = False
                # self.Check1 = False
                # self.Check2 = False
                # self.Check3 = False
            else:
                pass
            
    def stop(self):
        #self.BField_Yokogawa.write('OUTP OFF')
        if self.ui.radioButtonOne.isChecked():             
            self.Device1DataThread.stop_check = True
            self.Device1DataThread.break_check = True
            self.Device1DataThread.Device1Pause = True
            self.Device1DataThread.quit()
            self.ui.lineEditStatus_1.setText('The Measurement For Device 1 Has Stopped')
            #self.Yokogawa_1.write('OUTP OFF')
            self.Yokogawa_1.close()
            
        elif self.ui.radioButtonTwo.isChecked():
            self.Device1DataThread.stop_check = True
            self.Device1DataThread.break_check = True
            self.Device1DataThread.Device1Pause = True
            self.Device1DataThread.quit()
            self.ui.lineEditStatus_1.setText('The Measurement For Device 1 Has Stopped')

            self.Device2DataThread.break_check = True
            self.Device2DataThread.stop_check = True   
            self.Device2DataThread.Device2Pause = True
            self.Device2DataThread.quit()
            self.ui.lineEditStatus_2.setText('The Measurement For Device 2 Has Stopped')

            #self.Yokogawa_1.write('OUTP OFF')
            #self.Yokogawa_2.write('OUTP OFF')
            self.Yokogawa_1.close()
            self.Yokogawa_2.close()
        else:
            self.Device1DataThread.stop_check = True
            self.Device1DataThread.break_check = True
            self.Device1DataThread.Device1Pause = True
            self.Device1DataThread.quit()
            self.ui.lineEditStatus_1.setText('The Measurement For Device 1 Has Stopped')

            self.Device2DataThread.break_check = True
            self.Device2DataThread.stop_check = True
            self.Device2DataThread.Device2Pause = True
            self.Device2DataThread.quit()
            self.ui.lineEditStatus_2.setText('The Measurement For Device 2 Has Stopped')

            self.Device3DataThread.break_check = True
            self.Device3DataThread.stop_check = True
            self.Device3DataThread.Device3Pause = True
            self.Device3DataThread.quit()
            self.ui.lineEditStatus_3.setText('The Measurement For Device 3 Has Stopped')
            #self.Yokogawa_1.write('OUTP OFF')
            #self.Yokogawa_2.write('OUTP OFF')
            #self.Yokogawa_3.write('OUTP OFF')
            self.Yokogawa_1.close()
            self.Yokogawa_2.close()
            self.Yokogawa_3.close()

        
    def Plot_Device1(self):
        self.curve_item_device_1.plot().replot()
        self.ui.curvewidgetDevice1.plot.do_autoscale()


    def Plot_Device2(self):
        self.curve_item_device_2.plot().replot()
        self.ui.curvewidgetDevice2.plot.do_autoscale()

        
    def Plot_Device3(self):
        self.curve_item_device_3.plot().replot()
        self.ui.curvewidgetDevice3.plot.do_autoscale()

                
    def stopDevice1(self):
        self.Device1DataThread.stop_check = True
        self.Device1DataThread.break_check = True
        self.Device1DataThread.Device1Pause = True
        self.Device1DataThread.quit()
        self.ui.lineEditStatus_1.setText('The Measurement For Device 1 Has Stopped')
        
    def stopDevice2(self):
        self.Device2DataThread.break_check = True
        self.Device2DataThread.stop_check = True
        self.Device2DataThread.Device2Pause = True
        self.Device2DataThread.quit()
        self.ui.lineEditStatus_2.setText('The Measurement For Device 1 Has Stopped')
        
    def stopDevice3(self):
        self.Device3DataThread.break_check = True
        self.Device3DataThread.stop_check = True
        self.Device3DataThread.Device3Pause = True
        self.Device3DataThread.quit()
        self.ui.lineEditStatus_3.setText('The Measurement For Device 2 Has Stopped')
        
    def closeEvent(self, question):
        print question
        quit_msg = "Do you want to quit this program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            question.accept()
        else:
            question.ignore()

class CollectDevice1Data(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self,parent)
        self.exiting = False
        
    def initial_input(self, ui):
        self.ui = ui
        
    def input(self, ui, curveDevice1, timestep, timedelay, LockIn_Sens, PreAmp, OutVoltage, Resistor, Yokogawa, Agilent):
        self.ui = ui
        self.curveDevice1 = curveDevice1
        self.timestep = timestep
        self.timedelay = timedelay
        self.LockIn1_Sens = LockIn_Sens
        self.PreAmp1 = PreAmp
        self.OutVoltage1 = OutVoltage
        self.Resistor1 = Resistor
        self.Yokogawa1 = Yokogawa
        self.Agilent1 = Agilent
        
        self.Current1 = np.array([], dtype = float)
        self.Voltage1 = np.array([], dtype = float)
        self.Resistance1 = np.array([], dtype = float)
        
        self.RampUpArray1 = np.array([], dtype = float)
        self.StepArray1 = np.array([], dtype = float)
        self.RampDownArray1 = np.array([], dtype = float)
        
        self.RampUpStep1 = float(self.ui.lineEditInitialRamp_Step_1.text())
        self.StepSize1 = float(self.ui.lineEditCollect_Step_1.text())
        self.RampDownStep1 = float(self.ui.lineEditFinalRamp_Step_1.text())
        self.Agilent1.write('MEAS:VOLT?')
        #Arrays
        Temp = (float(self.ui.lineEditInitialRamp_End_1.text())-float(self.ui.lineEditInitialRamp_Start_1.text()))/self.RampUpStep1
        for i in range(0, int(Temp) + 1):
            self.RampUpArray1 = np.append(self.RampUpArray1, float(self.ui.lineEditInitialRamp_Start_1.text())+ self.RampUpStep1*i)
            
        Temp = (float(self.ui.lineEditCollect_End_1.text())-float(self.ui.lineEditCollect_Start_1.text()))/self.StepSize1
        for i in range(0, int(Temp) +1):
            self.StepArray1 = np.append(self.StepArray1, float(self.ui.lineEditCollect_Start_1.text())+ self.StepSize1*i)
            
        Temp = (float(self.ui.lineEditFinalRamp_End_1.text())-float(self.ui.lineEditFinalRamp_Start_1.text()))/self.RampDownStep1
        for i in range(0, int(Temp)+1):
            self.RampDownArray1 = np.append(self.RampDownArray1, float(self.ui.lineEditFinalRamp_Start_1.text()) + self.RampDownStep1*i)
            
        self.RampUpArray1 = self.RampUpArray1*1E-03
        self.StepArray1 = self.StepArray1*1E-03
        self.RampDownArray1 = self.RampDownArray1*1E-03
        self.Device1Pause = False
        self.Yokogawa1.write('OUTP ON')
        self.Yokogawa1.write('SOUR:FUNC VOLT')
        self.DirectoryCheck = False
        self.save_information()
        
        if self.CustomDirectory == True:
            if not os.path.isdir(self.directory):
                print self.directory
                os.makedirs(self.directory)
            #self.f_name = self.directory + '\\' + self.File_Name + self.type
        else:
            #self.f_name = self.File_Name + self.type
            pass
        
        self.Save_Index = 0
        self.stop_check = False
        self.break_check = False
        self.start()
        
    def run(self):
        while True:
            self.ui.curvewidgetDevice1.plot.set_titles('Resistance v. Current', 'Current (A)', 'Resistance (Ohms)')
            if not self.Device1Pause:
                self.RampUp()
                for i in range(0, len(self.StepArray1)):
                    self.Yokogawa1.write('SOUR:LEV:AUTO ' +str(self.StepArray1[i]))
                    time.sleep(self.timedelay)
                    
                    # self.Agilent1.write('SAMP:COUN 3')
                    # self.Agilent1.write('TRIG:SOUR BUS')
                    # self.Agilent1.write('INIT')
                    # self.Agilent1.write('*TRG')
                    # string_ = self.Agilent.query('FETCH?').replace("\n", "")
                    # list_ = string_.split(",")
                    # total = 0
                    # for i in range(0, len(list_)):
                    #     total += float(list_[i])*self.LockIn1_Sens/(10*self.PreAmp1)
                    # avg = total/float(len(list_))

                    VoltageReading = float(self.Agilent1.ask('READ?'))*self.LockIn1_Sens/(10*self.PreAmp1)
                    #VoltageReading = avg
                    CurrentLockIn = self.OutVoltage1/self.Resistor1
                    CurrentReading = self.StepArray1[i]/self.Resistor1
                    ResistanceReading = VoltageReading/CurrentLockIn
                    self.ui.labelDevice1Resistance.setText(str(ResistanceReading))
                    self.Voltage1 = np.append(self.Voltage1, VoltageReading)
                    self.Current1 = np.append(self.Current1, CurrentReading)
                    self.Resistance1 = np.append(self.Resistance1, ResistanceReading)
                    self.curveDevice1.set_data(self.Current1, self.Resistance1)
                    self.emit(SIGNAL('Plot1'))
                    if self.Save_Index == 0:
                        self.f_name = self.directory + '\\' + self.File_Name + ' ' + self.date + ' ' + 'B_Field ' + str(self.ui.label_BField_Value.text()) + self.type
                    else:
                        pass
                    if i == 0:
                        f = open(self.f_name, 'w')
                        f.write('Lock In Sens: ' + str(self.LockIn1_Sens) + '\n')
                        f.write('Resistor Value (Ohms): ' + str(self.Resistor1) + '\n')
                        f.write('Lock-In Output (Volts): ' + str(self.OutVoltage1) + '\n')
                        f.write('B Field Strength: ' + str(self.ui.label_BField_Value.text()) + '\n')
                        f.write('Collected Data' + '\n')
                        f.write('Current' + self.divide + 'Resistance' + '\n')
                        f.write('A' + self.divide + 'Ohms' + '\n' )
                        f.write(str(CurrentReading) + self.divide + str(ResistanceReading) + '\n')
                    else:
                        f = open(self.f_name, 'a')
                        f.write(str(CurrentReading) + self.divide + str(ResistanceReading) + '\n')
                    if self.stop_check == False:
                        pass
                    else:
                        break
                Finish_Check = True
                if self.stop_check == False:
                    self.RampDown()
                else:
                    Finish_Check = False
                self.Save_Index += 1
                self.emit(SIGNAL('Device1_Check'), Finish_Check, self.Current1, self.Resistance1)
                self.reset_sweep()

            else:
                if self.break_check == False:
                    pass
                else:
                    break
            
    def RampUp(self):
        for i in range(0, len(self.RampUpArray1)):
            self.Yokogawa1.write('SOUR:LEV:AUTO ' + str(self.RampUpArray1[i]))
            time.sleep(self.timestep)
            
    def RampDown(self):
        for i in range(0, len(self.RampDownArray1)):
            self.Yokogawa1.write('SOUR:LEV:AUTO ' + str(self.RampDownArray1[i]))
            time.sleep(self.timestep)
            
    def reset_sweep(self):
        self.Current1 = np.array([], dtype = float)
        self.Voltage1 = np.array([], dtype = float)
        self.Resistance1 = np.array([], dtype = float)
        self.curveDevice1.set_data(self.Current1, self.Resistance1)
        self.emit(SIGNAL('Plot1'))
        
    def save_information(self):
        if self.ui.radioButton_CSV_1.isChecked():
            self.type = '.csv'
            self.divide = ','
            self.form = ''
        elif self.ui.radioButton_TXT_1.isChecked():
            self.type = '.txt'
            self.divide = '\t'
            self.form = ''
        else:
            self.type = False
            
        self.File_Name = str(self.ui.lineEditFileName_1.text())

    def browse(self):
        prev_dir = 'C:\\'
        file_list = []
        file_dir = QFileDialog.getExistingDirectory(None, 'Select The GoogleDrive Folder', prev_dir)
        if file_dir != '':
            file_list = str(file_dir).split('/')
            file_dir.replace('/', '\\')
            self.ui.lineEditSaveDirectory_1.setText(file_dir)
        self.directory = ''

    def select_name(self):
        file_list= []
        file_list = str(self.ui.lineEditSaveDirectory_1.text()).split('\\')
        for i in range(0, len(file_list)):
            self.directory += file_list[i] + '\\'
        now = datetime.now()
        date = '%s-%s-%s' % (now.year, now.month, now.day)
        self.date = date
        self.directory = self.directory + "Data\\"+ date
        self.CustomDirectory = True
        self.ui.lineEditStatus_1.setText('A Directory has been chosen. ')
        print self.directory
    def __del__(self):
        self.exiting = True
        self.wait()
                
class CollectDevice2Data(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self,parent)
        self.exiting = False
    def initial_input(self, ui):
        self.ui = ui
        
    def input(self, ui, curveDevice2, timestep, timedelay, LockIn_Sens, PreAmp, OutVoltage, Resistor, Yokogawa, Agilent):
        self.ui = ui
        self.curveDevice2 = curveDevice2
        self.timestep = timestep
        self.timedelay = timedelay
        self.LockIn2_Sens = LockIn_Sens
        self.PreAmp2 = PreAmp
        self.OutVoltage2 = OutVoltage
        self.Resistor2 = Resistor
        self.Yokogawa2 = Yokogawa
        self.Agilent2 = Agilent
        
        self.Current2 = np.array([], dtype = float)
        self.Voltage2 = np.array([], dtype = float)
        self.Resistance2 = np.array([], dtype = float)
        self.RampUpArray2 = np.array([], dtype = float)
        self.StepArray2 = np.array([], dtype = float)
        self.RampDownArray2 = np.array([], dtype = float)
        
        self.RampUpStep2 = float(self.ui.lineEditInitialRamp_Step_2.text())
        self.StepSize2 = float(self.ui.lineEditCollect_Step_2.text())
        self.RampDownStep2 = float(self.ui.lineEditFinalRamp_Step_2.text())
        self.Agilent2.write('MEAS:VOLT?')
        #Arrays
        Temp = (float(self.ui.lineEditInitialRamp_End_2.text())-float(self.ui.lineEditInitialRamp_Start_2.text()))/self.RampUpStep2
        for i in range(0, int(Temp)+1):
            self.RampUpArray2 = np.append(self.RampUpArray2, float(self.ui.lineEditInitialRamp_Start_2.text())+ self.RampUpStep2*i)
            
        Temp = (float(self.ui.lineEditCollect_End_2.text())-float(self.ui.lineEditCollect_Start_2.text()))/self.StepSize2
        for i in range(0, int(Temp)+1):
            self.StepArray2 = np.append(self.StepArray2, float(self.ui.lineEditCollect_Start_2.text())+ self.StepSize2*i)
            
        Temp = (float(self.ui.lineEditFinalRamp_End_2.text())-float(self.ui.lineEditFinalRamp_Start_2.text()))/self.RampDownStep2
        for i in range(0, int(Temp)+1):
            self.RampDownArray2 = np.append(self.RampDownArray2, float(self.ui.lineEditFinalRamp_Start_2.text()) + self.RampDownStep2*i)
            
        self.RampUpArray2 = self.RampUpArray2*1E-03
        self.StepArray2 = self.StepArray2*1E-03
        self.RampDownArray2 = self.RampDownArray2*1E-03
        
        self.Device2Pause = False
        self.Yokogawa2.write('OUTP ON')
        self.Yokogawa2.write('SOUR:FUNC VOLT')
        
        self.Save_Index = 0
        self.save_information()
        if self.CustomDirectory == True:
            if not os.path.isdir(self.directory):
                os.makedirs(self.directory)
            #self.f_name = self.directory + '\\' + self.File_Name + self.type
        else:
            #self.f_name = self.File_Name + self.type
            pass
                        
        self.stop_check = False
        self.break_check = False
        #self.run()
        self.start()
        
    def run(self):
        while True:
            self.ui.curvewidgetDevice2.plot.set_titles('Resistance v. Current', 'Current (A)', 'Resistance (Ohms)')
            if not self.Device2Pause:
                self.RampUp()
                for i in range(0, len(self.StepArray2)):
                    self.Yokogawa2.write('SOUR:LEV:AUTO ' +str(self.StepArray2[i]))
                    time.sleep(self.timedelay)

##                    self.Agilent2.write('SAMP:COUN 3')
##                    self.Agilent2.write('TRIG:SOUR BUS')
##                    self.Agilent2.write('INIT')
##                    self.Agilent2.write('*TRG')
##                    string_ = self.Agilent2.query('FETCH?').replace("\n", "")
##                    list_ = string_.split(",")
##                    total = 0
##                    for i in range(0, len(list_)):
##                        total += float(list_[i])*self.LockIn2_Sens/(10*self.PreAmp2)
##                    avg = total/float(len(list_))
##
##                    VoltageReading = avg
##                    
                    VoltageReading = float(self.Agilent2.ask('READ?'))*self.LockIn2_Sens/(10*self.PreAmp2)
                    CurrentReading = self.StepArray2[i]/self.Resistor2
                    CurrentLockIn = self.OutVoltage2/self.Resistor2
                    ResistanceReading = VoltageReading/CurrentLockIn
                    self.ui.labelDevice2Resistance.setText(str(ResistanceReading))
                    self.Voltage2 = np.append(self.Voltage2, VoltageReading)
                    self.Current2 = np.append(self.Current2, CurrentReading)
                    self.Resistance2 = np.append(self.Resistance2, ResistanceReading)
                    self.curveDevice2.set_data(self.Current2, self.Resistance2)
                    self.emit(SIGNAL('Plot2'))
                    if self.Save_Index == 0:
                        self.f_name = self.directory + '\\' + self.File_Name + ' ' + self.date + ' ' + 'B_Field ' + str(self.ui.label_BField_Value.text()) + self.type
                    else:
                        pass
                    if i == 0:
                        f = open(self.f_name, 'w')
                        f.write('Lock In Sens: ' + str(self.LockIn2_Sens) + '\n')
                        f.write('Resistor Value (Ohms): ' + str(self.Resistor2) + '\n')
                        f.write('Lock-In Output (Volts): ' + str(self.OutVoltage2) + '\n')
                        f.write('B Field Strength: ' + str(self.ui.label_BField_Value.text()) + '\n')
                        f.write('Collected Data' + '\n')
                        f.write('Current' + self.divide + 'Resistance' + '\n')
                        f.write('A' + self.divide + 'Ohms' + '\n' )
                        f.write(str(CurrentReading) + self.divide + str(ResistanceReading) + '\n')
                    else:
                        f = open(self.f_name, 'a')
                        f.write(str(CurrentReading) + self.divide + str(ResistanceReading) + '\n')
                    if self.stop_check == False:
                        pass
                    else:
                        break
                Finish_Check = True
                if self.stop_check == False:
                    self.RampDown()
                else:
                    Finish_Check = False
                self.Save_Index += 1
                self.emit(SIGNAL('Device2_Check'), Finish_Check, self.Current2, self.Resistance2)
                self.reset_sweep()

            else:
                if self.break_check == False:
                    pass
                else:
                    break
    def RampUp(self):
        for i in range(0, len(self.RampUpArray2)):
            self.Yokogawa2.write('SOUR:LEV:AUTO ' + str(self.RampUpArray2[i]))
            time.sleep(self.timestep)
            
    def RampDown(self):
        for i in range(0, len(self.RampDownArray2)):
            self.Yokogawa2.write('SOUR:LEV:AUTO ' + str(self.RampDownArray2[i]))
            time.sleep(self.timestep)
            
    def reset_sweep(self):
        self.Current2 = np.array([], dtype = float)
        self.Voltage2 = np.array([], dtype = float)
        self.Resistance2 = np.array([], dtype = float)
        self.curveDevice2.set_data(self.Current2, self.Resistance2)
        self.emit(SIGNAL('Plot2'))
        
    def save_information(self):
        if self.ui.radioButton_CSV_2.isChecked():
            self.type = '.csv'
            self.divide = ','
            self.form = ''
        elif self.ui.radioButton_TXT_2.isChecked():
            self.type = '.txt'
            self.divide = '\t'
            self.form = ''
        else:
            self.type = False
            
        self.File_Name = str(self.ui.lineEditFileName_2.text())
        
    def browse(self):
        prev_dir = 'C:\\'
        file_list = []
        file_dir = QFileDialog.getExistingDirectory(None, 'Select The GoogleDrive Folder', prev_dir)
        if file_dir != '':
            file_list = str(file_dir).split('/')
            file_dir.replace('/', '\\')
            self.ui.lineEditSaveDirectory_2.setText(file_dir)
        self.directory = ''

    def select_name(self):
        file_list= []
        file_list = str(self.ui.lineEditSaveDirectory_2.text()).split('\\')
        for i in range(0, len(file_list)):
            self.directory += file_list[i] + '\\'
        now = datetime.now()
        date = '%s-%s-%s' % (now.year, now.month, now.day)
        self.date = date
        self.directory = self.directory + "Data\\"+ date
        self.CustomDirectory = True
        self.ui.lineEditStatus_2.setText('A Directory has been chosen')
        
    def __del__(self):
        self.exiting = True
        self.wait()
            
class CollectDevice3Data(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self,parent)
        self.exiting = False

    def initial_input(self, ui):
        self.ui = ui
        
    def input(self, ui, curveDevice3, timestep, timedelay, LockIn_Sens, PreAmp, OutVoltage, Resistor, Yokogawa, Agilent):
        self.ui = ui
        self.curveDevice3 = curveDevice3
        self.timestep = timestep
        self.timedelay = timedelay
        self.LockIn3_Sens = LockIn_Sens
        self.PreAmp3 = PreAmp
        self.OutVoltage3 = OutVoltage
        self.Resistor3 = Resistor
        self.Yokogawa3 = Yokogawa
        self.Agilent3 = Agilent
        
        self.Current3 = np.array([], dtype = float)
        self.Voltage3 = np.array([], dtype = float)
        self.Resistance3 = np.array([], dtype = float)
        
        self.RampUpArray3 = np.array([], dtype = float)
        self.StepArray3 = np.array([], dtype = float)
        self.RampDownArray3 = np.array([], dtype = float)
        
        self.RampUpStep3 = float(self.ui.lineEditInitialRamp_Step_3.text())
        self.StepSize3 = float(self.ui.lineEditCollect_Step_3.text())
        self.RampDownStep3 = float(self.ui.lineEditFinalRamp_Step_3.text())
        self.Agilent3.write('MEAS:VOLT?')
        #Arrays
        Temp = (float(self.ui.lineEditInitialRamp_End_3.text())-float(self.ui.lineEditInitialRamp_Start_3.text()))/self.RampUpStep3
        for i in range(0, int(Temp)+1):
            self.RampUpArray3 = np.append(self.RampUpArray3, float(self.ui.lineEditInitialRamp_Start_3.text())+ self.RampUpStep3*i)
            
        Temp = (float(self.ui.lineEditCollect_End_3.text())-float(self.ui.lineEditCollect_Start_3.text()))/self.StepSize3
        for i in range(0, int(Temp)+1):
            self.StepArray3 = np.append(self.StepArray3, float(self.ui.lineEditCollect_Start_3.text())+ self.StepSize3*i)
            
        Temp = (float(self.ui.lineEditFinalRamp_End_3.text())-float(self.ui.lineEditFinalRamp_Start_3.text()))/self.RampDownStep3
        for i in range(0,int(Temp)+1):
            self.RampDownArray3 = np.append(self.RampDownArray3, float(self.ui.lineEditFinalRamp_Start_3.text()) + self.RampDownStep3*i)
            
        self.RampUpArray3 = self.RampUpArray3*1E-03
        self.StepArray3 = self.StepArray3*1E-03
        self.RampDownArray3 = self.RampDownArray3*1E-03
        
        self.Device3Pause = False
        self.Yokogawa3.write('OUTP ON')
        self.Yokogawa3.write('SOUR:FUNC VOLT')
        
        self.Save_Index = 0
        self.save_information()
        
        if self.CustomDirectory == True:
            if not os.path.isdir(self.directory):
                os.makedirs(self.directory)
            #self.f_name = self.directory + '\\' + self.File_Name + self.type
        else:
            #self.f_name = self.File_Name + self.type
            pass
        self.stop_check = False
        self.break_check = False
        self.start()
        
    def run(self):
        while True:
            self.ui.curvewidgetDevice3.plot.set_titles('Resistance v. Current', 'Current (A)', 'Resistance (Ohms)')
            if not self.Device3Pause:
                self.RampUp()
                for i in range(0, len(self.StepArray3)):
                    self.Yokogawa3.write('SOUR:LEV:AUTO ' +str(self.StepArray3[i]))
                    time.sleep(self.timedelay)
                    
##                    self.Agilent3.write('SAMP:COUN 3')
##                    self.Agilent3.write('TRIG:SOUR BUS')
##                    self.Agilent3.write('INIT')
##                    self.Agilent3.write('*TRG')
##                    string_ = self.Agilent3.query('FETCH?').replace("\n", "")
##                    list_ = string_.split(",")
##                    total = 0
##                    for i in range(0, len(list_)):
##                        total += float(list_[i])*self.LockIn3_Sens/(10*self.PreAmp3)
##                    avg = total/float(len(list_))
##
##                    VoltageReading = avg
                    
                    VoltageReading = float(self.Agilent3.ask('READ?'))*self.LockIn3_Sens/(10*self.PreAmp3)
                    CurrentReading = self.StepArray3[i]/self.Resistor3
                    CurrentLockIn = self.OutVoltage3/self.Resistor3
                    ResistanceReading = VoltageReading/CurrentLockIn
                    self.ui.labelDevice3Resistance.setText(str(ResistanceReading))
                    self.Voltage3 = np.append(self.Voltage3, VoltageReading)
                    self.Current3 = np.append(self.Current3, CurrentReading)
                    self.Resistance3 = np.append(self.Resistance3, ResistanceReading)
                    self.curveDevice3.set_data(self.Current3, self.Resistance3)
                    self.emit(SIGNAL('Plot3'))
                    if self.Save_Index == 0:
                        self.f_name = self.directory + '\\' + self.File_Name + ' ' + self.date + ' ' + 'B_Field ' + str(self.ui.label_BField_Value.text()) + self.type
                    else:
                        pass
                    if i == 0: 
                        f = open(self.f_name, 'w')
                        f.write('Lock In Sens: ' + str(self.LockIn3_Sens) + '\n')
                        f.write('Resistor Value (Ohms): ' + str(self.Resistor3) + '\n')
                        f.write('Lock-In Output (Volts): ' + str(self.OutVoltage3) + '\n')
                        f.write('B Field Strength: ' + str(self.ui.label_BField_Value.text()) + '\n')
                        f.write('Collected Data' + '\n')
                        f.write('Current' + self.divide + 'Resistance' + '\n')
                        f.write('A' + self.divide + 'Ohms' + '\n' )
                        f.write(str(CurrentReading) + self.divide + str(ResistanceReading) + '\n')
                    else:
                        f = open(self.f_name, 'a')
                        f.write(str(CurrentReading) + self.divide + str(ResistanceReading) + '\n')
                    if self.stop_check == False:
                        pass
                    else:
                        break
                Finish_Check = True
                if self.stop_check == False:
                    self.RampDown()
                else:
                    Finish_Check = False
                self.Save_Index += 1
                self.emit(SIGNAL('Device3_Check'), Finish_Check, self.Current3, self.Resistance3)
                self.reset_sweep()

            else:
                if self.break_check == False:
                    pass
                else:
                    break
    def RampUp(self):
        for i in range(0, len(self.RampUpArray3)):
            self.Yokogawa3.write('SOUR:LEV:AUTO ' + str(self.RampUpArray3[i]))
            time.sleep(self.timestep)
            
    def RampDown(self):
        for i in range(0, len(self.RampDownArray3)):
            self.Yokogawa3.write('SOUR:LEV:AUTO ' + str(self.RampDownArray3[i]))
            time.sleep(self.timestep)
            
    def reset_sweep(self):
        self.Current3 = np.array([], dtype = float)
        self.Voltage3 = np.array([], dtype = float)
        self.Resistance3 = np.array([], dtype = float)
        self.curveDevice3.set_data(self.Current3, self.Resistance3)
        self.emit(SIGNAL('Plot3'))
        
    def save_information(self):
        if self.ui.radioButton_CSV_3.isChecked():
            self.type = '.csv'
            self.divide = ','
            self.form = ''
        elif self.ui.radioButton_TXT_3.isChecked():
            self.type = '.txt'
            self.divide = '\t'
            self.form = ''
        else:
            self.type = False
            
        self.File_Name = str(self.ui.lineEditFileName_3.text())
        
    def browse(self):
        prev_dir = 'C:\\'
        file_list = []
        file_dir = QFileDialog.getExistingDirectory(None, 'Select The GoogleDrive Folder', prev_dir)
        if file_dir != '':
            file_list = str(file_dir).split('/')
            file_dir.replace('/', '\\')
            self.ui.lineEditSaveDirectory_3.setText(file_dir)
        self.directory = ''

    def select_name(self):
        file_list= []
        file_list = str(self.ui.lineEditSaveDirectory_3.text()).split('\\')
        for i in range(0, len(file_list)):
            self.directory += file_list[i] + '\\'
        now = datetime.now()
        date = '%s-%s-%s' % (now.year, now.month, now.day)
        self.date = date
        self.directory = self.directory + "Data\\"+ date
        self.CustomDirectory = True
        self.ui.lineEditStatus_3.setText('A Directory has been chosen')
    def __del__(self):
        self.exiting = True
        self.wait()
            
if __name__ == "__main__":
    # Opens the GUI
    app = QApplication(sys.argv)
    myapp = MyForm()
    
    # Shows the GUI
    myapp.show()
    
    # Exits the GUI when the x button is clicked
    sys.exit(app.exec_())
