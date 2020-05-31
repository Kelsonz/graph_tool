# encoding: utf8

# imports
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from ui.history import Ui_Form
import enum
from main import opt


class historyWidget(QtWidgets.QWidget, Ui_Form):
    Signal_scene = pyqtSignal(str, QtGui.QPixmap)
    Signal_clear = pyqtSignal()
    pix_set = list()

    def __init__(self, parent=None):
        super(historyWidget, self).__init__(parent)
        self.setupUi(self)
        self._signel_call()
        self.clear()

    def _signel_call(self):
        self.btn_load.clicked.connect(self._open_img)
        self.btn_save.clicked.connect(self._save_img)
        self.tableWidget.itemClicked.connect(self._get_item)
        pass

    def _get_item(self, item: QtWidgets.QTableWidgetItem):
        row = item.row()
        index = len(self.pix_set) - 1 - row
        filename = self.pix_set[index][0]
        opt = self.pix_set[index][1]
        pix = self.pix_set[index][2]
        self.Signal_scene.emit(filename, pix)
        return item.text()
        pass

    def _open_img(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开图片')
        # 维护历史列表
        if filename == '':
            pass
        else:
            pix = QtGui.QPixmap(filename)
            self.slot_opt(filename, opt.load, pix, filename.split('/')[-1])
            # 发射信号
            self.Signal_scene.emit(filename, pix)
        pass

    def _save_img(self):
        if self.is_exist():
            row = self.tableWidget.currentRow()
            if row == -1:
                row = 0
            index = len(self.pix_set) - 1 - row
            filename = self.pix_set[index][0].split('/')[-1]
            format = filename.split('.')[-1]
            opt = self.pix_set[index][1]
            pix = self.pix_set[index][2]
            msg = '是否保存\n' + opt + ' ' + filename
            reply = QtWidgets.QMessageBox.information(self, '保存确认', msg,
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Yes)
            if reply == QtWidgets.QMessageBox.Cancel:
                return
            elif reply == QtWidgets.QMessageBox.Yes:
                # 打开文件
                fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, '保存图片', filename)
                # 保存文件
                temp = fname.split('.')
                if format.lower() == 'svg':
                    format = 'png'
                if len(temp) == 1:
                    fname = '%s.%s' % (fname, format)
                pix.save(fname, format)
            self.Signal_clear.emit()
            pass

    def clear(self):
        # 清空图片和标题
        pix = QtGui.QPixmap('img/init.png')
        self.Signal_scene.emit('init', pix)
        # 清空表格
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        # 清空pix_list
        self.pix_set.clear()
        pass

    def slot_opt(self, fname: str, opt: enum, pix: QtGui.QPixmap, msg: str):
        self.pix_set.append([fname, opt.value, pix, msg])
        self._draw_table()

    def _draw_table(self):
        # 设置行列数
        LEN = len(self.pix_set)
        self.tableWidget.setRowCount(LEN)
        self.tableWidget.setColumnCount(2)
        # 设置表格
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 设置表头
        self.tableWidget.setHorizontalHeaderLabels(['操作', '信息'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setVisible(True)
        # 填充数据
        for i in range(LEN):
            index = LEN - i - 1
            op, msg = self._item(index)
            self.tableWidget.setItem(i, 0, op)
            self.tableWidget.setItem(i, 1, msg)
        pass

    def _item(self, index: int):
        filename = self.pix_set[index][0].split('/')[-1]
        op = self.pix_set[index][1]
        msg = self.pix_set[index][3]
        op = QtWidgets.QTableWidgetItem(op)
        msg = QtWidgets.QTableWidgetItem(msg)
        return op, msg

    def is_exist(self) -> bool:
        return len(self.pix_set) > 0
