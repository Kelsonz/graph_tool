# encoding: utf8

# imports
from PyQt5.QtGui import QPixmap
from basic import exp
import os


class function:
    def __init__(self):
        pass

    @staticmethod
    def rotate(filename: str, degree: float):
        img = exp(filename)
        img.rotate(degree)
        fname = img.save()
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    pass
