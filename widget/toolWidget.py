# imports
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from ui.tool import Ui_Form


class toolWidget(QtWidgets.QWidget, Ui_Form):
    Signal_roatate = pyqtSignal(float)

    def __init__(self, parent=None):
        super(toolWidget, self).__init__(parent)
        self.setupUi(self)
        self._initUI()

    def _initUI(self):
        self._signal_call()
        pass

    def _signal_call(self):
        self.btn_rotate.clicked.connect(self._slot_rotate)
        pass

    def _slot_rotate(self):
        self.Signal_roatate.emit(self.doubleSpinBox_rotate.value())
        pass
