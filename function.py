# encoding: utf8

# imports
from PyQt5.QtGui import QPixmap
from basic import exp
from hence import ImageFilter
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

    @staticmethod
    def flip(filename: str, axis: str):
        img = exp(filename)
        img.flip(axis)
        fname = img.save()
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    @staticmethod
    def zoom(*args):
        img = exp(args[0])
        if len(args) == 3:
            img.resize((args[1], args[2]))
        elif len(args) == 2:
            img.resize(args[1])
        fname = img.save()
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    @staticmethod
    def medial_filter(filename: str, size: int):
        img = ImageFilter(filename)
        fname = img.medial_filter(size=size)
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    @staticmethod
    def avg_filter(filename: str, size: int):
        img = ImageFilter(filename)
        fname = img.avg_filter(size=size)
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    pass
