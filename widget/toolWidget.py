# imports
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from ui.tool import Ui_Form


class toolWidget(QtWidgets.QWidget, Ui_Form):
    Signal_roatate = pyqtSignal(float)
    Signal_flip = pyqtSignal(str)
    Signal_resize_rate = pyqtSignal(float)
    Signal_zoom = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(toolWidget, self).__init__(parent)
        self.setupUi(self)
        self._initUI()

    def _initUI(self):
        self._signal_call()
        pass

    def _signal_call(self):
        self.btn_rotate.clicked.connect(lambda: self.Signal_roatate.emit(self.doubleSpinBox_rotate.value()))
        self.btn_updown.clicked.connect(lambda: self.Signal_flip.emit('x'))
        self.btn_leftright.clicked.connect(lambda: self.Signal_flip.emit('y'))
        self.btn_hw.clicked.connect(lambda: self.Signal_zoom.emit(self.spinBox_h.value(), self.spinBox_w.value()))
        self.btn_rate.clicked.connect(lambda: self.Signal_resize_rate.emit(self.doubleSpinBox_rate.value()))
        pass
