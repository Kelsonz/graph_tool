#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 灰度直方图均衡化 """
__author__ = 'Kelsonz Fu'

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class grey:
    def __init__(self, filename):
        # 打开文件
        self.filename = filename
        self.im = Image.open(self.filename)
        # 获得图片属性
        self.xsize, self.ysize = self.im.size
        self.format = self.im.format
        self.mode = self.im.mode
        # 获得像素灰度值信息
        temp = self.im.load()
        self.pix = list()
        for j in range(self.ysize):
            for i in range(self.xsize):
                self.pix.append(temp[i, j])

    def get_filename(self):
        return self.filename.split('.')[0]

    def handle(self):

        # 频数统计
        self.n = [0] * 256
        for i in range(self.xsize * self.ysize):
            self.n[self.pix[i]] += 1
        # 频率计算
        p = [0] * 256
        for i in range(256):
            p[i] = self.n[i] / (self.xsize * self.ysize)
        # 累计频率计算
        cp = [0] * 256
        for i in range(256):
            cp[i] = self.sum_p(p, i)
        # 计算映射后的灰度值
        # new数组，索引与值分别代表映射前后的灰度值
        self.new = [0] * 256
        for i in range(256):
            self.new[i] = 255 * cp[i]
            self.new[i] = round(self.new[i])

        # 将映射后的频数对应起来，获得均衡化后的频数
        # yy数组，索引与值分别代表映射后的灰度值和频数
        self.yy = [0] * 256
        flag = self.new[0]
        for i in range(256):
            if flag != self.new[i]:
                self.yy[self.new[i]] = self.n[i]
                flag = self.new[i]
            else:
                self.yy[flag] += self.n[i]

        list1 = list(self.im.getdata())
        self.new_pix = list()
        for i in range(self.xsize * self.ysize):
            r = self.new[list1[i]]
            temp = (r, r, r)
            self.new_pix.append(temp)

    # 修正原图
    def print_change(self):
        self.im.putdata(self.new_pix)
        fname = 'aim.%s' % self.format
        self.im.save(fname)
        return fname

    # 绘直方图
    def print_Histogram(self):
        # x: 原灰度值
        x = np.arange(0, 256)
        # y: 原频数
        # yy: 映射后频数
        y = np.asarray(self.n)
        yy = np.asarray(self.yy)

        # 直方图
        plt.xlabel("r")
        plt.ylabel("s")
        plt.bar(x, y, label='old')
        plt.bar(x, yy, label='new')
        plt.legend()

        # 保存图像
        plt.savefig(self.get_filename() + '_Histogram')
        plt.show()

    # 绘灰度变换曲线
    def print_curve(self):
        # x: 原灰度值
        # new: 映射后灰度值
        x = np.arange(0, 256)
        new = np.asarray(self.new)
        # 灰度值变换曲线
        plt.xlabel('old')
        plt.ylabel('new')
        plt.plot(x, new)

        # 保存图像
        plt.savefig(self.get_filename() + '_curve')
        plt.show()

    def print_whole(self):
        # x: 原灰度值
        # new: 映射后灰度值
        x = np.arange(0, 256)
        new = np.asarray(self.new)
        # y: 原频数
        # yy: 映射后频数
        y = np.asarray(self.n)
        yy = np.asarray(self.yy)

        # 灰度值变换曲线
        plt.subplot(2, 1, 2)
        plt.xlabel('old')
        plt.ylabel('new')
        plt.plot(x, new)

        # 直方图
        plt.subplot(2, 1, 1)
        plt.xlabel("r")
        plt.ylabel("s")
        plt.bar(x, y, label='old')
        plt.bar(x, yy, label='new')
        plt.legend()

        # 保存图像
        plt.savefig(self.get_filename() + '_both')
        plt.show()

    # 计算累计频率
    def sum_p(self, x, index):
        sum = 0
        for i in range(index + 1):
            sum += x[i]
        return sum


if __name__ == "__main__":
    x = grey('grey.png')
    # 处理
    x.handle()
    # 打印变换后图像
    x.print_change()
    # 打印变换曲线和直方图
    # x.print_curve()
    # x.print_Histogram()
    x.print_whole()
