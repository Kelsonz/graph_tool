# imports
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from ui.tool import Ui_Form


class toolWidget(QtWidgets.QWidget, Ui_Form):
    Signal_roatate = pyqtSignal(float)
    Signal_flip = pyqtSignal(str)
    Signal_resize_rate = pyqtSignal(float)
    Signal_zoom = pyqtSignal(int, int)
    Signal_move = pyqtSignal(int, int)
    # 平滑
    Signal_mid = pyqtSignal(int)
    Signal_avg = pyqtSignal(int)
    Signal_gauss = pyqtSignal(float, int)
    # 增强
    Signal_his = pyqtSignal()
    Signal_robert = pyqtSignal(bool)
    Signal_prewitt = pyqtSignal(bool)
    Signal_sobel = pyqtSignal(bool)
    Signal_laplace = pyqtSignal(int, bool)
    Signal_canny = pyqtSignal(int, int)

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
        self.btn_hw.clicked.connect(lambda: self.Signal_zoom.emit(self.spinBox_h.value(),
                                                                  self.spinBox_w.value()))
        self.btn_rate.clicked.connect(lambda: self.Signal_resize_rate.emit(self.doubleSpinBox_rate.value()))
        self.btn_move.clicked.connect(
            lambda: self.Signal_move.emit(-self.spinBox_left.value() + self.spinBox_right.value(),
                                          -self.spinBox_up.value() + self.spinBox_down.value())
        )
        # 平滑
        self.btn_mid.clicked.connect(lambda: self.Signal_mid.emit(int(self.comboBox_mid.currentText())))
        self.btn_avg.clicked.connect(lambda: self.Signal_avg.emit(int(self.comboBox_avg.currentText())))
        self.btn_gauss.clicked.connect(lambda: self.Signal_gauss.emit(self.doubleSpinBox_gauss_sigma.value(),
                                                                      int(self.comboBox_gauss_size.currentText())))
        # 增强
        # self.btn.clicked.connect(lambda: self.Signal_his.emit())
        self.btn_robert.clicked.connect(lambda: self.Signal_robert.emit(self.comboBox_robert.currentText() == '叠加'))
        self.btn_prewitt.clicked.connect(lambda: self.Signal_prewitt.emit(self.comboBox_prewitt.currentText() == '叠加'))
        self.btn_sobel.clicked.connect(lambda: self.Signal_sobel.emit(self.comboBox_sobel.currentText() == '叠加'))
        self.btn_canny.clicked.connect(
            lambda: self.Signal_canny.emit(self.spinBox_low.value(), self.spinBox_high.value()))
        self.btn_laplace.clicked.connect(self._slot_laplace)
        pass

    def _slot_laplace(self):
        size = 4
        if self.comboBox_l48.currentText() == '4领域':
            size = 4
        elif self.comboBox_l48.currentText() == '8领域':
            size = 8
        hence = self.comboBox_l.currentText() == '叠加'
        self.Signal_laplace.emit(size, hence)
