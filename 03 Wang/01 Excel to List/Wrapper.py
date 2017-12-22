# Import numpy library
import numpy

import datetime, time

import os

import sys

from Tkinter import *
from tkFileDialog import *
from tkMessageBox import showerror

# Import pylab library
# It contains some functions necessary to create some of the functions in the use of the plots
from pylab import *

# Adding navigation toolbar to the figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

# Import the PyQt4 modules for all the commands that control the GUI.
# Importing as from "Module" import 
from PyQt4.QtCore import *
from PyQt4.QtGui import *

linelist =[]



# This is very important because it imports the GUI created earlier using Qt Designer
# To import the GUI from another python file, it is very somple. Just following the following steps:
# 1. Creat an empty file called __init__.py in the same directory as the GUI file
# 2. If the GUI file and __init__.py file are in the same directory as this file, just type "from .GUIfilename import classname"
# 3. If the GUI file and __init__.py file are in the sub file of this file, then type "from subfilename.GUIfilename.GUIfilename import classname"
# classname is the name of the class in the GUI file, usually it should be 'Ui_MainWindow'

from Sub_Scripts.GUI import Ui_MainWindow

# This class controls all the operations of the GUI. This is the main class that contains all the functions that control the GUI.
class MyForm(QMainWindow):
    
    # The __init__ function is what everything the user wants to be initialized when the class is called.
    # Here we shall define the tring functions to corresponding variables.
    # The 'self' variable means that the function is part of the class and can be called inside and outside the class.
    def __init__(self, parent = None):
        
        # Standard GUI code
        QWidget.__init__(self, parent)
        
        # All the GUI data and widgets in the Ui_MainWindow() class is defined to "self.ui"
        # Thus to do anything on the GUI, the commands must go through this variable
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # For the canvas.
        self.canvas = FigureCanvas(self.ui.mplwidget.figure)
        self.canvas.setParent(self.ui.widget)
        # We need the toolbar widget for the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.ui.widget)

        # For the canvas.
        self.canvas_first_step = FigureCanvas(self.ui.mplwidget_first_step.figure)
        self.canvas_first_step.setParent(self.ui.widget_first_step)
        # We need the toolbar widget for the canvas
        self.mpl_toolbar_first_step = NavigationToolbar(self.canvas_first_step, self.ui.widget_first_step)
        
        # For the canvas.
        self.canvas_second_step = FigureCanvas(self.ui.mplwidget_second_step.figure)
        self.canvas_second_step.setParent(self.ui.widget_second_step)
        # We need the toolbar widget for the canvas
        self.mpl_toolbar_second_step = NavigationToolbar(self.canvas_second_step, self.ui.widget_second_step)
        
        
        # Create the QVBoxLayout object and add the widget into the layout
        vbox = QVBoxLayout()
        # The matplotlib canvas
        vbox.addWidget(self.canvas)
        # The matplotlib toolbar
        vbox.addWidget(self.mpl_toolbar)
        self.ui.widget.setLayout(vbox)
        
        # Create the QVBoxLayout object and add the widget into the layout
        vbox_first_step = QVBoxLayout()
        # The matplotlib canvas
        vbox_first_step.addWidget(self.canvas_first_step)
        # The matplotlib toolbar
        vbox_first_step.addWidget(self.mpl_toolbar_first_step)
        self.ui.widget_first_step.setLayout(vbox_first_step)
        
        # Create the QVBoxLayout object and add the widget into the layout
        vbox_second_step = QVBoxLayout()
        # The matplotlib canvas
        vbox_second_step.addWidget(self.canvas_second_step)
        # The matplotlib toolbar
        vbox_second_step.addWidget(self.mpl_toolbar_second_step)
        self.ui.widget_second_step.setLayout(vbox_second_step)
        
        
        # Connect the mplwidget with canvas
        self.ui.mplwidget = self.canvas
        
        # Connect the mplwidget with canvas
        self.ui.mplwidget_first_step = self.canvas_first_step
        
        # Connect the mplwidget with canvas
        self.ui.mplwidget_second_step = self.canvas_second_step
        
        self.connect(self.ui.pushButton_browse, SIGNAL('clicked()'), self.Browse)
        self.connect(self.ui.pushButton_change_name, SIGNAL('clicked()'), self.Change_name)
        self.connect(self.ui.pushButton_openfile, SIGNAL('clicked()'), self.OpenFile)
        self.connect(self.ui.radioButton_qmd, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.radioButton_ppms, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.radioButton_frontpanel, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.radioButton_zbridge, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.radioButton_compressor, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.pushButton_Plot, SIGNAL('clicked()'), self.Plot_ready)
        self.connect(self.ui.pushButton_recent, SIGNAL('clicked()'), self.Open_Recent)
        self.connect(self.ui.pushButton_plot_first_step, SIGNAL('clicked()'), self.plot1)
        self.connect(self.ui.pushButton_plot_second_step, SIGNAL('clicked()'), self.plot2)
        self.connect(self.ui.pushButton_find, SIGNAL('clicked()'), self.Find)
        self.connect(self.ui.pushButton_modify, SIGNAL('clicked()'), self.Modify)
        self.connect(self.ui.pushButton_return, SIGNAL('clicked()'), self.Return)

        self.first_round = True
        self.open_dir = ''
        self.open_files_number = 0
        self.all_info = []
        
    def Choose_type(self):
        if self.ui.radioButton_qmd.isChecked():
            self.divider = 'Collected Data'
            self.ui.lineEdit_divider.setText(self.divider)
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition.setText('Please choose your file.')
        elif self.ui.radioButton_ppms.isChecked():
            self.divider = '[Data]'
            self.ui.lineEdit_divider.setText(self.divider)
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition.setText('Please choose your file.')
        elif self.ui.radioButton_frontpanel.isChecked():
            self.divider = 'frontpanel'
            self.ui.lineEdit_divider.setText('None')
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition.setText('Please choose your file.')
        elif self.ui.radioButton_zbridge.isChecked():
            self.divider = '#'
            self.ui.lineEdit_divider.setText(self.divider)
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition.setText('Please choose your file.')
        elif self.ui.radioButton_compressor.isChecked():
            self.divider = 'compressor'
            self.ui.lineEdit_divider.setText('None')
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition.setText('Please choose your file.')
            
    def Browse(self):
        self.open_recent = False
        
        prev_dir = os.getcwd()
        if self.ui.lineEdit_address.text() == '' or self.ui.lineEdit_address.text() == 'None':
            fileDir = QFileDialog.getOpenFileName(self, 'Select Folder to Save', prev_dir)
        else:
            fileDir = QFileDialog.getOpenFileName(self, 'Select Folder to Save', self.ui.lineEdit_address.text())
        if fileDir != '':
            open_dir = ''
            file_list = str(fileDir).split('/')
            for i in range(0, len(file_list) - 1):
                if i < len(file_list) - 1:
                    open_dir += file_list[i] + '\\'
                elif i == len(file_list) - 1:
                    open_dir += file_list[i]
            fileDir.replace('/', '\\')
            self.ui.lineEdit_address.setText(fileDir)
            
            self.ui.pushButton_openfile.setEnabled(True)
            self.ui.groupBox_labels.setEnabled(True)
            self.first_round = False
            filedir = str(fileDir).split('\\')
            self.file_name = filedir[len(filedir) - 1]
        else:
            self.ui.lineEdit_address.setText('None')
            self.ui.lineEdit_condition.setText('Failed to Read File')
        
    def OpenFile(self):
        
        # Every you click the "Open File" button, the content in the plot combox is refreshed
        self.reset_plot()
        self.ui.mplwidget.draw()
        self.reset_first_step_plot()
        self.reset_second_step_plot()
        self.ui.comboBox_x.clear()
        self.ui.comboBox_y1.clear()
        self.ui.comboBox_y2.clear()
        self.ui.comboBox_y3.clear()
        self.ui.comboBox_y4.clear()
        self.ui.comboBox_y5.clear()
        self.ui.comboBox_second_x.clear()
        self.ui.comboBox_second_y1.clear()
        self.ui.comboBox_second_y2.clear()
        self.ui.comboBox_second_y3.clear()
        self.ui.comboBox_second_y4.clear()
        self.ui.comboBox_second_y5.clear()
        self.ui.comboBox_y_first_step.clear()
        self.ui.comboBox_y_second_step.clear()
        self.ui.comboBox_first.clear()
        self.ui.comboBox_second.clear()
        self.ui.lineEdit_x.setText('')
        self.ui.lineEdit_y.setText('')
        self.ui.lineEdit_name.setText('')
        self.ui.lineEdit_condition.setText('')
        self.ui.lineEdit_minute.setText('')
        self.ui.lineEdit_date.setText('')
        
        labels = ''
        
        raw_parameters = []
        units = []
        parameters = []
        new_parameters = []
        self.data = []
        new_data = []
        first_data = []
        self.date_time = []
        temp_parameters = []
        
        item = 0
        z_item = 0
        length = 0
        # This count is the number of the reading loops for labels. If count is over 1000, that means there's something wrong with the divider line and it helps to stop the program
        count = 0
        
        # It is false when program cannot find the line divider and runs the while loop 1000 times
        self.divider_found = True
        
        self.fileDir = self.ui.lineEdit_address.text()
        self.divider = str(self.ui.lineEdit_divider.text())
        fp = open(self.fileDir)
        if self.ui.radioButton_frontpanel.isChecked():
            labels = 'None'
        elif self.ui.radioButton_compressor.isChecked():
            labels = fp.readline()
        elif self.ui.radioButton_zbridge.isChecked():
            line = fp.readline()
            labels += line
            line = fp.readline()
            labels += line
            line = fp.readline()
            linelist = line.split(':')
            namelist = linelist[1].split('\t')
            labels += '        ' + linelist[0] + ':\n'
            for i in range(0, len(namelist) - 1):
                labels += '\t' + str(i) + '. ' + namelist[i] + '\n'
            labels += '\t' + str(len(namelist) - 1) + '. ' + namelist[len(namelist) - 1] + '\n'
            line = fp.readline()
            linelist = line.split(':')
            namelist = linelist[1].split('\t')
            labels += '        ' + linelist[0] + ':\n'
            for i in range(0, len(namelist) - 1):
                labels += '\t' + str(i) + '. ' + namelist[i] + '\n'
            labels += '\t' + str(len(namelist) - 1) + '. ' + namelist[len(namelist) - 1] + '\n'
            line = fp.readline()
            linelist = line.split(':')
            namelist = linelist[1].split('\t')
            labels += linelist[0] + ':\n'
            for i in range(0, len(namelist)):
                labels += '\t' + str(i) + '. ' + namelist[i] + '\n'
            line = fp.readline()
        else:
            while True:
                if count > 1000:
                    self.ui.lineEdit_condition.setText('Line divider is not found.')
                    self.divider_found = False
                    break
                line = fp.readline()
                linelist = line.split(',')
                if linelist[0].upper() == self.divider.upper() + '\n':
                    break
                for i in range(0, len(linelist)):
                    labels += linelist[i]
                count += 1
            
        if self.divider_found == True:
            self.ui.textEdit_labels.setText(labels)
            parameters = fp.readline().replace("\n", '')
            if self.ui.radioButton_frontpanel.isChecked():
                parameters = parameters.split('\t')
                for i in range(0, len(parameters)):
                    if parameters[i] == '#Date':
                        parameters[i] = 'Time'
                    elif parameters[i] == 'P1':
                        parameters[i] = 'Probe Line (P1)'
                    elif parameters[i] == 'P2':
                        parameters[i] = ' OVC Line (P2)'
                    elif parameters[i] == 'P3':
                        parameters[i] = 'IVC/Aux Port Line (P3)'
                    elif parameters[i] == 'P4':
                        parameters[i] = 'Turbo-to-S3 (P4)'
                    elif parameters[i] == 'P5':
                        parameters[i] = 'S3-to-traps (P5)'
                    elif parameters[i] == 'P6':
                        parameters[i] = '4He Dump (P6)'
                    elif parameters[i] == 'P7':
                        parameters[i] = '3He Dump (P7)'
                    elif parameters[i] == 'MG2':
                        parameters[i] = 'OVC Maxigauge (MG2)'
                    elif parameters[i] == 'MG3':
                        parameters[i] = 'Still Maxiguage (MG3)'
                    elif parameters[i] == 'MG4':
                        parameters[i] = 'IVC Maxiguage (MG4)'
                    elif parameters[i] == 'MG5':
                        parameters[i] = 'Probe Maxiguage (MG5)'
                    elif parameters[i] == 'P_low':
                        parameters[i] = 'P_high'
                    elif parameters[i] == 'P_high':
                        parameters[i] = 'P_low'
            elif self.ui.radioButton_zbridge.isChecked():
                parameters = parameters.split('\t')
                new_p = []
                new_p.append('Time')
                new_p.extend(parameters[12:22])
                parameters = new_p
            elif self.ui.radioButton_compressor.isChecked():
                parameters = parameters.split('\t')
            else:
                temp_parameters = parameters.split(',')
                if temp_parameters[0] == 'Date':
                    parameters = temp_parameters[1:]
                else:
                    parameters = temp_parameters
            
            # The following is for the units
            if self.ui.radioButton_ppms.isChecked():
                lines = fp.readline().replace("\n", "")
                first_data = lines.split(",")
                for i in range(0, len(first_data)):
                    par = []
                    if first_data[i] != '':
                        par = parameters[i].split(' (')
                        if len(par) == 2:
                            if par[1].replace(')', '') == 'sec':
                                units.append('hour')
                            else:
                                units.append(par[1].replace(')', ''))
                        elif len(par) == 1:
                            units.append('1')
                        new_parameters.append(par[0])
                parameters = new_parameters
            elif self.ui.radioButton_qmd.isChecked():
                units = fp.readline().replace("\n", '')
                units = units.split(",")
                if temp_parameters[0] == 'Date':
                    units = units[1:]
            elif self.ui.radioButton_frontpanel.isChecked():
                for i in range(0, len(parameters)):
                    units.append('')
            elif self.ui.radioButton_zbridge.isChecked():
                units.append('hour')
                for i in range(1, len(parameters)):
                    units.append('K')
            elif self.ui.radioButton_compressor.isChecked():
                units.append('')
                new_parameters.append(parameters[0])
                for i in range(1, len(parameters)):
                    par = []
                    if parameters[i] != "Errors":
                        par = parameters[i].split('(')
                        if par[1].replace(')', '') == 's':
                            units.append('h')
                        else:
                            units.append(par[1].replace(')', ''))
                        new_parameters.append(par[0])
                    else:
                        units.append("")
                        new_parameters.append(parameters[i])
                parameters = new_parameters
            
            self.ui.comboBox_second_x.addItem('None')
            self.ui.comboBox_second_y1.addItem('None')
            self.ui.comboBox_y2.addItem('None')
            self.ui.comboBox_second_y2.addItem('None')
            self.ui.comboBox_y3.addItem('None')
            self.ui.comboBox_second_y3.addItem('None')
            self.ui.comboBox_y4.addItem('None')
            self.ui.comboBox_second_y4.addItem('None')
            self.ui.comboBox_y5.addItem('None')
            self.ui.comboBox_second_y5.addItem('None')
            self.ui.comboBox_first.addItem('None')
            self.ui.comboBox_second.addItem('None')
            if self.ui.radioButton_compressor.isChecked():
                for i in range(1, len(parameters)):
                    self.ui.comboBox_x.addItem(parameters[i])
                    self.ui.comboBox_y1.addItem(parameters[i])
                    self.ui.comboBox_y2.addItem(parameters[i])
                    self.ui.comboBox_y3.addItem(parameters[i])
                    self.ui.comboBox_y4.addItem(parameters[i])
                    self.ui.comboBox_y5.addItem(parameters[i])
                    self.ui.comboBox_y_first_step.addItem(parameters[i])
                    self.ui.comboBox_y_second_step.addItem(parameters[i])               
                    self.ui.comboBox_second_x.addItem(parameters[i])
                    self.ui.comboBox_second_y1.addItem(parameters[i])
                    self.ui.comboBox_second_y2.addItem(parameters[i])
                    self.ui.comboBox_second_y3.addItem(parameters[i])
                    self.ui.comboBox_second_y4.addItem(parameters[i])
                    self.ui.comboBox_second_y5.addItem(parameters[i])
                    self.ui.comboBox_first.addItem(parameters[i])
                    self.ui.comboBox_second.addItem(parameters[i])
            elif self.ui.radioButton_zbridge.isChecked():
                self.ui.comboBox_x.addItem(parameters[0])
                for i in range(0, len(parameters)):
                    self.ui.comboBox_y_first_step.addItem(parameters[i])
                    self.ui.comboBox_y_second_step.addItem(parameters[i])               
                    self.ui.comboBox_first.addItem(parameters[i])
                    self.ui.comboBox_second.addItem(parameters[i])
            else:
                for i in range(0, len(parameters)):
                    self.ui.comboBox_x.addItem(parameters[i])
                    self.ui.comboBox_y1.addItem(parameters[i])
                    self.ui.comboBox_y2.addItem(parameters[i])
                    self.ui.comboBox_y3.addItem(parameters[i])
                    self.ui.comboBox_y4.addItem(parameters[i])
                    self.ui.comboBox_y5.addItem(parameters[i])
                    self.ui.comboBox_y_first_step.addItem(parameters[i])
                    self.ui.comboBox_y_second_step.addItem(parameters[i])               
                    self.ui.comboBox_second_x.addItem(parameters[i])
                    self.ui.comboBox_second_y1.addItem(parameters[i])
                    self.ui.comboBox_second_y2.addItem(parameters[i])
                    self.ui.comboBox_second_y3.addItem(parameters[i])
                    self.ui.comboBox_second_y4.addItem(parameters[i])
                    self.ui.comboBox_second_y5.addItem(parameters[i])
                    self.ui.comboBox_first.addItem(parameters[i])
                    self.ui.comboBox_second.addItem(parameters[i])
            
            for i in range(0, len(parameters)):
                new_data = [parameters[i], units[i], [], []]
                self.data.append(new_data)
    
            if self.ui.radioButton_ppms.isChecked():
                for i in range(0, len(first_data)):
                    if first_data[i] != '':
                        self.data[item][2].append(first_data[i])
                        item += 1
                
                length = item
                
            while True:
                
                val = []
                lines = fp.readline().replace("\n","")
                if lines == '':
                    break
                if self.ui.radioButton_frontpanel.isChecked() or self.ui.radioButton_compressor.isChecked() or self.ui.radioButton_zbridge.isChecked():
                    values = lines.split('\t')
                else:
                    values = lines.split(',')
                for i in range(0, len(values)):
                    if values[0] != 'Measurement was Aborted':
                        if values[i] != '':
                            val.append(values[i])
                if self.ui.radioButton_ppms.isChecked():
                    if len(val) < length:
                        break
                    for i in range(0, len(val)):
                        self.data[i][2].append(val[i])
                elif self.ui.radioButton_frontpanel.isChecked():
                    date_info = val[0].split(' ')
                    weekday = datetime.datetime.strptime(date_info[0], '%Y-%m-%d').strftime('%a')
                    date = date_info[0] + ' ' + weekday + ' ' + date_info[1]
                    self.data[0][3].append(date)
                    self.data[0][3].append(self.convert_time(val[0]))
                    for i in range(0, len(val) - 1):
                        self.data[i][2].append(val[i]) #+ 1])
                
                elif self.ui.radioButton_zbridge.isChecked():
                    date_info = val[0].split(' ')
                    weekday = datetime.datetime.strptime(date_info[0], '%Y-%m-%d').strftime('%a')
                    date = date_info[0] + ' ' + weekday + ' ' + date_info[1]
                    self.date_time.append(date)
                    self.data[0][2].append(val[1])
                    for i in range(1, len(parameters)):
                        if val[i + 11] == '-Inf':
                            self.data[i][3].append(z_item)
                        else:
                            self.data[i][2].append(val[i + 11])
                    
                elif self.ui.radioButton_qmd.isChecked():
                    if temp_parameters[0] == 'Date':
                        date_info = val[0].split(' ')
                        weekday = datetime.datetime.strptime(date_info[0], '%Y-%m-%d').strftime('%a')
                        date = date_info[0] + ' ' + weekday + ' ' + date_info[1]
                        self.date_time.append(date)
                        start = 1
                    else:
                        start = 0
                    for i in range(start, len(val)):
                        self.data[i - start][2].append(val[i])
                        
                else:
                    for i in range(0, len(val)):
                        self.data[i][2].append(val[i])
                z_item += 1
            
            
            if self.ui.radioButton_zbridge.isChecked():
                set_zero = float(self.data[0][2][0])
                for i in range(0, len(self.data[0][2])):
                    self.data[0][2][i] = ((float(self.data[0][2][i]) - set_zero) / 3600)
                new_data = []
                new_par = []
                for i in range(0, len(self.data)):
                    if len(self.data[i][3]) != len(self.data[0][2]):
                        new_data.append(self.data[i])
                        new_par.append(parameters[i])
                self.data = new_data
                parameters = new_par
                for i in range(0, len(parameters)):
                    self.ui.comboBox_y1.addItem(parameters[i])
                    self.ui.comboBox_y2.addItem(parameters[i])
                    self.ui.comboBox_y3.addItem(parameters[i])
                    self.ui.comboBox_y4.addItem(parameters[i])
                    self.ui.comboBox_y5.addItem(parameters[i])
                    
            if self.ui.radioButton_ppms.isChecked():
                set_zero = float(self.data[0][2][0])
                for i in range(0, len(self.data[0][2])):
                    self.data[0][2][i] = ((float(self.data[0][2][i]) - set_zero) / 3600)
                    
            if self.ui.radioButton_frontpanel.isChecked():
                set_zero = self.data[0][3][1]
                for i in range(0, len(self.data[0][2])):
                    self.data[0][2][i] = ((float(self.data[0][3][2 * i + 1]) - set_zero) / 3600)
                self.data[0][1] = 'hour'

            if self.open_recent == False:   
                self.item_info = []
                if self.ui.radioButton_frontpanel.isChecked():
                    self.item_info.append('frontpanel')
                elif self.ui.radioButton_compressor.isChecked():
                    self.item_info.append('compressor')
                else:
                    self.item_info.append(self.divider)
                self.item_info.append(self.file_name)
                self.item_info.append(str(self.ui.lineEdit_address.text()))
                self.all_info.append(self.item_info)
                self.ui.comboBox_recent.addItem(self.all_info[len(self.all_info) - 1][1])
            
            if self.ui.radioButton_compressor.isChecked():
                self.date_transfer = []
                date_tran = []
                date_tran = self.data[0][2]
                for i in range(0, len(date_tran)):
                    date_info = []
                    date_info = date_tran[i].split(' ')
                    weekday = date_info[0]
                    day = date_info[2]
                    year = date_info[4]
                    mon = date_info[1]
                    if mon == 'Jan':
                        mon = '01'
                    elif mon == 'Feb':
                        mon = '02'
                    elif mon == 'Mar':
                        mon = '03'
                    elif mon == 'Apr':
                        mon = '04'
                    elif mon == 'May':
                        mon = '05'
                    elif mon == 'Jun':
                        mon = '06'
                    elif mon == 'Jul':
                        mon = '07'
                    elif mon == 'Aug':
                        mon = '08'
                    elif mon == 'Sep':
                        mon = '09'
                    elif mon == 'Oct':
                        mon = '10'
                    elif mon == 'Nov':
                        mon = '11'
                    elif mon == 'Dec':
                        mon = '12'
                    date = year + '-' + mon + '-' + day + ' ' + weekday + ' ' + date_info[3]
                    self.date_transfer.append(date)
                #self.date_transfer.append(self.data[1][2])
                self.data = self.data[1:]
                for i in range(0, len(self.data[0][2])):
                    self.data[0][2][i] = float(self.data[0][2][i]) / 3600
                
            self.ui.groupBox_plot.setEnabled(True)
            self.ui.groupBox_first.setEnabled(True)
            self.ui.groupBox_second.setEnabled(True)
            self.ui.lineEdit_condition.setText('Ready to Plot.')
            self.ui.label_11.setEnabled(True)
            self.ui.comboBox_recent.setEnabled(True)
            self.ui.pushButton_recent.setEnabled(True)
            self.ui.comboBox_y_first_step.setEnabled(True)
            self.ui.pushButton_plot_first_step.setEnabled(True)
            self.ui.pushButton_plot_second_step.setEnabled(True)
            self.ui.comboBox_y_second_step.setEnabled(True)
            self.ui.label_14.setEnabled(True)
            self.ui.label_15.setEnabled(True)
            self.ui.groupBox_first.setEnabled(True)
            self.ui.groupBox_second.setEnabled(True)
            if self.ui.radioButton_frontpanel.isChecked() or self.ui.radioButton_compressor.isChecked():
                self.ui.groupBox_date.setEnabled(True)
            elif self.ui.radioButton_zbridge.isChecked():
                self.ui.groupBox_date.setEnabled(True)
                self.ui.groupBox_x.setEnabled(False)
                self.ui.groupBox_y1.setEnabled(False)
                self.ui.groupBox_y2.setEnabled(False)
                self.ui.groupBox_y3.setEnabled(False)
                self.ui.groupBox_y4.setEnabled(False)
                self.ui.groupBox_y5.setEnabled(False)
                self.ui.tabWidget_xy.setCurrentIndex(1)
                self.ui.groupBox_first.setEnabled(False)
                self.ui.groupBox_second.setEnabled(False)
            elif self.ui.radioButton_qmd.isChecked() and temp_parameters[0] == 'Date':
                self.ui.groupBox_date.setEnabled(True)
            self.ui.groupBox_modify.setEnabled(False)
            
    def Open_Recent(self):
        file_number = self.ui.comboBox_recent.currentIndex()
        if self.all_info[file_number][0].upper() == '[Data]'.upper():
            self.ui.radioButton_ppms.setChecked(True)
            self.ui.lineEdit_divider.setText('[Data]')
            self.divider = '[Data]' + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
        elif self.all_info[file_number][0].upper() == 'Collected Data'.upper():
            self.ui.radioButton_qmd.setChecked(True)
            self.ui.lineEdit_divider.setText('Collected Data')
            self.divider = 'Collected Data' + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
        elif self.all_info[file_number][0].upper() == 'frontpanel'.upper():
            self.ui.radioButton_frontpanel.setChecked(True)
            self.ui.lineEdit_divider.setText('')
            self.divider = self.all_info[file_number][1] + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
            self.ui.lineEdit_divider.setText('None')
            self.ui.lineEdit_condition.setText(self.ui.comboBox_recent.currentText() + ' has been opened.')
        elif self.all_info[file_number][0].upper() == 'compressor'.upper():
            self.ui.radioButton_compressor.setChecked(True)
            self.ui.lineEdit_divider.setText('')
            self.divider = self.all_info[file_number][1] + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
            self.ui.lineEdit_divider.setText('None')
            self.ui.lineEdit_condition.setText(self.ui.comboBox_recent.currentText() + ' has been opened.')
        elif self.all_info[file_number][0].upper() == '#'.upper():
            self.ui.radioButton_zbridge.setChecked(True)
            self.ui.lineEdit_divider.setText('#')
            self.divider = '#' + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
        
        self.reset_plot()
        self.ui.mplwidget.draw()
        self.open_recent = True
        self.OpenFile()
        
    def Find(self):
        try:
            time = float(self.ui.lineEdit_minute.text())
            if time <= float(self.data[0][2][0]):
                if self.ui.radioButton_frontpanel.isChecked():
                    self.ui.lineEdit_date.setText(self.data[0][3][0])
                elif self.ui.radioButton_compressor.isChecked():
                    self.ui.lineEdit_date.setText(self.date_transfer[0])
                else:
                    self.ui.lineEdit_date.setText(self.date_time[0])
            elif time >= float(self.data[0][2][len(self.data[0][2]) - 1]):
                if self.ui.radioButton_frontpanel.isChecked():
                    self.ui.lineEdit_date.setText(self.data[0][3][2 * (len(self.data[0][2]) - 1)])
                elif self.ui.radioButton_compressor.isChecked():
                    self.ui.lineEdit_date.setText(self.date_transfer[len(self.date_transfer) - 1])
                else:
                    self.ui.lineEdit_date.setText(self.date_time[len(self.date_time) - 1])
            else:
                item = 0
                while float(self.data[0][2][item]) - time < 0:
                    item += 1
                if abs(float(self.data[0][2][item - 1]) - time) <= abs(float(self.data[0][2][item]) - time):
                    if self.ui.radioButton_frontpanel.isChecked():
                        self.ui.lineEdit_date.setText(self.data[0][3][2 * (item - 1)])
                    elif self.ui.radioButton_compressor.isChecked():
                        self.ui.lineEdit_date.setText(self.date_transfer[item - 1])
                    else:
                        self.ui.lineEdit_date.setText(self.date_time[item - 1])
                else:
                    if self.ui.radioButton_frontpanel.isChecked():
                        self.ui.lineEdit_date.setText(self.data[0][3][2 * item])
                    elif self.ui.radioButton_compressor.isChecked():
                        self.ui.lineEdit_date.setText(self.date_transfer[item])
                    else:
                        self.ui.lineEdit_date.setText(self.date_time[item])
                        
        except ValueError:
            self.ui.lineEdit_date.setText('')
            self.ui.lineEdit_condition.setText('Please enter valid time.')
        
    def Plot_ready(self):
        self.x_value = []
        self.y1_value = []
        self.y2_value = []
        self.y3_value = []
        self.y4_value = []
        self.y5_value = []
        
        # The corresponding number of the comboBox
        self.x_num = 0
        self.x_num = self.ui.comboBox_x.currentIndex()
        self.y1_num = 0
        self.y1_num = self.ui.comboBox_y1.currentIndex()
        self.y2_num = 0
        self.y2_num = self.ui.comboBox_y2.currentIndex() - 1
        self.y3_num = 0
        self.y3_num = self.ui.comboBox_y3.currentIndex() - 1
        self.y4_num = 0
        self.y4_num = self.ui.comboBox_y4.currentIndex() - 1
        self.y5_num = 0
        self.y5_num = self.ui.comboBox_y5.currentIndex() - 1
        
        x_axis = self.data[self.x_num][0]
        x_unit = self.data[self.x_num][1]
        y1_axis = self.data[self.y1_num][0]
        y1_unit = self.data[self.y1_num][1]
        y2_axis = self.data[self.y2_num][0]
        y2_unit = self.data[self.y2_num][1]
        y3_axis = self.data[self.y3_num][0]
        y3_unit = self.data[self.y3_num][1]
        y4_axis = self.data[self.y4_num][0]
        y4_unit = self.data[self.y4_num][1]
        y5_axis = self.data[self.y5_num][0]
        y5_unit = self.data[self.y5_num][1]
        
        self.second_x_num = 0
        self.second_x_num = self.ui.comboBox_second_x.currentIndex() - 1
        self.second_y1_num = 0
        self.second_y1_num = self.ui.comboBox_second_y1.currentIndex() - 1
        self.second_y2_num = 0
        self.second_y2_num = self.ui.comboBox_second_y2.currentIndex() - 1
        self.second_y3_num = 0
        self.second_y3_num = self.ui.comboBox_second_y3.currentIndex() - 1
        self.second_y4_num = 0
        self.second_y4_num = self.ui.comboBox_second_y4.currentIndex() - 1
        self.second_y5_num = 0
        self.second_y5_num = self.ui.comboBox_second_y5.currentIndex() - 1
        
        second_x_axis = self.data[self.second_x_num][0]
        second_x_unit = self.data[self.second_x_num][1]
        second_y1_axis = self.data[self.second_y1_num][0]
        second_y1_unit = self.data[self.second_y1_num][1]
        second_y2_axis = self.data[self.second_y2_num][0]
        second_y2_unit = self.data[self.second_y2_num][1]
        second_y3_axis = self.data[self.second_y3_num][0]
        second_y3_unit = self.data[self.second_y3_num][1]
        second_y4_axis = self.data[self.second_y4_num][0]
        second_y4_unit = self.data[self.second_y4_num][1]
        second_y5_axis = self.data[self.second_y5_num][0]
        second_y5_unit = self.data[self.second_y5_num][1]
        
        self.y1_color_num = 0
        self.y1_color_num = self.ui.comboBox_color_y1.currentIndex()
        self.y1_color = self.Color(self.y1_color_num)
        self.y2_color_num = 0
        self.y2_color_num = self.ui.comboBox_color_y2.currentIndex()
        self.y2_color = self.Color(self.y2_color_num)
        self.y3_color_num = 0
        self.y3_color_num = self.ui.comboBox_color_y3.currentIndex()
        self.y3_color = self.Color(self.y3_color_num)
        self.y4_color_num = 0
        self.y4_color_num = self.ui.comboBox_color_y4.currentIndex()
        self.y4_color = self.Color(self.y4_color_num)
        self.y5_color_num = 0
        self.y5_color_num = self.ui.comboBox_color_y5.currentIndex()
        self.y5_color = self.Color(self.y5_color_num)
        
        self.y1_legend = self.ui.comboBox_y1.currentText()
        self.y2_legend = self.ui.comboBox_y2.currentText()
        self.y3_legend = self.ui.comboBox_y3.currentText()
        self.y4_legend = self.ui.comboBox_y4.currentText()
        self.y5_legend = self.ui.comboBox_y5.currentText()
        
        if self.ui.radioButton_zbridge.isChecked():
            self.y1_scale = 1E3
            if self.y1_num == 0:
                self.y1_scale = 1
            self.y2_scale = 1E3
            if self.y2_num == 0:
                self.y2_scale = 1
            self.y3_scale = 1E3
            if self.y3_num == 0:
                self.y3_scale = 1
            self.y4_scale = 1E3
            if self.y4_num == 0:
                self.y4_scale = 1
            self.y5_scale = 1E3
            if self.y5_num == 0:
                self.y5_scale = 1
        
        if self.second_x_num == -1:
            self.ui.lineEdit_x.setText(x_axis + ' (' + x_unit + ')')
            self.x_value = self.data[self.x_num][2]
        elif self.second_x_num >= 0:    
            if self.ui.radioButton_x_divide.isChecked():
                self.x_value = numpy.array(self.data[self.x_num][2], dtype = 'float') / numpy.array(self.data[self.second_x_num][2], dtype = 'float')
                x_title_mod = x_axis + '/' + second_x_axis
                self.ui.lineEdit_x.setText(x_title_mod + ' (' + x_unit + '/' + second_x_unit + ')')
            elif self.ui.radioButton_x_multiply.isChecked():
                self.x_value = numpy.array(self.data[self.x_num][2], dtype = 'float') * numpy.array(self.data[self.second_x_num][2], dtype = 'float')
                x_title_mod = x_axis + '*' + second_x_axis
                self.ui.lineEdit_x.setText(x_title_mod + ' (' + x_unit + '*' + second_x_unit + ')')
            elif self.ui.radioButton_x_plus.isChecked():
                self.x_value = numpy.array(self.data[self.x_num][2], dtype = 'float') + numpy.array(self.data[self.second_x_num][2], dtype = 'float')
                x_title_mod = x_axis + ' + ' + second_x_axis
                self.ui.lineEdit_x.setText(x_title_mod + ' (' + x_unit + ' + ' + second_x_unit + ')')
            elif self.ui.radioButton_x_minus.isChecked():
                self.x_value = numpy.array(self.data[self.x_num][2], dtype = 'float') - numpy.array(self.data[self.second_x_num][2], dtype = 'float')
                x_title_mod = x_axis + ' - ' + second_x_axis
                self.ui.lineEdit_x.setText(x_title_mod + ' (' + x_unit + ' - ' + second_x_unit + ')')
        if self.ui.checkBox_x_value.isChecked():
            self.x_value = numpy.absolute(self.x_value)
            
        if self.second_y1_num == -1:
            if self.ui.radioButton_frontpanel.isChecked() and self.y1_num != 0:
                self.ui.lineEdit_y.setText(y1_axis)
            else:
                self.ui.lineEdit_y.setText(y1_axis + ' (' + y1_unit + ')')
            self.y1_value = self.data[self.y1_num][2]    
        elif self.second_y1_num >= 0:
            if self.ui.radioButton_y1_divide.isChecked():
                self.y1_value = numpy.array(self.data[self.y1_num][2], dtype = 'float') / numpy.array(self.data[self.second_y1_num][2], dtype = 'float')
                y_title_mod = y1_axis + '/' + second_y1_axis
                self.ui.lineEdit_y.setText(y_title_mod + ' (' + y1_unit + '/' + second_y1_unit + ')')
            elif self.ui.radioButton_y1_multiply.isChecked():
                self.y1_value = numpy.array(self.data[self.y1_num][2], dtype = 'float') * numpy.array(self.data[self.second_y1_num][2], dtype = 'float')
                y_title_mod = y1_axis + '*' + second_y1_axis
                self.ui.lineEdit_y.setText(y_title_mod + ' (' + y1_unit + '*' + second_y1_unit + ')')
            elif self.ui.radioButton_y1_plus.isChecked():
                self.y1_value = numpy.array(self.data[self.y1_num][2], dtype = 'float') + numpy.array(self.data[self.second_y1_num][2], dtype = 'float')
                y_title_mod = y1_axis + ' + ' + second_y1_axis
                self.ui.lineEdit_y.setText(y_title_mod + ' (' + y1_unit + ' + ' + second_y1_unit + ')')
            elif self.ui.radioButton_y1_minus.isChecked():
                self.y1_value = numpy.array(self.data[self.y1_num][2], dtype = 'float') - numpy.array(self.data[self.second_y1_num][2], dtype = 'float')
                y_title_mod = y1_axis + ' - ' + second_y1_axis
                self.ui.lineEdit_y.setText(y_title_mod + ' (' + y1_unit + ' - ' + second_y1_unit + ')')
        if self.ui.checkBox_y1_value.isChecked():
            self.y1_value = numpy.absolute(self.y1_value)
        
        if self.y2_num != -1:
            if self.second_y2_num == -1:
                self.y2_value = self.data[self.y2_num][2]
            elif self.second_y2_num >= 0:
                if self.ui.radioButton_y2_divide.isChecked():
                    self.y2_value = numpy.array(self.data[self.y2_num][2], dtype = 'float') / numpy.array(self.data[self.second_y2_num][2], dtype = 'float')
                elif self.ui.radioButton_y2_multiply.isChecked():
                    self.y2_value = numpy.array(self.data[self.y2_num][2], dtype = 'float') * numpy.array(self.data[self.second_y2_num][2], dtype = 'float')
                elif self.ui.radioButton_y2_plus.isChecked():
                    self.y2_value = numpy.array(self.data[self.y2_num][2], dtype = 'float') + numpy.array(self.data[self.second_y2_num][2], dtype = 'float')
                elif self.ui.radioButton_y2_minus.isChecked():
                    self.y2_value = numpy.array(self.data[self.y2_num][2], dtype = 'float') - numpy.array(self.data[self.second_y2_num][2], dtype = 'float')
            if self.ui.checkBox_y2_value.isChecked():
                self.y2_value = numpy.absolute(self.y2_value)
        else:
            self.ui.radioButton_y2_divide.click()
            self.ui.comboBox_second_y2.setCurrentIndex(0)
            self.ui.checkBox_y2_value.setChecked(False)
            
        if self.y3_num != -1:
            if self.second_y3_num == -1:
                self.y3_value = self.data[self.y3_num][2]
            elif self.second_y3_num >= 0:
                if self.ui.radioButton_y3_divide.isChecked():
                    self.y3_value = numpy.array(self.data[self.y3_num][2], dtype = 'float') / numpy.array(self.data[self.second_y3_num][2], dtype = 'float')
                elif self.ui.radioButton_y3_multiply.isChecked():
                    self.y3_value = numpy.array(self.data[self.y3_num][2], dtype = 'float') * numpy.array(self.data[self.second_y3_num][2], dtype = 'float')
                elif self.ui.radioButton_y3_plus.isChecked():
                    self.y3_value = numpy.array(self.data[self.y3_num][2], dtype = 'float') + numpy.array(self.data[self.second_y3_num][2], dtype = 'float')
                elif self.ui.radioButton_y3_minus.isChecked():
                    self.y3_value = numpy.array(self.data[self.y3_num][2], dtype = 'float') - numpy.array(self.data[self.second_y3_num][2], dtype = 'float')
            if self.ui.checkBox_y3_value.isChecked():
                self.y3_value = numpy.absolute(self.y3_value)
        else:
            self.ui.radioButton_y3_divide.click()
            self.ui.comboBox_second_y3.setCurrentIndex(0)
            self.ui.checkBox_y3_value.setChecked(False)
            
        if self.y4_num != -1:
            if self.second_y4_num == -1:
                self.y4_value = self.data[self.y4_num][2]
            elif self.second_y4_num >= 0:
                if self.ui.radioButton_y4_divide.isChecked():
                    self.y4_value = numpy.array(self.data[self.y4_num][2], dtype = 'float') / numpy.array(self.data[self.second_y4_num][2], dtype = 'float')
                elif self.ui.radioButton_y4_multiply.isChecked():
                    self.y4_value = numpy.array(self.data[self.y4_num][2], dtype = 'float') * numpy.array(self.data[self.second_y4_num][2], dtype = 'float')
                elif self.ui.radioButton_y4_plus.isChecked():
                    self.y4_value = numpy.array(self.data[self.y4_num][2], dtype = 'float') + numpy.array(self.data[self.second_y4_num][2], dtype = 'float')
                elif self.ui.radioButton_y4_minus.isChecked():
                    self.y4_value = numpy.array(self.data[self.y4_num][2], dtype = 'float') - numpy.array(self.data[self.second_y4_num][2], dtype = 'float')
            if self.ui.checkBox_y4_value.isChecked():
                self.y4_value = numpy.absolute(self.y4_value)
        else:
            self.ui.radioButton_y4_divide.click()
            self.ui.comboBox_second_y4.setCurrentIndex(0)
            self.ui.checkBox_y4_value.setChecked(False)
            
        if self.y5_num != -1:
            if self.second_y5_num == -1:
                self.y5_value = self.data[self.y5_num][2]
            elif self.second_y5_num >= 0:
                if self.ui.radioButton_y5_divide.isChecked():
                    self.y5_value = numpy.array(self.data[self.y5_num][2], dtype = 'float') / numpy.array(self.data[self.second_y5_num][2], dtype = 'float')
                elif self.ui.radioButton_y5_multiply.isChecked():
                    self.y5_value = numpy.array(self.data[self.y5_num][2], dtype = 'float') * numpy.array(self.data[self.second_y5_num][2], dtype = 'float')
                elif self.ui.radioButton_y5_plus.isChecked():
                    self.y5_value = numpy.array(self.data[self.y5_num][2], dtype = 'float') + numpy.array(self.data[self.second_y5_num][2], dtype = 'float')
                elif self.ui.radioButton_y5_minus.isChecked():
                    self.y5_value = numpy.array(self.data[self.y5_num][2], dtype = 'float') - numpy.array(self.data[self.second_y5_num][2], dtype = 'float')
            if self.ui.checkBox_y5_value.isChecked():
                self.y5_value = numpy.absolute(self.y5_value)
        else:
            self.ui.radioButton_y5_divide.click()
            self.ui.comboBox_second_y5.setCurrentIndex(0)
            self.ui.checkBox_y5_value.setChecked(False)
            
        if self.second_x_num == -1 and self.second_y1_num == -1:
            self.ui.lineEdit_name.setText(y1_axis + ' vs. ' + x_axis)
        elif self.second_x_num >= 0 and self.second_y1_num == -1:
            self.ui.lineEdit_name.setText(y1_axis + ' vs. ' + x_title_mod)
        elif self.second_x_num == -1 and self.second_y1_num >= 0:
            self.ui.lineEdit_name.setText(y_title_mod + ' vs. ' + x_axis)
        else:
            self.ui.lineEdit_name.setText(y_title_mod + ' vs. ' + x_title_mod)
        
        self.ui.pushButton_change_name.setEnabled(True)
        self.ui.groupBox_modify.setEnabled(True)
        self.Pre_plot()
    
    def Color(self, num):
        if num == 0:
            return 'b'
        elif num == 1:
            return 'g'
        elif num == 2:
            return 'r'
        elif num == 3:
            return 'y'
        elif num == 4:
            return 'k'
        
    def Pre_plot(self):
        self.reset_plot()
        self.axes.grid()
        
        if self.ui.radioButton_zbridge.isChecked():
            self.x_value = numpy.array(self.x_value, dtype = 'float')
            self.y1_value = numpy.array(self.y1_value, dtype = 'float') / self.y1_scale
            if self.y2_num != -1:
                self.y2_value = numpy.array(self.y2_value, dtype = 'float') / self.y2_scale
            if self.y3_num != -1:
                self.y3_value = numpy.array(self.y3_value, dtype = 'float') / self.y3_scale
            if self.y4_num != -1:
                self.y4_value = numpy.array(self.y4_value, dtype = 'float') / self.y4_scale
            if self.y5_num != -1:
                self.y5_value = numpy.array(self.y5_value, dtype = 'float') / self.y5_scale
            
            # If some x values are -Inf, we need to delete them.
            if len(self.data[self.y1_num][3]) > 0:
                self.x1_plot = numpy.delete(self.x_value, self.data[self.y1_num][3])
                self.Plot(self.x1_plot, self.y1_value, self.y1_color, self.y1_legend)
                self.ui.label_ymin.setText('(' + str(format(numpy.min(self.y1_value), '.3f')) + ')')
                self.ui.label_ymax.setText('(' + str(format(numpy.max(self.y1_value), '.3f')) + ')')
                self.ui.label_xmin.setText('(' + str(format(numpy.min(self.x1_plot), '.3f')) + ')')
                self.ui.label_xmax.setText('(' + str(format(numpy.max(self.x1_plot), '.3f')) + ')')
            if self.y2_num != -1 and len(self.data[self.y2_num][3]) > 0:
                self.x2_plot = numpy.delete(self.x_value, self.data[self.y2_num][3])
                self.Plot(self.x2_plot, self.y2_value, self.y2_color, self.y2_legend)
            if self.y3_num != -1 and len(self.data[self.y3_num][3]) > 0:
                self.x3_plot = numpy.delete(self.x_value, self.data[self.y3_num][3])
                self.Plot(self.x3_plot, self.y3_value, self.y3_color, self.y3_legend)
            if self.y4_num != -1 and len(self.data[self.y4_num][3]) > 0:
                self.x4_plot = numpy.delete(self.x_value, self.data[self.y4_num][3])
                self.Plot(self.x4_plot, self.y4_value, self.y4_color, self.y4_legend)
            if self.y5_num != -1 and len(self.data[self.y5_num][3]) > 0:
                self.x5_plot = numpy.delete(self.x_value, self.data[self.y5_num][3])
                self.Plot(self.x5_plot, self.y5_value, self.y5_color, self.y5_legend)
            else:
                self.Plot(self.x_value, self.y1_value, self.y1_color, self.y1_legend)
                if self.y2_num != -1:
                    self.Plot(self.x_value, self.y2_value, self.y2_color, self.y2_legend)
                if self.y3_num != -1:
                    self.Plot(self.x_value, self.y3_value, self.y3_color, self.y3_legend)
                if self.y4_num != -1:
                    self.Plot(self.x_value, self.y4_value, self.y4_color, self.y4_legend)
                if self.y5_num != -1:
                    self.Plot(self.x_value, self.y5_value, self.y5_color, self.y5_legend)
                self.ui.label_ymin.setText('(' + str(format(numpy.min(self.y1_value), '.3f')) + ')')
                self.ui.label_ymax.setText('(' + str(format(numpy.max(self.y1_value), '.3f')) + ')')
                self.ui.label_xmin.setText('(' + str(format(numpy.min(self.x_value), '.3f')) + ')')
                self.ui.label_xmax.setText('(' + str(format(numpy.max(self.x_value), '.3f')) + ')')
        else:
            self.x_value = numpy.array(self.x_value, dtype = 'float') 
            self.y1_value = numpy.array(self.y1_value, dtype = 'float')
            self.Plot(self.x_value, self.y1_value, self.y1_color, self.y1_legend)
            if self.y2_num != -1:
                self.y2_value = numpy.array(self.y2_value, dtype = 'float')
                self.Plot(self.x_value, self.y2_value, self.y2_color, self.y2_legend)
            if self.y3_num != -1:
                self.y3_value = numpy.array(self.y3_value, dtype = 'float')
                self.Plot(self.x_value, self.y3_value, self.y3_color, self.y3_legend)
            if self.y4_num != -1:
                self.y4_value = numpy.array(self.y4_value, dtype = 'float')
                self.Plot(self.x_value, self.y4_value, self.y4_color, self.y4_legend)
            if self.y5_num != -1:
                self.y5_value = numpy.array(self.y5_value, dtype = 'float')
                self.Plot(self.x_value, self.y5_value, self.y5_color, self.y5_legend)
            self.ui.label_ymin.setText('(' + str(format(numpy.min(self.y1_value), '.3f')) + ')')
            self.ui.label_ymax.setText('(' + str(format(numpy.max(self.y1_value), '.3f')) + ')')
            self.ui.label_xmin.setText('(' + str(format(numpy.min(self.x_value), '.3f')) + ')')
            self.ui.label_xmax.setText('(' + str(format(numpy.max(self.x_value), '.3f')) + ')')
        
        self.Draw()
        
    def Modify(self):
        try:
            self.reset_plot()
            self.axes.grid()
            
            x_modify = numpy.array([])
            x_origin = numpy.array([])
            y_modify = numpy.array([])
            y_origin = numpy.array([])

            if self.ui.radioButton_zbridge.isChecked():
                if len(self.data[self.y1_num][3]) > 0:
                    x_modify = self.x1_plot
                    x_origin = self.x1_plot
                    y_modify = numpy.array(self.y1_value)
                    y_origin = numpy.array(self.y1_value)
                else:
                    x_modify = numpy.array(self.x_value)
                    x_origin = numpy.array(self.x_value)
                    y_modify = numpy.array(self.y1_value)
                    y_origin = numpy.array(self.y1_value)
            else:
                x_modify = numpy.array(self.x_value)
                x_origin = numpy.array(self.x_value)
                y_modify = numpy.array(self.y1_value)
                y_origin = numpy.array(self.y1_value)
            x_exc = []
            y_exc = []
            if self.ui.lineEdit_y_min.text() != '':
                y_min = float(self.ui.lineEdit_y_min.text())
                for i in range(0, len(y_modify)):
                    if y_modify[i] < y_min:
                        x_exc.append(i)
                        y_exc.append(i)
            x_modify = numpy.delete(x_modify, x_exc)
            y_modify = numpy.delete(y_modify, y_exc)
            x_exc = []
            y_exc = []            
            if self.ui.lineEdit_y_max.text() != '':
                y_max = float(self.ui.lineEdit_y_max.text())
                for i in range(0, len(y_modify)):
                    if y_modify[i] > y_max:
                        x_exc.append(i)
                        y_exc.append(i)
            x_modify = numpy.delete(x_modify, x_exc)
            y_modify = numpy.delete(y_modify, y_exc)
            x_exc = []
            y_exc = []
            if self.ui.lineEdit_x_min.text() != '':
                x_min = float(self.ui.lineEdit_x_min.text())
                for i in range(0, len(x_modify)):
                    if x_modify[i] < x_min:
                        x_exc.append(i)
                        y_exc.append(i)
            x_modify = numpy.delete(x_modify, x_exc)
            y_modify = numpy.delete(y_modify, y_exc)
            x_exc = []
            y_exc = []
            if self.ui.lineEdit_x_max.text() != '':
                x_max = float(self.ui.lineEdit_x_max.text())
                
                for i in range(0, len(x_modify)):
                    if x_modify[i] > x_max:
                        x_exc.append(i)
                        y_exc.append(i)
            x_modify = numpy.delete(x_modify, x_exc)
            y_modify = numpy.delete(y_modify, y_exc)
            self.ui.label_ymin.setText('(' + str(format(numpy.min(y_origin), '.3f')) + ')')
            self.ui.label_ymax.setText('(' + str(format(numpy.max(y_origin), '.3f')) + ')')
            self.ui.label_xmin.setText('(' + str(format(numpy.min(x_origin), '.3f')) + ')')
            self.ui.label_xmax.setText('(' + str(format(numpy.max(x_origin), '.3f')) + ')')
            self.Plot(x_modify, y_modify, self.y1_color, self.y1_legend)
            self.ui.pushButton_return.setEnabled(True)
            self.tab_number = self.ui.tabWidget_xy.currentIndex()
            self.ui.tabWidget_xy.setCurrentIndex(1)
            print self.tab_number
            
            self.Draw()
        except ValueError:
            self.ui.lineEdit_condition.setText('Please enter valid Min and Max.')
            
    def Return(self):
        x_return = []
        y_return = []
        if self.ui.radioButton_zbridge.isChecked():
            if len(self.data[self.y1_num][3]) > 0:
                x_return = self.x1_plot
                y_return = numpy.array(self.y1_value)
        else:
            x_return = numpy.array(self.x_value)
            y_return = numpy.array(self.y1_value)
        self.ui.label_ymin.setText('')
        self.ui.label_ymax.setText('')
        self.ui.label_xmin.setText('')
        self.ui.label_xmax.setText('')
        self.ui.lineEdit_y_min.setText('')
        self.ui.lineEdit_y_max.setText('')
        self.ui.lineEdit_x_min.setText('')
        self.ui.lineEdit_x_max.setText('')
        self.ui.pushButton_return.setEnabled(False)
        self.ui.tabWidget_xy.setCurrentIndex(self.tab_number)
        self.Plot_ready()
    
    def Change_name(self):
        self.axes.set_title(self.ui.lineEdit_name.text())
        self.axes.set_xlabel(self.ui.lineEdit_x.text())
        self.axes.set_ylabel(self.ui.lineEdit_y.text())
        self.Draw()
            
    def Plot(self, x, y, c, l):
        self.axes.plot(x, y, color = c, marker = '.', linestyle = ':', label= l)
        self.axes.set_title(self.ui.lineEdit_name.text())
        self.axes.set_xlabel(self.ui.lineEdit_x.text())
        self.axes.set_ylabel(self.ui.lineEdit_y.text())
        self.axes.legend()
        self.ui.lineEdit_condition.setText('Plot successfully.')
        
    def Draw(self):
        self.ui.mplwidget.draw()
    
    def plot1(self):
        y_value1 = self.ui.comboBox_y_first_step.currentIndex()
        y_value2 = self.ui.comboBox_first.currentIndex() - 1
        y_axis1 = self.data[y_value1][0]
        y_axis2 = self.data[y_value2][0]
        y_unit1 = self.data[y_value1][1]
        y_unit2 = self.data[y_value2][1]
        yv1 = numpy.array(self.data[y_value1][2], dtype = 'float')
        yv2 = numpy.array(self.data[y_value2][2], dtype = 'float')
        xv = []
        y_value1_scale = 1
        y_value2_scale = 1
        
        if self.ui.radioButton_zbridge.isChecked():
            if y_value1 != 0:
                y_value1_scale = 1E3
            if y_value2 != 0:
                y_value2_scale = 1E3
            
        if self.ui.radioButton_zbridge.isChecked():
            xv = self.data[0][2]
            xv = numpy.delete(xv, self.data[y_value1][3])
        elif self.ui.radioButton_frontpanel.isChecked():
            xv = self.data[0][2]
        else:
            item = 0
            for i in range(0, len(yv1)):
                xv.append(item)
                item += 1
        
        if y_value2 == -1:
            y_value = yv1 / y_value1_scale
            y_name = y_axis1 + ' (' + y_unit1 + ')'
            name = y_axis1 + ' Steps'
        elif y_value2 >= 0:
            yv2 = yv2 / y_value2_scale
            if self.ui.radioButton_first_divide.isChecked():
                y_value = numpy.array(yv1 / yv2)
                y_name = y_axis1 + ' / ' + y_axis2 + ' (' + y_unit1 + ' / ' + y_unit2 + ')'
                name = y_axis1 + ' / ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_first_multiply.isChecked():
                y_value = numpy.array(yv1 / yv2)
                y_name = y_axis1 + ' * ' + y_axis2 + ' (' + y_unit1 + ' * ' + y_unit2 + ')'
                name = y_axis1 + ' * ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_first_plus.isChecked():
                y_value = numpy.array(yv1 / yv2)
                y_name = y_axis1 + ' + ' + y_axis2 + ' (' + y_unit1 + ' + ' + y_unit2 + ')'
                name = y_axis1 + ' + ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_first_minus.isChecked():
                y_value = numpy.array(yv1 / yv2)
                y_name = y_axis1 + ' - ' + y_axis2 + ' (' + y_unit1 + ' - ' + y_unit2 + ')'
                name = y_axis1 + ' - ' + y_axis2 + ' Steps'
        if self.ui.checkBox_first.isChecked():
            y_value = numpy.absolute(y_value)      
        
        self.reset_first_step_plot()
        self.axes_first_step.plot(xv, y_value, marker = '.', linestyle = ':')
        self.axes_first_step.grid()
        self.axes_first_step.set_title(name)
        if self.ui.radioButton_zbridge.isChecked() or self.ui.radioButton_frontpanel.isChecked():
            self.axes_first_step.set_xlabel('Time (s)')
        else:
            self.axes_first_step.set_xlabel('Unit Step (1)')
        self.axes_first_step.set_ylabel(y_name)
        self.ui.mplwidget_first_step.draw()
 
    def plot2(self):
        y_value1 = self.ui.comboBox_y_second_step.currentIndex()
        y_value2 = self.ui.comboBox_second.currentIndex() - 1
        y_axis1 = self.data[y_value1][0]
        y_axis2 = self.data[y_value2][0]
        y_unit1 = self.data[y_value1][1]
        y_unit2 = self.data[y_value2][1]
        yv1 = numpy.array(self.data[y_value1][2], dtype = 'float')
        yv2 = numpy.array(self.data[y_value2][2], dtype = 'float')
        xv = []
        y_value1_scale = 1
        y_value2_scale = 1
        
        if self.ui.radioButton_zbridge.isChecked():
            if y_value1 != 0:
                y_value1_scale = 1E3
            if y_value2 != 0:
                y_value2_scale = 1E3
        
        if self.ui.radioButton_zbridge.isChecked():
            xv = self.data[0][2]
            xv = numpy.delete(xv, self.data[y_value1][3])
        elif self.ui.radioButton_frontpanel.isChecked():
            xv = self.data[0][2]
        else:
            item = 0
            for i in range(0, len(yv1)):
                xv.append(item)
                item += 1
        
        if y_value2 == -1:
            y_value = yv1 / y_value1_scale
            y_name = y_axis1 + ' (' + y_unit1 + ')'
            name = y_axis1 + ' Steps'
        elif y_value2 >= 0:
            yv2 = yv2 / y_value2_scale
            if self.ui.radioButton_second_divide.isChecked():
                y_value = numpy.array(yv1 / yv2)
                y_name = y_axis1 + ' / ' + y_axis2 + ' (' + y_unit1 + ' / ' + y_unit2 + ')'
                name = y_axis1 + ' / ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_second_multiply.isChecked():
                y_value = numpy.array(yv1 / yv2)
                y_name = y_axis1 + ' * ' + y_axis2 + ' (' + y_unit1 + ' * ' + y_unit2 + ')'
                name = y_axis1 + ' * ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_second_plus.isChecked():
                y_value = numpy.array(yv1 / yv2)
                y_name = y_axis1 + ' + ' + y_axis2 + ' (' + y_unit1 + ' + ' + y_unit2 + ')'
                name = y_axis1 + ' + ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_second_minus.isChecked():
                y_value = numpy.array(yv1 / yv2)
                y_name = y_axis1 + ' - ' + y_axis2 + ' (' + y_unit1 + ' - ' + y_unit2 + ')'
                name = y_axis1 + ' - ' + y_axis2 + ' Steps'
        if self.ui.checkBox_second.isChecked():
            y_value = numpy.absolute(y_value)    
        
        self.reset_second_step_plot()
        self.axes_second_step.plot(xv, y_value, marker = '.', linestyle = ':')
        self.axes_second_step.grid()
        self.axes_second_step.set_title(name)
        if self.ui.radioButton_zbridge.isChecked() or self.ui.radioButton_frontpanel.isChecked():
            self.axes_first_step.set_xlabel('Time (s)')
        else:
            self.axes_first_step.set_xlabel('Unit Step (1)')
        self.axes_second_step.set_ylabel(y_name)
        self.ui.mplwidget_second_step.draw()   
    
    def reset_plot(self):
        self.ui.mplwidget.figure.clear()        
        self.axes = self.ui.mplwidget.figure.add_subplot(111)

    def reset_first_step_plot(self):
        self.ui.mplwidget_first_step.figure.clear()        
        self.axes_first_step = self.ui.mplwidget_first_step.figure.add_subplot(111)
        
    def reset_second_step_plot(self):
        self.ui.mplwidget_second_step.figure.clear()        
        self.axes_second_step = self.ui.mplwidget_second_step.figure.add_subplot(111)
    
    def convert_time(self, d):
        date, times = d.split(" ")
        year, month, day = date.split("-")
        hour, minute, second = times.split(":")
    
        t = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        t_sec = time.mktime(t.timetuple())

        return t_sec
    
    def closeEvent(self, question):
        quit_msg = "Do you want to quit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        # If your answer is "yes", then quit
        if reply == QMessageBox.Yes:
            question.accept()
        # If your answer is "no", then get back
        else:
            question.ignore()

if __name__ == "__main__":
    # To open the GUI
    app = QApplication(sys.argv)
    myapp = MyForm()
    
    # It shows the GUI
    myapp.show()
    
    # Exit the GUI when "x" button is clicked
    sys.exit(app.exec_())  
        
