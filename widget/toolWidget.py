# imports
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from ui.tool import Ui_Form


class toolWidget(QtWidgets.QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(toolWidget, self).__init__(parent)
        self.setupUi(self)
        self._initUI()

    def _initUI(self):
        pass
