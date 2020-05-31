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


class main(QtWidgets.QMainWindow, Ui_MainWindow):

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
        self.historyWidget.clear()
        pass

    def _signal_call(self):
        self.historyWidget.Signal_scene.connect(self._slot_img)

    def _slot_img(self, filename: str, pix: QtGui.QPixmap):
        # 显示图片
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(pix)
        self.graphicsView.setScene(scene)
        self.graphicsView.show()
        # 设置信息
        if filename != 'init':
            self.label_filename.setText(filename)
            size = 'h * w (%s * %s)' % (pix.height(), pix.width())
            self.label_size.setText(size)
        else:
            self.label_filename.setText('添加图片吧')
            self.label_size.setText('')


@unique
class opt(Enum):
    load = '加载图片'
    save = '保存图片'


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = main()
    win.show()
    res = app.exec_()
    if res == 0:
        sys.exit(res)
