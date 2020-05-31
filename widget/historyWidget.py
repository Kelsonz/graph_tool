# imports
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from ui.history import Ui_Form


class historyWidget(QtWidgets.QWidget, Ui_Form):
    Signal_scene = pyqtSignal(str)

    def __init__(self, parent=None):
        super(historyWidget, self).__init__(parent)
        self.setupUi(self)
        self._initUI()
        self._signel_call()

    def _initUI(self):
        pass

    def _signel_call(self):
        self.btn_load.clicked.connect(self._open_file)
        pass

    def _open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开图片')
        self.Signal_scene.emit(filename)
        pass
