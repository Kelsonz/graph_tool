# encoding: utf8
# module: main
"""

"""
# imports
import sys

# PyQt5
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from ui.main import Ui_MainWindow
from enum import Enum, unique
from function import function


class main(QtWidgets.QMainWindow, Ui_MainWindow):
    Signal_opt = pyqtSignal(str, Enum, QtGui.QPixmap, str)

    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        self.setupUi(self)
        self._init()

    def setupUi(self, main_win):
        super().setupUi(main_win)
        # 设置App Icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/Tools.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_win.setWindowIcon(icon)
        # 信号槽链接
        self._signal_call()

    def _init(self):
        self._slot_clear()
        pass

    def _slot_clear(self):
        self.historyWidget.clear()
        self.toolWidget.doubleSpinBox_rotate.setValue(0)
        self.toolWidget.spinBox_h.setValue(0)
        self.toolWidget.spinBox_w.setValue(0)
        self.toolWidget.doubleSpinBox_rate.setValue(1)
        self.toolWidget.comboBox_avg.setCurrentIndex(0)
        self.toolWidget.comboBox_mid.setCurrentIndex(0)
        self.toolWidget.comboBox_robert.setCurrentIndex(0)
        self.toolWidget.comboBox_prewitt.setCurrentIndex(0)
        self.toolWidget.comboBox_sobel.setCurrentIndex(0)
        self.toolWidget.comboBox_l.setCurrentIndex(0)
        self.toolWidget.comboBox_l48.setCurrentIndex(0)
        self.toolWidget.comboBox_gauss_size.setCurrentIndex(0)
        self.toolWidget.doubleSpinBox_gauss_sigma.setValue(1.4)
        self.toolWidget.spinBox_high.setValue(100)
        self.toolWidget.spinBox_low.setValue(50)
        self.toolWidget.spinBox_up.setValue(0)
        self.toolWidget.spinBox_down.setValue(0)
        self.toolWidget.spinBox_left.setValue(0)
        self.toolWidget.spinBox_right.setValue(0)
        pass

    def _signal_call(self):
        self.historyWidget.Signal_scene.connect(self._slot_img)
        self.Signal_opt.connect(self.historyWidget.slot_opt)
        self.historyWidget.Signal_clear.connect(self._slot_clear)

        self.toolWidget.Signal_flip.connect(self._slot_flip)
        self.toolWidget.Signal_roatate.connect(self._slot_rotate)
        self.toolWidget.Signal_zoom.connect(self._slot_zoom)
        self.toolWidget.Signal_resize_rate.connect(self._slot_zoom)
        self.toolWidget.Signal_move.connect(self._slot_move)
        # 平滑
        self.toolWidget.Signal_mid.connect(self._slot_mid)
        self.toolWidget.Signal_avg.connect(self._slot_avg)
        # 增强
        self.toolWidget.Signal_his.connect(self._slot_his)
        self.toolWidget.Signal_robert.connect(self._slot_robert)
        self.toolWidget.Signal_prewitt.connect(self._slot_prewitt)
        self.toolWidget.Signal_sobel.connect(self._slot_sobel)
        self.toolWidget.Signal_gauss.connect(self._slot_gauss)
        self.toolWidget.Signal_laplace.connect(self._slot_laplace)
        self.toolWidget.Signal_canny.connect(self._slot_canny)

    def _slot_canny(self, low: int, high: int):
        if self.is_exist():
            self.pix = function.canny(low=low, high=high)
            msg = 'low:%d high:%d' % (low, high)
            self.Signal_opt.emit(self.filename, opt.canny, self.pix, msg)
            self._show_img(self.pix)
        pass

    def _slot_laplace(self, size: int, hence: bool):
        if self.is_exist():
            self.pix = function.laplace(self.filename, size, hence)
            if hence:
                hence = '叠加'
            else:
                hence = '不叠加'
            if size == 4:
                size = '4领域'
            elif size == 8:
                size = '8领域'
            msg = '%s %s' % (size, hence)
            self.Signal_opt.emit(self.filename, opt.laplace, self.pix, msg)
            self._show_img(self.pix)
        pass

    def _slot_gauss(self, sigma: float, size: int):
        if self.is_exist():
            self.pix = function.gauss(self.filename, sigma, size)
            msg = 'sigma:%f size:%d' % (sigma, size)
            self.Signal_opt.emit(self.filename, opt.gauss, self.pix, msg)
            self._show_img(self.pix)
        pass

    def _slot_robert(self, hence: bool):
        if self.is_exist():
            self.pix = function.robert(self.filename, hence)
            if hence:
                msg = '叠加'
            else:
                msg = '不叠加'
            self.Signal_opt.emit(self.filename, opt.robert, self.pix, msg)
            self._show_img(self.pix)
        pass

    def _slot_prewitt(self, hence: bool):
        if self.is_exist():
            self.pix = function.prewitt(self.filename, hence)
            if hence:
                msg = '叠加'
            else:
                msg = '不叠加'
            self.Signal_opt.emit(self.filename, opt.prewitt, self.pix, msg)
            self._show_img(self.pix)
        pass

    def _slot_sobel(self, hence: bool):
        if self.is_exist():
            self.pix = function.sobel(self.filename, hence)
            if hence:
                msg = '叠加'
            else:
                msg = '不叠加'
            self.Signal_opt.emit(self.filename, opt.sobel, self.pix, msg)
            self._show_img(self.pix)
        pass

    def _slot_avg(self, size: int):
        if self.is_exist():
            self.pix = function.medial_filter(self.filename, size)
            size = str(size) + '*' + str(size)
            self.Signal_opt.emit(self.filename, opt.avg, self.pix, size)
            self._show_img(self.pix)

    def _slot_mid(self, size: int):
        if self.is_exist():
            self.pix = function.medial_filter(self.filename, size)
            size = str(size) + '*' + str(size)
            self.Signal_opt.emit(self.filename, opt.mid, self.pix, size)
            self._show_img(self.pix)

    def _slot_his(self):
        if self.is_exist():
            self.pix = function.his(self.filename)
            self.Signal_opt.emit(self.filename, opt.his, self.pix, '')
            self._show_img(self.pix)
        pass

    def _slot_rotate(self, degree: float):
        if self.is_exist():
            self.pix = function.rotate(self.filename, degree)
            self.Signal_opt.emit(self.filename, opt.rotate, self.pix, str(degree))
            self._show_img(self.pix)
        pass

    def _slot_flip(self, axis: str):
        if self.is_exist():
            self.pix = function.flip(self.filename, axis)
            if axis == 'x':
                self.Signal_opt.emit(self.filename, opt.flip, self.pix, '上下')
            elif axis == 'y':
                self.Signal_opt.emit(self.filename, opt.flip, self.pix, '左右')
            self._show_img(self.pix)
        pass

    def _slot_zoom(self, *args):
        if self.is_exist():
            if len(args) == 2:
                self.pix = function.zoom(self.filename, args[0], args[1])
                msg = '%d * %d' % (args[0], args[1])
                self.Signal_opt.emit(self.filename, opt.zoom, self.pix, msg)
            elif len(args) == 1:
                self.pix = function.zoom(self.filename, args[0])
                msg = '%f *' % (args[0])
                self.Signal_opt.emit(self.filename, opt.zoom, self.pix, msg)
            self._show_img(self.pix)
        pass

    def _slot_move(self, X, Y):
        if self.is_exist():
            self.pix = function.move(self.filename, X, Y)
            size = '(%d, %d)' % (X, Y)
            self.Signal_opt.emit(self.filename, opt.avg, self.pix, size)
            self._show_img(self.pix)

    def _show_img(self, pix):
        # 显示图片
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(pix)
        self.graphicsView.setScene(scene)
        self.graphicsView.show()

    def _slot_img(self, filename: str, pix: QtGui.QPixmap):
        self.pix = pix
        self.filename = filename
        self._show_img(pix)
        # 设置信息
        if filename != 'init':
            self.label_filename.setText(filename)
            size = 'h * w (%s * %s)' % (pix.height(), pix.width())
            self.label_size.setText(size)
        else:
            self.label_filename.setText('添加图片吧')
            self.label_size.setText('')
        # 设置其余信息
        self.toolWidget.spinBox_h.setValue(pix.height())
        self.toolWidget.spinBox_w.setValue(pix.width())

    def is_exist(self):
        return self.filename != 'init'


@unique
class opt(Enum):
    load = '加载图片'
    save = '保存图片'
    rotate = '旋转'
    flip = '翻转'
    zoom = '缩放'
    mid = '中值滤波'
    avg = '均值滤波'
    his = '直方图均衡化'
    robert = 'Robert算子'
    prewitt = 'Prewitt算子'
    sobel = 'Sobel算子'
    laplace = 'Laplace算子'
    gauss = 'Gauss平滑'
    canny = 'canny算子'


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = main()
    win.show()
    res = app.exec_()
    if res == 0:
        sys.exit(res)
