# imports
import sys

# PyQt5
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from ui.main import Ui_MainWindow


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
        pass

    def _signal_call(self):
        self.pushButton.clicked.connect(self._slot_openfile)

    def _slot_openfile(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开图片', '.')
        img = QtGui.QImage(filename)
        self.label.setPixmap(QtGui.QPixmap(filename))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = main()
    win.show()
    res = app.exec_()
    if res == 0:
        # win.save()
        sys.exit(res)
