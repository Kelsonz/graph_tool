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

    def _signal_call(self):
        self.historyWidget.Signal_scene.connect(self._slot_img)
        self.toolWidget.Signal_roatate.connect(self._slot_rotate)
        self.Signal_opt.connect(self.historyWidget.slot_opt)
        self.historyWidget.Signal_clear.connect(self._slot_clear)

    def _slot_clear(self):
        self.historyWidget.clear()
        self.toolWidget.doubleSpinBox_rotate.setValue(0)
        pass

    def _slot_rotate(self, degree: float):
        if self.is_exist():
            self.pix = function.rotate(self.filename, degree)
            self.Signal_opt.emit(self.filename, opt.rotate, self.pix, str(degree))
            self._show_img(self.pix)
        pass

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

    def is_exist(self):
        return self.filename != 'init'


@unique
class opt(Enum):
    load = '加载图片'
    save = '保存图片'
    rotate = '旋转'


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = main()
    win.show()
    res = app.exec_()
    if res == 0:
        sys.exit(res)
