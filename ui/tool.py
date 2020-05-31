# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tool.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(220, 811)
        Form.setMaximumSize(QtCore.QSize(220, 811))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 16))
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 40, 224, 36))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.doubleSpinBox_rotate = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_rotate.setDecimals(1)
        self.doubleSpinBox_rotate.setMinimum(-360.0)
        self.doubleSpinBox_rotate.setMaximum(360.0)
        self.doubleSpinBox_rotate.setObjectName("doubleSpinBox_rotate")
        self.horizontalLayout.addWidget(self.doubleSpinBox_rotate)
        self.btn_rotate = QtWidgets.QPushButton(self.widget)
        self.btn_rotate.setObjectName("btn_rotate")
        self.horizontalLayout.addWidget(self.btn_rotate)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "工具箱🧰"))
        self.label_2.setText(_translate("Form", "旋转"))
        self.btn_rotate.setText(_translate("Form", "确认"))
