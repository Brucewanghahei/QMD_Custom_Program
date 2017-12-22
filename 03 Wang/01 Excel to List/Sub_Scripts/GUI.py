# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created: Tue Aug 09 15:53:04 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(542, 296)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(20, 110, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton_convert = QtGui.QPushButton(self.widget)
        self.pushButton_convert.setEnabled(False)
        self.pushButton_convert.setGeometry(QtCore.QRect(290, 50, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_convert.setFont(font)
        self.pushButton_convert.setObjectName(_fromUtf8("pushButton_convert"))
        self.pushButton_browse = QtGui.QPushButton(self.widget)
        self.pushButton_browse.setEnabled(False)
        self.pushButton_browse.setGeometry(QtCore.QRect(140, 50, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_browse.setFont(font)
        self.pushButton_browse.setObjectName(_fromUtf8("pushButton_browse"))
        self.label_address = QtGui.QLabel(self.widget)
        self.label_address.setGeometry(QtCore.QRect(20, 140, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_address.setFont(font)
        self.label_address.setText(_fromUtf8(""))
        self.label_address.setObjectName(_fromUtf8("label_address"))
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "File Address:", None))
        self.pushButton_convert.setText(_translate("MainWindow", "Convert", None))
        self.pushButton_browse.setText(_translate("MainWindow", "Browse", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

