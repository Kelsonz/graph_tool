# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 878)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/Tools.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(470, 70, 941, 751))
        self.graphicsView.setObjectName("graphicsView")
        self.toolWidget = toolWidget(self.centralwidget)
        self.toolWidget.setGeometry(QtCore.QRect(10, 10, 221, 811))
        self.toolWidget.setObjectName("toolWidget")
        self.historyWidget = historyWidget(self.centralwidget)
        self.historyWidget.setGeometry(QtCore.QRect(240, 10, 221, 811))
        self.historyWidget.setObjectName("historyWidget")
        self.label_size = QtWidgets.QLabel(self.centralwidget)
        self.label_size.setGeometry(QtCore.QRect(470, 40, 941, 20))
        self.label_size.setText("")
        self.label_size.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_size.setObjectName("label_size")
        self.label_filename = QtWidgets.QLabel(self.centralwidget)
        self.label_filename.setGeometry(QtCore.QRect(470, 20, 941, 16))
        self.label_filename.setText("")
        self.label_filename.setObjectName("label_filename")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "图像小工具"))


from widget.historyWidget import historyWidget
from widget.toolWidget import toolWidget
